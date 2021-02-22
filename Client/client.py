from __future__ import print_function
import logging

import grpc
import sys
import time
import copy
import threading

import wait_room_requests_pb2
import wait_room_requests_pb2_grpc

import play_room_requests_pb2
import play_room_requests_pb2_grpc

class Client:
    def __init__(self):
        self._address = 'localhost'
        self._wait_room_port = 50051

        self._progress_lock = threading.Lock()
        self._current_progress = 4, []

        self._state_lock = threading.Lock()
        self._current_state = None
        self._connected_to_server = False

        self._game_finished = False

    def register_client(self, name):
        self._name = name

        with grpc.insecure_channel(self._address + ":" + str(self._wait_room_port)) as channel:
            stub = wait_room_requests_pb2_grpc.WaitRoomReqtestsStub(channel)
            message = wait_room_requests_pb2.RegisterRequest(name = name)
            response = stub.Register(message)
            channel.close()

        return response.valid_name, response.available_server

    def ask_progress(self):
        with grpc.insecure_channel(self._address + ":" + str(self._wait_room_port)) as channel:
            stub = wait_room_requests_pb2_grpc.WaitRoomReqtestsStub(channel)
            message = wait_room_requests_pb2.AskProgressRequest(name = self._name)
            response = stub.AskProgress(message)
            channel.close()
        with self._progress_lock:
            self._current_progress = response.players_remaining, response.name
            return self._current_progress

    def _ask_playing_port(self):
        with grpc.insecure_channel(self._address + ":" + str(self._wait_room_port)) as channel:
            stub = wait_room_requests_pb2_grpc.WaitRoomReqtestsStub(channel)
            message = wait_room_requests_pb2.PortRequest(name = self._name)
            response = stub.AskPlayPort(message)
            channel.close()
        self._session_port = response.port
    
    def get_room(self):
        return self._session_port - self._wait_room_port

    def connected(self):
        return self._connected_to_server

    def start_play(self):
        self._ask_playing_port()
        print("Received port number {}".format(self._session_port))

        with grpc.insecure_channel(self._address + ":" + str(self._session_port)) as channel:
            stub = play_room_requests_pb2_grpc.PlayRoomRequestsStub(channel)
            message = play_room_requests_pb2.StartPlayRequest(name = self._name)
            response = stub.StartPlay(message)
            print("Succesfully connected to play room!")
            self._connected_to_server = True
            channel.close()
        return True

    def pull_game_state(self):
        with grpc.insecure_channel(self._address + ":" + str(self._session_port)) as channel:
            stub = play_room_requests_pb2_grpc.PlayRoomRequestsStub(channel)
            message = play_room_requests_pb2.StateRequest(name = self._name)
            response = stub.Heartbeat(message)
            channel.close()

        with self._state_lock:
            self._current_state = response
            if self._current_state.game_finished:
                self._game_finished = True
            return self._current_state
    
    def game_finished(self):
        return self._game_finished

    def set_action(self, day, state, type, name):
        with grpc.insecure_channel(self._address + ":" + str(self._session_port)) as channel:
            stub = play_room_requests_pb2_grpc.PlayRoomRequestsStub(channel)
            message = play_room_requests_pb2.Action(
                day = day,
                state = state,
                name = self._name,
                type = type,
                who = name)
            response = stub.SetAction(message)
            print("Succesfully set action!")
            channel.close()