import kivy   
from kivy.app import App 
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout 
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.config import Config
from client import Client
from functools import partial
import sounddevice as sd
import threading
import copy
import time
import json
from audio_client import Client as AudioClient

Config.set('graphics', 'width', '800')
Config.set('graphics', 'height', '800')
Config.set('graphics', 'resizable', True)
Config.write()

PLAYERS_REQUIRED = 4

class MyApp(App):

    def _change_room(self, room, instance):
        if instance.state == 'down':
            success = self._audio_client.change_room(room)
            if not success:
                instance.state = 'normal'
        else:
            self._audio_client.drop_room()

    def _talk_switch_change(self, instance):
        if instance.state == 'down':
            self._audio_client.set_talking_mode()
        else:
            self._audio_client.turn_down_talking_mode()

    def _handle_audio(self):
        with sd.Stream(samplerate = 44100, blocksize = 11360, channels = 1,
                                         callback = self._audio_client.callback):
            while not self._client._game_finished and not self._game_finished:
                time.sleep(0.5)

    def _on_name_enter(self, instance):
        self._already_taken_label.opacity = 0
        valid_name, available_server = self._client.register_client(instance.text)
        self._my_name = instance.text

        if not valid_name:
            self._already_taken_label.text = "Name already taken!"
            self._already_taken_label.opacity = 1
        elif not available_server:
            self._already_taken_label.text = "No available servers, try again later!"
            self._already_taken_label.opacity = 1
        else:
            self._already_taken_label.opacity = 0
            self._enter_label.text = "Already registered players"
            self._title_label.text = "Awaiting other players"

            self._textinput.disabled = True
            self._textinput.multiline = True
            self._textinput.pos_hint = {'x':.2, 'y':.22 }
            self._textinput.size_hint = (.6, .22)

            self._waiting_room_loop()

    def _parse_players_list(self, num_remaining, str_data_players):
        answer = ""
        for name in str_data_players:
            answer += name
            if name == self._my_name:
                answer += " (me)"
            answer += "\n"
        answer += "\n... and need {} more players to go".format(num_remaining)
        return answer

    def _set_action(self, type, who, instance):
        if instance.text == 'check' and type == 'kill':
            type = 'check'
        if type == 'kill' and instance.state == 'down' or \
                type == 'none' and instance.state == 'normal' or \
                type == 'end day' and instance.state == 'down' or \
                type == 'check' and instance.state == 'down':
            self._client.set_action(self._current_day, self._current_state,\
                                    type, self._other_players[who])

    def _set_commissar_bindings(self, action):
        for i in range(PLAYERS_REQUIRED):
            self._kill_buttons[i].text = action

    def _update_day(self, state):
        names = list(state.alive.keys())
        names.sort()

        if state.roles[self._my_name] == 'commissar':
            if state.state:
                self._set_commissar_bindings('kill')
            else:
                self._set_commissar_bindings('check')

        self._current_day = state.day_number
        self._current_state = state.state
        for i in range(PLAYERS_REQUIRED):
            if len(self._other_players) < PLAYERS_REQUIRED:
                break
            if self._other_players[i] in state.alive and state.alive[self._other_players[i]]:
                self._kill_buttons[i].disabled = False
                self._kill_buttons[i].state = 'normal'
            else:
                self._kill_buttons[i].opacity = 0
                self._kill_buttons[i].disabled = True

        if not state.alive[self._my_name]:
            for i in range(PLAYERS_REQUIRED):
                self._kill_buttons[i].disabled = True
                self._kill_buttons[i].state = 'normal'
                self._kill_buttons[i].opacity = 0
            self._end_day_btn.state = 'normal'
            self._end_day_btn.disabled = True
            self._end_day_btn.opacity = 0
        else:
            self._kill_buttons[self._player_number[self._my_name]].opacity = 0
            self._kill_buttons[self._player_number[self._my_name]].disabled = True
            self._end_day_btn.state = 'normal'
            self._end_day_btn.disabled = False
        
        self._talk_btn.state = 'normal'
        self._talk_btn.opacity = 0
        self._talk_btn.disabled = True
        self._audio_client.turn_down_talking_mode()

        if state.state:
            self._time_label.text = "Day "
            if state.day_number == 1:
                for i in range(PLAYERS_REQUIRED):
                    self._kill_buttons[i].disabled = True
            if state.alive[self._my_name]:
                self._talk_btn.state = 'normal'
                self._talk_btn.opacity = 1
                self._talk_btn.disabled = False
        else:
            self._time_label.text = "Night "
            if state.roles[self._my_name] == "commoner" or not state.alive[self._my_name]:
                for i in range(PLAYERS_REQUIRED):
                    self._kill_buttons[i].disabled = True
                self._end_day_btn.disabled = True

        self._time_label.text += str(state.day_number)

        for name in names:
            if name in self._player_number:
                num = self._player_number[name]
                if name in state.roles:
                    self._role_labels[num].text = state.roles[name]

        for name in names:
            if name in self._player_number:
                if not state.alive[name]:
                    num = self._player_number[name]
                    self._role_labels[num].text += ' (dead)'

    def _open_result_table(self, state):
        for i in range(PLAYERS_REQUIRED):
            self._kill_buttons[i].opacity = 0
            self._kill_buttons[i].disabled = 0

            self._player_labels[i].opacity = 0
            self._role_labels[i].opacity = 0
            self._action_labels[i].opacity = 0

        self._end_day_btn.opacity = 0
        self._end_day_btn.disabled = 0

        self._talk_btn.opacity = 0
        self._talk_btn.disabled = 0

        self._time_label.opacity = 0

        verdict = "Commoners won!"
        for name in state.alive.keys():
            if state.roles[name] == 'mafia' and state.alive[name]:
                verdict = "Mafia won!"

        self._title_label.text = verdict
        self._title_label.opacity = 1      

    def _pull_game_state(self):
        state = self._client.pull_game_state()

        names = list(state.alive.keys())
        names.sort()

        self._other_players = names
        self._player_number = \
            {self._other_players[i]: i for i in range(len(self._other_players))}

        for name in names:
            if name in self._player_number:
                num = self._player_number[name]
                self._player_labels[num].text = self._other_players[num]
            if name in self._player_number and name == self._my_name:
                num = self._player_number[name]
                self._player_labels[num].text += " (me)"

        if state.state != self._current_state or state.day_number != self._current_day:
            self._update_day(state)

        if self._client._game_finished:
            self._open_result_table(state)
            return

        self._timer_label.text = "0:" + str(int(state.time_till_next_event))

        for name in names:
            if name in self._player_number:
                num = self._player_number[name]
                if name in state.actions:
                    self._action_labels[num].text = state.actions[name].type
                    if state.actions[name].type in ['kill', 'check']:
                        self._action_labels[num].text += '->' + state.actions[name].who
                else:
                    self._action_labels[num].text = 'none'

        threading.Timer(1.0, self._pull_game_state).start()

    def _open_playground(self):
        self._title_label.opacity = 0
        self._enter_label.opacity = 0
        self._textinput.opacity = 0
        for btn in self._player_labels:
            btn.opacity = 1
        for btn in self._role_labels:
            btn.opacity = 1
        for btn in self._action_labels:
            btn.opacity = 1
        for btn in self._kill_buttons:
            btn.opacity = 1
            btn.disabled = False
        for i in range(PLAYERS_REQUIRED):
            self._kill_buttons[i].bind(on_press = partial
            (
                self._set_action, 
                'kill',
                i)
            )
            self._kill_buttons[i].bind(on_release = partial
            (
                self._set_action, 
                'none',
                i)
            )
        self._end_day_btn.opacity = 1
        self._end_day_btn.disabled = False
        self._talk_btn.bind(on_press = self._talk_switch_change)
        self._end_day_btn.bind(on_press = partial
            (
                self._set_action, 
                'end day',
                0)
            )
        self._end_day_btn.bind(on_release = partial
            (
                self._set_action, 
                'none',
                0)
            )
        connected = self._client.start_play()
        if connected:
            self._audio_client = AudioClient(rate = 44100, channels = 1, chunk_size = 1160)
            room_number = self._client.get_room()
            print("Assigned room number {}".format(room_number))
            self._audio_client.change_room(room_number)
            threading.Thread(target = self._handle_audio).start()

            self._current_day = 0
            self._current_state = False
            threading.Thread(target = self._pull_game_state).start()

    def _waiting_room_loop(self):
        if self._game_finished:
            return
        players_remaining = 1
        if not self._client.connected():
            players_remaining, players = self._client.ask_progress()
            self._textinput.text = self._parse_players_list(players_remaining, players)

        if players_remaining > 0:
            threading.Timer(0.5, self._waiting_room_loop).start()
        else:
            self._open_playground()
    
    def _exit_app(self, instance):
        self._game_finished = True
        self._client._game_finished = True
        self._audio_client.shutdown()
        self.stop()
  
    def build(self): 
        self._game_finished = False
        self._client = Client()
    
        Fl = FloatLayout()

        self._player_labels = []
        self._role_labels = []
        self._kill_buttons = []
        self._action_labels = []
        
        for i in range(PLAYERS_REQUIRED):
            self._player_labels.append( \
                Label(
                    text='Player' + str(i),
                    size_hint = (.2, .1),
                    font_size ='18sp',
                    pos_hint = {'x':.05, 'y': 0.8 - (i / (PLAYERS_REQUIRED-1)) * 0.6},
                    bold = True,
                    markup = True,
                    opacity = 0))
            self._role_labels.append( \
                Label(
                    text='Unknown',
                    size_hint = (.2, .1),
                    font_size ='18sp',
                    pos_hint = {'x':.27, 'y': 0.8 - (i / (PLAYERS_REQUIRED-1)) * 0.6},
                    bold = True,
                    markup = True,
                    opacity = 0))
            self._action_labels.append( \
                Label(
                    text='No action',
                    size_hint = (.2, .1),
                    font_size ='18sp',
                    pos_hint = {'x':.5, 'y': 0.8 - (i / (PLAYERS_REQUIRED-1)) * 0.6},
                    bold = True,
                    markup = True,
                    opacity = 0))
            self._kill_buttons.append(
                ToggleButton(
                    text = 'kill', size_hint = (.2, .1), 
                    background_color =(.3, .6, .7, 1), 
                    pos_hint = {'x':.75, 'y': 0.8 - (i / (PLAYERS_REQUIRED-1)) * 0.6},
                    opacity = 0, disabled = True, group = 'action'))

            Fl.add_widget(self._player_labels[-1])
            Fl.add_widget(self._role_labels[-1])
            Fl.add_widget(self._action_labels[-1])
            Fl.add_widget(self._kill_buttons[-1])

        self._talk_btn = ToggleButton(text = 'Talk', size_hint = (.25, .1), 
                                      background_color =(.3, .6, .7, 1), 
                                      pos_hint = {'x':.05, 'y':.05 },
                                      opacity = 0, disabled = True,
                                      group = 'talk')
        self._end_day_btn = ToggleButton(text = 'End day', size_hint = (.25, .1), 
                                    background_color =(.3, .6, .7, 1), 
                                    pos_hint = {'x':.38, 'y':.05 },
                                    opacity = 0, disabled = True, group = 'action')
        self._time_label = Label(text='',
                            size_hint = (.2, .1),
                            font_size ='28sp',
                            pos_hint = {'x':.02, 'y':.9 },
                            bold = True,
                            markup = True)
        self._timer_label = Label(text='',
                            size_hint = (.2, .1),
                            font_size ='28sp',
                            pos_hint = {'x':.78, 'y':.9 },
                            bold = True,
                            markup = True)
        
        Fl.add_widget(self._talk_btn)
        Fl.add_widget(self._end_day_btn)
        Fl.add_widget(self._time_label)
        Fl.add_widget(self._timer_label)

        self._title_label = Label(text='Welcome to mafia',
                            size_hint = (.4, .2),
                            font_size ='72sp',
                            pos_hint = {'x':.3, 'y':.6 },
                            bold = True,
                            markup = True)

        self._enter_label = Label(text='Enter your name',
                            size_hint = (.2, .1),
                            font_size ='48sp',
                            pos_hint = {'x':.4, 'y':.45 },
                            bold = True,
                            markup = True)

        self._already_taken_label = Label(text='Name already taken',
                            size_hint = (.2, .07),
                            font_size ='20sp',
                            pos_hint = {'x':.4, 'y':.30 },
                            color = 'red',
                            markup = True,
                            opacity = 0)

        self._exit_btn = Button(text = 'Exit', size_hint = (.25, .1), 
                        background_color = (.3, .6, .7, 1),
                        pos_hint = {'x':.7, 'y':.05 })
        self._exit_btn.bind(on_press = self._exit_app)

        self._textinput = TextInput(text = '', multiline = False,
                              size_hint = (.3, .06),
                              pos_hint = {'x':.35, 'y':.37 },
                              font_size = 24)
        self._textinput.bind(on_text_validate = self._on_name_enter)

        Fl.add_widget(self._textinput)
        Fl.add_widget(self._exit_btn)
        Fl.add_widget(self._title_label)
        Fl.add_widget(self._enter_label)
        Fl.add_widget(self._already_taken_label)
        return Fl

if __name__ == "__main__": 
    root = MyApp()
    root.run()
    root._client._game_finished = True
    root._game_finished = True
    root._audio_client.shutdown()