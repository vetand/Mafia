from python_graphql_client import GraphqlClient

class graphQLClient:
    def __init__(self, address):
        self.client = GraphqlClient(endpoint = address)

    # argument 'players' - array of players nicknames
    # result - ID of this game in GraphQL service
    def send_start_game_message(self, players):
        game_starts_mutation = \
        "mutation game_starts {\n" + \
        "   addGame(players: {})\n".format(players).replace("'", '"') + \
        "}"
        data = self.client.execute(query = game_starts_mutation)
        return data['data']['addGame']

    # arguments 'winners' and 'losers' - arrays of players nicknames
    # returns None
    def send_game_result_message(self, gameID, winners, losers):
        game_result_mutation = \
        "mutation game_complites {\n" + \
        "   addResult(gameID: {}, winners: {}, losers: {})\n".format(gameID,
                                                                     winners,
                                                                     losers).replace("'", '"') + \
        "}" 
        self.client.execute(query = game_result_mutation)

    def ask_single_game(self, gameID):
        game_query_message = \
        "query askAll {\n" + \
        "    game(gameID: {})".format(gameID) + """ {
                id
                winners
                losers
                players
                finished
                comments {
                    author
                    text
                }
            }
        }"""
        return self.client.execute(query = game_query_message)['data']['game']

    def ask_all_games(self, finished = None):
        if finished is None:
            finished_line = ""
        elif finished:
            finished_line = "(finished: true)"
        else:
            finished_line = "(finished: false)"
        games_query_message = \
        "query askAll {\n" + \
        "    games{}".format(finished_line) + """ {
                id
                winners
                losers
                players
                finished
            }
        }"""
        return self.client.execute(query = games_query_message)['data']['games']

    def add_comment_message(self, gameID, text, author):
        add_comment_message = \
        "mutation comment_made {\n" + \
        '    addComment(gameID: {}, comment_text: "{}", comment_author: "{}")\n'.format \
        (
            gameID,
            text,
            author
        ).replace("'", '"') + \
        "}"
        self.client.execute(query = add_comment_message)