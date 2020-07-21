import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from models import Actor, Movie, setup_db
from app import create_app

movie_id = 2
actor_id = 2


def set_auth_header(role):
    if role == 'assistant':
        return {'Authorization': 'Bearer {}'.format(os.getenv(casting_assistant))}
    elif role == 'director':
        return {'Authorization': 'Bearer {}'.format(os.getenv(casting_director))}
    elif role == 'producer':
        return {'Authorization': 'Bearer {}'.format(os.getenv(executive_producer))}


class CastingTestCase(unittest.TestCase):

    def setUp(self):
        '''define test variables and initialize app'''

        self.app = create_app()
        self.client = self.app.test_client
        self.database_path = os.environ['DATABASE_URL_TEST']
        setup_db(self.app, self.database_path)

        self.test_movie = {
            'title': 'first Movie',
        }

        self.test_actor = {
            'name': 'ABC',
            'age': 25,
            'gender': 'Male',
            'movie_id': 1
        }

        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            self.db.drop_all()
            self.db.create_all()

    def tearDown(self):
        pass

    # 1. get all the movies
    def test_get_movies_assistant(self):
        res = self.client().get('/movies', headers=set_auth_header('assistant'))
        self.assertEqual(res.status_code, 200)

    # 2. Authorization fail to get all movies
    def test_get_movies_fail_no_auth(self):
        res = self.client().get('/movies')
        self.assertEqual(res.status_code, 401)

    # 3. get all the actors
    def test_get_actors_assitant(self):
        res = self.client().get('/actors', headers=set_auth_header('assistant'))
        self.assertEqual(res.status_code, 200)

    # 4. Auth Fail to get all the actors
    def test_fail_get_actors_no_auth(self):
        res = self.client().get('/actors')
        self.assertEqual(res.status_code, 401)

    # 5. create a movie
    def test_create_movies_producer(self):
        res = self.client().post(
            '/movies', headers=set_auth_header('producer'), json=self.test_movie)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 201)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['movie']['title'], 'first Movie')

    # 6. create a movie fail
    def test_fail_create_movie_producer(self):
        test_mo = {
            'title': '',
        }
        res = self.client().post('/movies', headers=set_auth_header('producer'), json=test_mo)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)

    # 7. create a actor
    def test_create_actors_director(self):
        res = self.client().post(
            '/actors', headers=set_auth_header('director'), json=self.test_actor)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 201)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['actor']['name'], 'ABC')

    # 8. fail create actor
    def test_create_actors_fail_director(self):
        test = self.test_actor
        test['movie_id'] = 1000
        res = self.client().post('/actors', headers=set_auth_header('director'), json=test)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    # 9
    def test_update_movie_director(self):
        res = self.client().patch(
            '/movies/1', headers=set_auth_header('director'), json=self.test_movie)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    # 10
    def test_update_movie_fail_director(self):
        res = self.client().patch(
            '/movies/1', headers=set_auth_header('director'), json={'name': 'some'})
        self.assertEqual(res.status_code, 422)

    # 11
    def test_update_actor_producer(self):
        res = self.client().patch(
            '/actors/1', headers=set_auth_header('producer'), json=self.test_actor)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    # 12
    def test_update_actor_fail_producer(self):
        res = self.client().patch(
            '/actors/2000', headers=set_auth_header('producer'), json=self.test_actor)
        self.assertEqual(res.status_code, 404)

    # 13
    def test_delete_actor_director(self):
        res = self.client().delete('/actors/3', headers=set_auth_header('director'))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    # 14
    def test_delete_movie_producer(self):
        res = self.client().delete('/movies/3', headers=set_auth_header('producer'))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    # 15
    def test_fail_delete_movie_producer(self):
        res = self.client().delete('/movies/1000', headers=set_auth_header('producer'))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    # 16
    def test_fail_delete_actor_director(self):
        res = self.client().delete('/actors/1000', headers=set_auth_header('director'))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    # 17 casting agent test create actor fail
    def test_fail_create_actors_auth_assistant(self):
        res = self.client().post(
            '/actors', headers=set_auth_header('assistant'), json=self.test_actor)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)

    # 18 casting agent delete a movie fail
    def test_fail_auth_delete_movie_assistant(self):
        res = self.client().delete('/movies/1', headers=set_auth_header('assistant'))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)

    # 19. Executive producer fails to create a actor
    def test_fail_create_actors_auth_producer(self):
        res = self.client().post(
            '/actors', headers=set_auth_header('producer'), json=self.test_actor)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)

    # 20 producer fails to delete a actor
    def test_fail_delete_actor_auth_producer(self):
        res = self.client().delete('/actors/3', headers=set_auth_header('producer'))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)

    # 21 director fails to create movie
    def test_fail_create_movies_auth_director(self):
        res = self.client().post(
            '/movies', headers=set_auth_header('director'), json=self.test_movie)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)

    # 22 director fails to delete a movie
    def test_fail_delete_movie_auth_director(self):
        res = self.client().delete('/movies/3', headers=set_auth_header('director'))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)


if __name__ == "__main__":
    unittest.main()
