import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_migrate import Migrate
from models import setup_db, db, Actor, Movie
from auth import *


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    CORS(app)
    database_path = os.environ['DATABASE_URL']
    setup_db(app, database_path)

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type, Authorization, true')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET, PATCH, POST, DELETE, OPTIONS')
        return response

    @app.route("/authorization/url", methods=["GET"])
    def generate_auth_url():
        url = f'https://{os.environ["AUTH0_DOMAIN"]}/authorize' \
            f'?audience={os.environ["AUTH0_JWT_API_AUDIENCE"]}' \
            f'&response_type=token&client_id=' \
            f'{os.environ["AUTH0_CLIENT_ID"]}&redirect_uri=' \
            f'{os.environ["AUTH0_CALLBACK_URL"]}'

        return jsonify({
            'url': url
        })

    @app.route('/movies', methods=['GET'])
    @requires_auth('get:movies')
    def get_movies(payload):
        movies = Movie.query.all()
        movies = [movie.format() for movie in movies]
        for movie in movies:
            movie['actor'] = [ac.format() for ac in movie['actor']]

        return jsonify(movies), 200

    @app.route('/actors', methods=['GET'])
    @requires_auth('get:actors')
    def get_actors(payload):
        actors = Actor.query.all()
        actors = [actor.format() for actor in actors]
        return jsonify(actors), 200

    @app.route('/movies', methods=['POST'])
    @requires_auth('post:movies')
    def create_movie(payload):
        body = request.get_json()
        title = body.get('title', '')
        if not title:
            abort(422)
        movie = Movie(title=title)
        movie.insert()
        return jsonify({
            'success': True,
            'movie': movie.format()
        }), 201

    @app.route('/actors', methods=['POST'])
    @requires_auth('post:actors')
    def create_actor(payload):
        body = request.get_json()
        name = body.get('name', '')
        age = body.get('age', '')
        gender = body.get('gender', '')
        movie_id = body.get('movie_id', '')
        selection = Movie.query.get(movie_id)
        if selection is None:
            abort(404)
        actor = Actor(name=name, age=age, gender=gender, movie_id=movie_id)
        actor.insert()
        return jsonify({
            'success': True,
            'actor': actor.format()
        }), 201

    @app.route('/movies/<int:id>', methods=['DELETE'])
    @requires_auth('delete:movies')
    def delete_movie(payload, id):
        try:
            Movie.query.get(id).delete()
            return jsonify({
                'success': True,
                'message': 'Movie deleted'
            }), 200
        except:
            abort(404)

    @app.route('/actors/<int:id>', methods=['DELETE'])
    @requires_auth('delete:actors')
    def delete_actor(payload, id):
        try:
            Actor.query.get(id).delete()
            return jsonify({
                'success': True,
                'message': 'Actor deleted'
            }), 200
        except:
            abort(404)

    @app.route('/movies/<int:id>', methods=['PATCH'])
    @requires_auth('patch:movies')
    def update_movie(payload, id):
        movie = Movie.query.get(id)
        if movie is None:
            abort(404)

        body = request.get_json()
        if 'title' in body:
            title = body.get('title', '')
            movie.title = title
        else:
            abort(422)

        movie.update()
        return jsonify({
            'success': True,
            'message': 'update done'
        }), 200

    @app.route('/actors/<int:id>', methods=['PATCH'])
    @requires_auth('patch:actors')
    def update_actor(payload, id):
        actor = Actor.query.get(id)
        if actor is None:
            abort(404)

        body = request.get_json()
        if 'name' in body:
            name = body.get('name')
            actor.name = name
        if 'age' in body:
            age = body.get('age')
            actor.age = age
        if 'gender' in body:
            gender = body.get('gender')
            actor.gender = gender
        if 'movie_id' in body:
            movie_id = body.get('movie_id')
            actor.movie_id = movie_id

        actor.update()
        return jsonify({
            'success': True,
            'message': 'update done'
        }), 200

    @app.errorhandler(404)
    def error_404(error):
        return jsonify({
            'success': False,
            'error': 404,
            'message': 'Resource not Found'
        }), 404

    @app.errorhandler(422)
    def error_422(error):
        return jsonify({
            'success': False,
            'error': 422,
            'message': 'Unprocessable entity'
        }), 422

    @app.errorhandler(AuthError)
    def auth_error(error):
        return jsonify({
            "success": False,
            "error": error.status_code,
            "message": error.error['description']
        }), error.status_code

    @app.errorhandler(500)
    def error_500(error):
        return jsonify({
            'success': False,
            'error': 500,
            'message': 'Server side error'
        }), 500

    return app


app = create_app()

if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)
