from ariadne import ObjectType, QueryType, gql, make_executable_schema, MutationType
from ariadne.asgi import GraphQL

type_defs = """
    type Query {
        games(finished: Boolean): [Game!]

        game(gameID: Int!): Game
    }

    type Game {
        id: Int!
        finished: Boolean!
        players: [String!]!
        winners: [String!]!
        losers: [String!]!
        comments: [Comment!]!
    }

    type Comment {
        text: String!
        author: String!
    }

    type Mutation {
        addGame(players: [String!]): Int!
        
        addResult(gameID: Int!, winners: [String!], losers: [String!]): Boolean

        addComment(gameID: Int!, comment_text: String!, comment_author: String!): Boolean
    }
"""

# in-memory database to save some time
class Database:
    def __init__(self):
        self.current_gameID_ = 0
        self.current_commentID = 0

        self.games_ = dict()
        self.finished_ = False

    def add_game(self, players):
        gameID = self.current_gameID_
        self.current_gameID_ += 1
        self.games_[gameID] = {'players': players,
                               'finished': False,
                               'winners': [],
                               'losers': [],
                               'comments': []}
        return gameID

    def add_result(self, gameID, winners, losers):
        self.games_[gameID]['finished'] = True
        self.games_[gameID]['winners'] = winners
        self.games_[gameID]['losers'] = losers

    def add_comment(self, gameID, comment_text, comment_author):
        self.games_[gameID]['comments'].append(
            {
                'text': comment_text,
                'author': comment_author
            })

    def get_all_games(self, finished, id):
        if not id is None:
            return {'id': id,
                'finished': self.games_[id]['finished'],
                'players': self.games_[id]['players'],
                'winners': self.games_[id]['winners'],
                'losers': self.games_[id]['losers'],
                'comments': self.games_[id]['comments']
            }
        result = []
        for game in self.games_:
            if not finished is None and self.games_[game]['finished'] != finished:
                continue
            result.append({'id': game,
                'finished': self.games_[game]['finished'],
                'players': self.games_[game]['players'],
                'winners': self.games_[game]['winners'],
                'losers': self.games_[game]['losers'],
                'comments': self.games_[game]['comments']
            })
        return result

database = Database()
mutation = MutationType()

@mutation.field("addGame")
def resolve_addGame(_, info, players):
    return database.add_game(players)

@mutation.field("addResult")
def resolve_addResult(_, info, gameID, winners, losers):
    database.add_result(gameID, winners, losers)

@mutation.field("addComment")
def resolve_addComment(_, info, gameID, comment_text, comment_author):
    database.add_comment(gameID, comment_text, comment_author)

query = ObjectType("Query")
@query.field("games")
def resolve_games(*_, finished = None):
    return database.get_all_games(finished, None)

@query.field("game")
def resolve_game(*_, gameID):
    return database.get_all_games(None, gameID)

schema = make_executable_schema(type_defs, mutation, query)
app = GraphQL(schema, debug=True)