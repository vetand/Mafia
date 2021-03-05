import playerDatabase

import pika
import flask
import json
import subprocess
from flask import Flask, abort, request
from flask_restx import Api, Resource, fields
from werkzeug.datastructures import FileStorage
from reportGenerator import generate_report

import os

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
IMAGE_FOLDER = 'Images/'
REPORT_FOLDER = 'Reports/'

flask_app = Flask(__name__)
flask_app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

api = Api(app = flask_app,
    version='1.0',
    title='Mafia API',
    description='API of Mafia game database')

name_space = api.namespace('mafia', description='Mafia database Operations')

# player requests model
player = api.model('Player', {
    'player_id': fields.Integer(required=False, readonly=True, description='The player id'),
    'name': fields.String(required=True, description='The player`s name'),
    'gender': fields.String(required=True, description='The player`s gender'),
    'email': fields.String(required=True, description='The player`s email')
})

# player response model
playerUrl = api.model('Player URL', {
    'player_url': fields.Url('player_ep', readonly=True, absolute=True, description='URL'),
    'name': fields.String(required=True, description='The player`s name'),
    'gender': fields.String(required=True, description='The player`s gender'),
    'email': fields.String(required=True, description='The player`s email')
})

# player response model, after GET request a report is generated
playerUrlWithReportUrl = api.model('Player URL', {
    'player_url': fields.Url('player_ep', readonly=True, absolute=True, description='URL'),
    'name': fields.String(required=True, description='The player`s name'),
    'report_url': fields.Url('player_report', readonly=True, absolute=True, description='URL'),
    'gender': fields.String(required=True, description='The player`s gender'),
    'email': fields.String(required=True, description='The player`s email')
})

# update statistics request
newStats = api.model('Statistics', {
    'player_id': fields.Integer(required=False, readonly=True, description='The player id'),
    'victory': fields.Boolean(required=True, description='If player won'),
    'time': fields.Integer(required=True, description='Time in seconds')
})

@flask_app.errorhandler(400)
def resource_not_found(e):
    return jsonify(error=str(e)), 400

@name_space.route('/api/v1.0/players/<int:player_id>', endpoint='player_ep')
@name_space.response(404, 'Player not found')
@name_space.param('player_id', 'The player identifier')
class Player(Resource):

    @name_space.doc('get_player')
    @name_space.marshal_with(playerUrlWithReportUrl)
    def get(self, player_id):
        result = playerDatabase.get_player(player_id)
        if result is None:
            return abort(404)
        connection = pika.BlockingConnection(
        pika.ConnectionParameters(host = 'rabbitmq'))
        channel = connection.channel()
        channel.queue_declare(queue = 'report')
        channel.basic_publish(exchange='', routing_key='report', body=str(player_id))
        connection.close()
        return result

    @name_space.doc('update_player')
    @name_space.expect(player, validate=True)
    @name_space.marshal_with(playerUrl)
    def put(self, player_id):
        response = playerDatabase.get_player(player_id)
        if response is None:
            abort(404)
        response = playerDatabase.update_player(player_id,
                                                request.get_json()['name'],
                                                request.get_json()['gender'],
                                                request.get_json()['email'])
        if response is None:
            abort(400)
        return response
    
    @name_space.doc('delete_player')
    @name_space.response(204, 'Player deleted')
    def delete(self, player_id):
        response = playerDatabase.get_player(player_id)
        if response is None:
            abort(404)
        playerDatabase.remove_player(player_id)
        return '', 204

@name_space.route('/api/v1.0/players')
class PlayerList(Resource):
    @name_space.doc('list_players')
    @name_space.marshal_list_with(playerUrl)
    def get(self):
        return playerDatabase.get_all_players()

    @name_space.doc('create_player')
    @name_space.marshal_with(playerUrl, code=201)
    def post(self):
        try:
            body_in_json = request.get_json()
            if str(type(request.get_json())) != "<class 'dict'>":
                body_in_json = json.loads(request.get_json())
        except Exception as e:
            abort(400, description="Invalid file, use JSON format")

        if playerDatabase.name_exists(body_in_json['name']):
            abort(400, description="This name is already taken")
        response = playerDatabase.add_to_list(body_in_json['name'],
                                              body_in_json['gender'],
                                              body_in_json['email'])
        if response is None:
            abort(400)
        return response, 201

upload_parser = api.parser()
upload_parser.add_argument('image', location='files', type=FileStorage, required=True)

@name_space.route('/api/v1.0/players/<int:player_id>/image', endpoint='player_im')
@name_space.expect(upload_parser)
class Upload(Resource):
    @name_space.doc('update_image')
    @name_space.marshal_with(playerUrl)
    def put(self, player_id):
        result = playerDatabase.get_player(player_id)
        if result is None:
            abort(404)
        args = upload_parser.parse_args()
        uploaded_file = args['image']

        file_saved = playerDatabase.add_image_file(player_id, uploaded_file)
        if file_saved is None:
            abort(400, description="Incorrect file format")
        return result

@name_space.route('/api/v1.0/players/<int:player_id>/report', endpoint='player_report')
class Reporter(Resource):
    @name_space.doc('get_report')
    def get(self, player_id):
        result = playerDatabase.get_player(player_id)
        if result is None:
            abort(404)
        try:
            response = flask.send_from_directory(REPORT_FOLDER,
                str(player_id) + ".pdf", as_attachment = False)
            return response 
        except Exception as e:
            print(e)
            abort(400, description="""Wait a bit, the report is not ready yet.
                                      Don`t forget to order it via GET player_id
                                   """)

@name_space.route('/api/v1.0/players/<int:player_id>/stats', endpoint='player_stats')
class Statistcs(Resource):
    @name_space.doc('increment_statistics')
    def put(self, player_id):
        try:
            body_in_json = request.get_json()
            if str(type(request.get_json())) != "<class 'dict'>":
                body_in_json = json.loads(request.get_json())
        except Exception as e:
            print(e)
            abort(400, description="Invalid file, use JSON format")
        result = playerDatabase.get_player(player_id)
        if result is None:
            abort(404)
        playerDatabase.update_game_statistics(
            player_id, 
            body_in_json['victory'],
            body_in_json['time'])

if __name__ == "__main__":
    subprocess.Popen(['python3', 'reportGenerator.py'])
    flask_app.run(host='0.0.0.0',debug = True)