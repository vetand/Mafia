from graphQLClient import graphQLClient as GameInfoClient
import sys
import json
import time

client = GameInfoClient("http://54.237.97.163:8000/")

args = sys.argv
if len(args) < 2:
    print("No arguments! Need at least one")
    exit(1)

if args[1] == "list-all-games":
    data = client.ask_all_games()
    for game in data:
        print("ID = {}, finished = {}, players = {}".format(
            game['id'], 
            game['finished'],
            game['players']))
elif args[1] == "track-game":
    try:
        game = client.ask_single_game(int(args[2]))
        print("ID = {}, finished = {}\nplayers = {}\nwinners = {}\nlosers = {}\ncomments={}".format
        (
                game['id'], 
                game['finished'],
                game['players'],
                game['winners'],
                game['losers'],
                game['comments']
        ))
    except Exception as e:
        print("Invalid second argument, should be valid integer (game ID)")
elif args[1] == "add-comment":
    try:
        name = input("Enter your nickname: ")
        text = input("Enter comment text: ")
        client.add_comment_message(args[2], text, name)
    except Exception as e:
        print("Invalid second argument, should be valid integer (game ID)")
else:
    print("Invadid command...")
