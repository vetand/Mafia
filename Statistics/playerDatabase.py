# create sqlite players database as follows:
'''
CREATE TABLE "players"("player_id"
    INTEGER PRIMARY KEY,
    "name" TEXT NOT NULL,
    "gender" TEXT NOT NULL,
    "email" TEXT NOT NULL);

CREATE TABLE "game_info"("player_id"
    INTEGER PRIMARY KEY,
    "games_complited" INT NOT NULL,
    "victories" INT NOT NULL,
    "defeats" INT NOT NULL,
    "overall_time_played" INT NOT NULL);
'''

import sqlite3
from flask import jsonify
import os

DB_PATH = './mafia.db' # player general info
NOTSTARTED = 'Not Started'

def get_all_players():
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        c.execute('select * from players')
        rows = c.fetchall()
        return rows
    except Exception as e:
        print('Database error: ', e)
        return None

def get_player(player_id):
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        c.execute("select * from players where player_id=?;" , [player_id])
        r = c.fetchone()
        return r
    except Exception as e:
        print('Database error: ', e)
    return None

def get_player_stats(player_id):
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        c.execute("select * from game_info where player_id=?;" , [player_id])
        r = c.fetchone()
        return r
    except Exception as e:
        print('Database error: ', e)
    return None

def add_to_list(name, gender, email):
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('insert into players(name, gender, email) values(?,?,?)', 
        (
            name,
            gender,
            email
        ))
        c.execute("""insert into game_info(
            games_complited,
            victories,
            defeats,
            overall_time_played) values(?,?,?,?)""", 
            (0, 0, 0, 0))
        conn.commit()
        result = get_player(c.lastrowid)
        return result
    except Exception as e:
        print('Database error: ', e)
        return None

def update_player(player_id, name, gender, email):
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('update players set name=?, gender=?, email=? where player_id=?',
        (
            name,
            gender,
            email,
            player_id
        ))
        conn.commit()
        result = get_player(player_id)
        return result
    except Exception as e:
        print('Database error: ', e)
        return None

def remove_player(player_id):
    try:
        remove_player_resourses(player_id)
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('DELETE FROM players WHERE player_id=?', [player_id])
        c.execute('DELETE FROM game_info WHERE player_id=?', [player_id])
        conn.commit()
        return jsonify( { 'result': True } )
    except Exception as e:
        print('Database error: ', e)
        return None

def name_exists(name):
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        c.execute("select * from players where name=?;" , [name])
        r = c.fetchone()
        return not r is None
    except Exception as e:
        print('Database error: ', e)
        return None

def update_game_statistics(player_id, victory, time):
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        c.execute("select * from game_info where player_id=?;" , [player_id])
        r = c.fetchone()
        games = r['games_complited'] + 1
        victories = r['victories'] + int(victory)
        defeats = r['defeats'] + 1 - int(victory)
        overall_time = r['overall_time_played'] + time
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('''update game_info set games_complited=?, 
                                          victories=?,
                                          defeats=?,
                                          overall_time_played=? 
                                          where player_id=?''',
        (
            games,
            victories,
            defeats,
            overall_time,
            player_id
        ))
        conn.commit()
    except Exception as e:
        print('Database error: ', e)
    return None

def remove_player_resourses(player_id):
    for extension in ALLOWED_EXTENSIONS:
        try:
            os.remove('{}{}.{}'.format(IMAGE_FOLDER, player_id, extension))
        except Exception as e:
            pass
    try:
        os.remove('{}{}.pdf'.format(REPORT_FOLDER, player_id))
    except Exception as e:
        pass

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
IMAGE_FOLDER = 'Images/'
REPORT_FOLDER = 'Reports/'

def add_image_file(player_id, uploaded_file):
    if uploaded_file.filename.split('.')[-1] not in ALLOWED_EXTENSIONS:
        return None
    try:
        remove_player_resourses(player_id)
        uploaded_file.save('{}{}.{}'.format(IMAGE_FOLDER,
                                            player_id,
                                            uploaded_file.filename.split('.')[-1]))
    except exception as e:
        print('Database error: ', e)
        return None
    return jsonify( { 'result': True } )