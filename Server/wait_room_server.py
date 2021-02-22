from concurrent import futures
import logging

import grpc
import time
import threading
import copy
from subprocess import Popen
from audio_server import Server as AudioServer

import wait_room_requests_pb2
import wait_room_requests_pb2_grpc

from session import PLAYERS_REQUIRED

TIMEOUT = 1.5

class Server(wait_room_requests_pb2_grpc.WaitRoomReqtests):
    def __init__(self):
        super().__init__()

        self._clients_lock = threading.Lock()
        self._clients = set()
        self._playing_port = dict()
        self._available_ports = [50052, 50053, 50054]
        self._prev_heartbeat = dict()
        self._server = AudioServer(50055)

    def _add_new_client(self, name):
        with self._clients_lock:
            if name in self._clients or name in self._playing_port.keys():
                return False
            self._clients.add(name)
            self._prev_heartbeat[name] = time.time()
            print("New player with name {}".format(name))
        if self._get_remaining() <= 0:
            self._create_new_session()
        return True

    def _create_new_session(self):
        with self._clients_lock:
            if len(self._available_ports) == 0:
                return False
            port = self._available_ports.pop()
            for client in self._clients:
                self._playing_port[client] = port
            self._clients = set()

            print("Game on port #{} started!".format(port))
            Popen(['python', 'session.py', str(port)])
            time.sleep(2.0)
        return True

    def _get_remaining(self):
        with self._clients_lock:
            return PLAYERS_REQUIRED - len(self._clients)

    def _get_players(self):
        with self._clients_lock:
            answer = copy.deepcopy(self._clients)
        return list(answer)

    def AskProgress(self, request, context):
        with self._clients_lock:
            playing_port = copy.deepcopy(self._playing_port)
            self._prev_heartbeat[request.name] = time.time()
            
            to_delete = []
            for name in self._prev_heartbeat.keys():
                if time.time() - self._prev_heartbeat[name] > TIMEOUT:
                    to_delete.append(name)
            for name in to_delete:
                del self._prev_heartbeat[name]
                try:
                    self._clients.remove(name)
                except Exception as e:
                    continue
                print("Client with name {} disconnected!".format(name))
    
        if request.name not in playing_port.keys():
            return wait_room_requests_pb2.SessionLoadProgress \
                (
                    players_remaining = self._get_remaining(),
                    name =              self._get_players()
                )
        return wait_room_requests_pb2.SessionLoadProgress \
            (
                players_remaining = 0,
                name = self._get_players()
            )

    def Register(self, request, context):
        available_server = len(self._available_ports) > 0
        if available_server:
            return wait_room_requests_pb2.RegisterResponse \
                (
                    valid_name = self._add_new_client(request.name),
                    available_server = available_server
                )
        else:
            return wait_room_requests_pb2.RegisterResponse \
                (
                    valid_name = True,
                    available_server = False
                )

    def AskPlayPort(self, request, context):
        with self._clients_lock:
            return wait_room_requests_pb2.PortResponse \
                (
                    port = self._playing_port[request.name]
                )
    
    def ReturnRoom(self, request, context):
        port = request.port
        print("Game on port #{} finished!".format(port))
        with self._clients_lock:
            self._available_ports.append(port)
            to_delete = []
            for address in self._playing_port.keys():
                if self._playing_port[address] == port:
                    to_delete.append(address)
            for port in to_delete:
                del self._playing_port[port]
                try:
                    del self._prev_heartbeat[port]
                except Exception as e:
                    pass
        return request

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    wait_room_requests_pb2_grpc.add_WaitRoomReqtestsServicer_to_server(Server(), server)
    server.add_insecure_port('0.0.0.0:50051')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
