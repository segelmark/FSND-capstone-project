import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, Therapist, Booking


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "capstone_test"
        self.database_path = "postgres://{}/{}".format('localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

        # Example question for use in tests
        self.example_therapist = {
            'name': 'Tanner'
        }


    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    Tests
    """

    def test_get_therapists_success(self):
        """Test that we get a response when trying to get therapists"""

        res = self.client().get('/therapists')
        data = json.loads(res.data)

        # Check success
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

        # Check data
        self.assertTrue(len(data['therapists']))

    def test_get_bookings_success(self):
        """Test that we get a response when trying to get bookings """

        res = self.client().get('/bookings')
        data = json.loads(res.data)

        # Check success
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

        # Check data
        self.assertTrue(data['total_questions'])
        self.assertTrue(len(data['questions'])<=10)
        self.assertTrue(len(data['questions'])<=data['total_questions'])
        self.assertTrue(len(data['categories']))

    def test_get_therapists_not_found(self):
        """ Test what happens if we try to look for therapist that doesn't exist """

        res = self.client().get('/therapists/9999')
        data = json.loads(res.data)

        #Check for lack of success with correct error code and message
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource Not Found')

    def test_delete_therapist_page_not_found(self):
        """Test what happens if we try to delete something that doesn't exist"""
        res = self.client().get('/therapists/9999')
        data = json.loads(res.data)

        #Check for lack of success with correct error code and message
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource Not Found')

    def test_create_and_delete_therapist_success(self):
        """ Test successful creation and deletion """

        #Count what is in the database
        therapists_initially = Therapist.query.all()

        res = self.client().post('/therapists', json=self.example_therapist)
        data = json.loads(res.data)

        #Check for successful creation
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['created'])

        therapist_id = data['created']

        #Count again and compare to baseline
        therapists_created = Therapist.query.all()
        self.assertTrue(len(therapists_created)>len(therapists_initially))

        res_delete = self.client().delete('/therapists/'+str(therapist_id))
        data_delete = json.loads(res_delete.data)

        #Check for successful deletion
        self.assertEqual(res_delete.status_code, 200)
        self.assertEqual(data_delete['success'], True)

        #Make sure we delete the right thing
        self.assertEqual(data_delete['deleted'], therapist_id)

        #Count again after delete and compare to previous counts
        therapists_deleted = Therapist.query.all()
        self.assertTrue(len(therapists_deleted)<len(therapists_created))
        self.assertTrue(len(therapists_deleted)==len(therapists_initially))

        #Make sure the question we deleted doesn't exist
        question = Therapist.query.filter(Therapist.id == 1).one_or_none()
        self.assertEqual(question, None)

    def test_create_therapist_fields_missing(self):
        res = self.client().post('/therapist', json="")
        data = json.loads(res.data)

        # Check for lack of success with correct error code and message
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unprocessable Entity')



# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()