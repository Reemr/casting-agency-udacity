
import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, Movie, Actor


class CastingTestCase(unittest.TestCase):
    """This class represents the casting test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client 
        self.database_name = "casting_test"
        self.database_path = os.environ['DATABASE_URL_TEST']
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

        ####
        # dummy data for testing
        ####

        self.idd = Movie.query.order_by(Movie.id.desc()).first().id
        self.idd2 = 1
        self.idd3 = 5

        self.empty_dt = {
        }

        self.new_movie = {
            "title": "A beautiful Mind",
            "release_date": "2001"
        }
        self.new_actor = {
            "name": "Scarlett Johansson",
            "age": 36,
            "gender": "Female"
        }
        self.update_movie = {
            "title": "The Gentelmen",
            "release_date": "2019"
        }
        self.update_actor = {
            "name": "Tom Cruise",
            "age": 50,
            "gender": "Male"
        }       
        self.castingAssistant_header = {
            'Authorization': 'Bearer ' + str(os.getenv('TOKEN1'))
            }
        self.castingDirector_header = {
            'Authorization': 'Bearer ' + str(os.getenv('TOKEN2'))
        }
        self.executiveProducer_header = {
            'Authorization': 'Bearer ' + str(os.getenv('TOKEN3'))
        }
    
    def tearDown(self):
        """Executed after reach test"""
        pass


    """
    POST TESTS for Movie and Actor
    """
    
    def test_create_movie(self):
        res = self.client().post('/movies', json=self.new_movie, headers=self.executiveProducer_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['movie']))

    def test_create_actor(self):
        res = self.client().post('/actors', json=self.new_actor, headers=self.executiveProducer_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['actor']))

    def test_bad_create_actor(self):
        res = self.client().post('/actors', json=self.empty_dt, headers=self.executiveProducer_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable') 


    def test_bad_create_movie(self):
        res = self.client().post('/movies', json=self.empty_dt, headers=self.executiveProducer_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')
         

    """
    GET TESTS for Movie and Actor

    """
    
    def test_get_movie(self):
        res = self.client().get('/movies', headers=self.castingAssistant_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['movies']))

    def test_get_actor(self):
        res = self.client().get('/actors', headers=self.castingAssistant_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['actors']))

    """
    DELETE TESTS for Movie and Actor
    """
    def test_delete_movie(self):
        res = self.client().delete('/movies/{}'.format(self.idd), headers=self.executiveProducer_header)
        data = json.loads(res.data)

        movie = Movie.query.filter(Movie.id == self.idd).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['delete'], self.idd)
        self.assertEqual(movie, None)    

    def test_delete_movie_not_found(self):
        res = self.client().delete('/movies/{}'.format(self.idd2), headers=self.executiveProducer_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_delete_actor(self):
        res = self.client().delete('/actors/{}'.format(self.idd), headers=self.executiveProducer_header)
        data = json.loads(res.data)

        actor = Actor.query.filter(Actor.id == self.idd).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['delete'], self.idd)
        self.assertEqual(actor, None)    

    def test_delete_actor_not_found(self):
        res = self.client().delete('/movies/{}'.format(self.idd2), headers=self.executiveProducer_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    """
    PATCH TESTS for Movie and Actor
    """
    def test_update_movie(self):
        res = self.client().patch('/movies/{}'.format(self.idd3), json=self.update_movie, headers=self.executiveProducer_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['movies']))

    def test_update_actor(self):
        res = self.client().patch('/actors/{}'.format(self.idd3), json=self.update_actor, headers=self.executiveProducer_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['actors']))

    def test_update_movie_not_found(self):
        res = self.client().patch('/movies/{}'.format(self.idd2), json=self.update_movie, headers=self.executiveProducer_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')  

    def test_update_actor_not_found(self):
        res = self.client().patch('/actors/{}'.format(self.idd2), json=self.update_actor, headers=self.executiveProducer_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')
    
    """
    RBAC TESTS
    """
    def test_unauthorized_create_movie(self):
        res = self.client().post('/movies', json=self.new_movie, headers=self.castingDirector_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'invalid_permission')

    def test_unauthorized_create_actor(self):
        res = self.client().post('/movies', json=self.new_actor, headers=self.castingAssistant_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'invalid_permission') 

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()