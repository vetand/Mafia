from concurrent import futures
import logging

import grpc
import sys
import threading
import time
import random
import copy
import json
import os
import requests
import time

import play_room_requests_pb2
import play_room_requests_pb2_grpc

import wait_room_requests_pb2
import wait_room_requests_pb2_grpc

PLAYERS_REQUIRED = 4
TURN_TIMEOUT = 30.0
PLAYER_TIMEOUT = 60.0

class Server(play_room_requests_pb2_grpc.PlayRoomRequests):
    def __init__(self, port, stop_event):
        super().__init__()
        self._address = '0.0.0.0:50051'
        self._port = port
        self._stop_event = stop_event
        self._start_play_time = dict()

        self._active_players = 0
        self._players_made_decision = 0
        self._current_actions = dict()

        self._roles = dict()
        self._alive = dict()
        self._day_state = True
        self._prev_heartbeat = dict()
        self._known_roles = set()

        self._current_day = 1
        self._game_finished = False

        if PLAYERS_REQUIRED == 4:
            self._available_roles = \
                [
                    'commoner',
                    'commoner',
                    'mafia',
                    'commissar'
                ]
        random.shuffle(self._available_roles)

        self._request_processing_lock = threading.Lock()

        self._next_event_time = time.time() + TURN_TIMEOUT
        self._timer = threading.Timer(TURN_TIMEOUT, self._change_day)
        self._timer.start()

    def _get_list_of_actions(self):
        with self._request_processing_lock:
            return copy.deepcopy(self._current_actions)

    def _is_mafia(self, name): # not thread safe
        return name in self._roles and self._roles[name] == 'mafia'

    def _get_visible_people(self, name):
        with self._request_processing_lock:
            answer = dict()
            for other_name in self._roles:
                if other_name in self._known_roles:
                    answer[other_name] = self._roles[other_name]
                    continue
                if self._is_mafia(other_name) and self._is_mafia(name):
                    answer[other_name] = self._roles[other_name]
                    continue
                if other_name == name:
                    answer[other_name] = self._roles[other_name]
                    continue
            return answer

    def _change_day(self): # already thread-safe
        self._timer.cancel()
        for name in self._alive.keys():
            if time.time() - self._prev_heartbeat[name] >= PLAYER_TIMEOUT:
                self._alive[name] = False

        self._players_made_decision = 0

        votes = dict()
        for name in self._current_actions:
            action = self._current_actions[name]
            if action.type == 'kill':
                if action.who not in votes:
                    votes[action.who] = 1
                else:
                    votes[action.who] += 1
            elif action.type == 'check':
                self._known_roles.add(action.who)
        if len(votes) > 0:
            names = [key for key in votes.keys() if votes[key] == max(votes.values())]
            if len(names) == 1:
                self._alive[names[0]] = False
                self._known_roles.add(names[0])
        self._current_actions = dict()

        if self._day_state:
            self._day_state = False
            self._active_players = sum([self._roles[name] in ['mafia', 'commissar'] \
                                        and self._alive[name] \
                                        for name in self._roles.keys()])
        else:
            self._day_state = True
            self._current_day += 1
            self._active_players = sum([self._alive[name] \
                                        for name in self._roles.keys()])
            
        print("Day is changed, {} active players".format(self._active_players))

        if self._check_game_over():
            return

        self._next_event_time = time.time() + TURN_TIMEOUT
        self._timer = threading.Timer(TURN_TIMEOUT, self._change_day)
        self._timer.start()

    def _check_game_over(self): # already thread-safe
        mafias = 0
        others = 0
        for name in self._alive.keys():
            if self._alive[name]:
                mafias += self._is_mafia(name)
                others += (1 != self._is_mafia(name))
        if mafias == 0 or mafias >= others:
            if mafias == 0:
                self._winners = ['commoner', 'commissar']
            else:
                self._winners = ['mafia']
            self._game_finished = True
            for name in self._roles.keys():
                self._known_roles.add(name)
            threading.Timer(3.0, self._detach_port).start()
            return True
        return False

    def _get_visible_actions(self, name): # already thread-safe
        if self._day_state:
            return self._current_actions
        result = dict()
        for other_name in self._current_actions.keys():
            if self._roles[other_name] == self._roles[name]:
                result[other_name] = self._current_actions[other_name]
        return result

    def _check_valid_action(self, request): # already thread-safe
        return self._current_day == request.day and self._day_state == request.state

    def StartPlay(self, request, context):
        with self._request_processing_lock:
            self._active_players += 1
            role = self._available_roles.pop()
            name = request.name
            print("{} is now {}!".format(name, role))

            self._roles[name] = role
            self._alive[name] = True
            self._start_play_time[name] = time.time()
            self._prev_heartbeat[name] = time.time()

            return play_room_requests_pb2.NewRoleAssignment(role = role)

    def Heartbeat(self, request, context):
        self._prev_heartbeat[request.name] = time.time()

        answer = play_room_requests_pb2.StateResponse \
            (
                game_finished = self._game_finished,
                day_number = self._current_day,
                state = self._day_state,
                alive = self._alive,
                actions = self._get_visible_actions(request.name),
                roles = self._get_visible_people(request.name),
                time_till_next_event = self._next_event_time - time.time()
            )
        return answer

    def SetAction(self, request, context):
        print("Receive action {} from {}".format(request.type, request.name))
        with self._request_processing_lock:
            if self._check_valid_action(request):
                if request.name not in self._current_actions:
                    self._players_made_decision += 1
                    self._current_actions[request.name] = request
                elif request.type != 'none':
                    self._current_actions[request.name] = request
                elif request.type == 'none':
                    self._players_made_decision -= 1
                    del self._current_actions[request.name]
                print("{} players already made decision".format(self._players_made_decision))
            
                if self._players_made_decision == self._active_players:
                    self._change_day()
        return request

    def _send_game_statistics(self):
        # register all players, is the name already exists nothing happens
        for name in self._alive.keys():
            request_data = dict()
            request_data['name'] = name
            request_data['gender'] = 'undefined'
            request_data['email'] = 'none'
            url = 'http://webserver:5000/mafia/api/v1.0/players'
            headers = {'Content-Type': 'application/json'}
            requests.post(url, json = json.dumps(request_data), headers=headers)

        player_list = requests.get('http://webserver:5000/mafia/api/v1.0/players').json()

        for player_obj in player_list:
            name = player_obj['name']
            if name in self._alive.keys():
                victory = self._roles[name] in self._winners
                add_time = time.time() - self._start_play_time[name]
                request_data = dict()
                request_data['time'] = int(add_time)
                request_data['victory'] = victory
                num = player_obj['player_url'].split('/')[-1]
                url = 'http://webserver:5000/mafia/api/v1.0/players/{}/stats'.format(num)
                requests.put(url, json = json.dumps(request_data))

    def _detach_port(self):
        self._send_game_statistics()
        with grpc.insecure_channel(self._address) as channel:
            stub = wait_room_requests_pb2_grpc.WaitRoomReqtestsStub(channel)
            message = wait_room_requests_pb2.EndSession(port = self._port)
            stub.ReturnRoom(message)
            channel.close()
        self._stop_event.set()

def serve(port):
    stop_event = threading.Event()
    server = grpc.server(futures.ThreadPoolExecutor(max_workers = 10))
    play_room_requests_pb2_grpc.add_PlayRoomRequestsServicer_to_server \
        (
            Server(port, stop_event), server
        )
    server.add_insecure_port('0.0.0.0:' + str(port))
    server.start()
    stop_event.wait()
    server.stop(0.1)

if __name__ == '__main__':
    serve(int(sys.argv[1]))

