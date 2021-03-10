from graphQLClient import graphQLClient as GameInfoClient
import sys

client = GameInfoClient("http://127.0.0.1:8000/")

args = sys.argv
if len(args) < 2:
    print("No arguments! Need at least one")
    exit(1)

if args[1] == "list-all-games":
    data = client.ask_all_games()
    print(data)
