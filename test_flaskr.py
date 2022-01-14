import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, Therapist, Booking

AUTH_TOKEN='Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkV0dGFDa0h4dUFXaUI0UlBoejJKTyJ9.eyJpc3MiOiJodHRwczovL3VkYWNpdHktc2VnZWwuZXUuYXV0aDAuY29tLyIsInN1YiI6Imdvb2dsZS1vYXV0aDJ8MTAxMDY1MDU5NTE0MzgxODYwMTQ0IiwiYXVkIjoiZnNuZC1jYXBzdG9uZS5zZWdlbG1hcmsuY29tIiwiaWF0IjoxNjQyMTE4NDcwLCJleHAiOjE2NDIxMjU2NzAsImF6cCI6IkFzWndnQnNmNEd4NFdFY1hwUml1WjVyaWtTYTdlUG1pIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6Ym9va2luZ3MiLCJkZWxldGU6dGhlcmFwaXN0cyIsImdldDpib29raW5ncyIsInBhdGNoOmJvb2tpbmdzIiwicG9zdDpib29raW5ncyIsInBvc3Q6dGhlcmFwaXN0cyJdfQ.SwDREC1Ts-QpxLK1jbzHSTs9rWWTUHUvQCzXYMcnPyEGKVBHnoho7LY8i2knOZN_CiXluLedPN6y3abOfPWXTl3TnmmjFndQOz36jxcANtjpZLPbvf91-5lRkECfDgb6tA44tT-lnL8YZb0mSOY3sgvJ5fsBSq6xCoVH2fFIQX8kFGTuyYvGy2KZ1D8ERUNjBY9f5ueIZ89U8ZCGkdYrScwDwKbP4NqoR9OG9aA67y0h87XKYXFWE5TYEEXQGVprvf7zOL7XL5LB0BusiWs_vR5tPddmsqT907BOHZakAyOh542quhxYpPJd0asn-OLdxZMxgXxeRvozy1w9qHRJKg'
HEADERS={'Authorization': AUTH_TOKEN}

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

        # Example therapist for use in tests
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

        res = self.client().get('/bookings',headers=HEADERS)
        data = json.loads(res.data)

        # Check success
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

        # Check data
        self.assertTrue(data['total_bookings'])
        self.assertTrue(len(data['bookings'])<=data['total_bookings'])

    def test_get_therapists_not_found(self):
        """ Test what happens if we try to look for therapist that doesn't exist """

        res = self.client().get('/therapists/9999',headers=HEADERS)
        data = json.loads(res.data)

        #Check for lack of success with correct error code and message
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource Not Found')

    def test_delete_therapist_page_not_found(self):
        """Test what happens if we try to delete something that doesn't exist"""
        res = self.client().get('/therapists/9999',headers=HEADERS)
        data = json.loads(res.data)

        #Check for lack of success with correct error code and message
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource Not Found')

    def test_create_and_delete_therapist_success(self):
        """ Test successful creation and deletion """

        #Count what is in the database
        therapists_initially = Therapist.query.all()

        res = self.client().post('/therapists', json=self.example_therapist,headers=HEADERS)
        data = json.loads(res.data)

        #Check for successful creation
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['created'])

        therapist_id = data['created']

        #Count again and compare to baseline
        therapists_created = Therapist.query.all()
        self.assertTrue(len(therapists_created)>len(therapists_initially))

        res_delete = self.client().delete('/therapists/'+str(therapist_id),headers=HEADERS)
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

        #Make sure the therapist we deleted doesn't exist
        therapist = Therapist.query.filter(Therapist.id == therapist_id).one_or_none()
        self.assertEqual(therapist, None)

    def test_create_therapist_fields_missing(self):
        res = self.client().post('/therapists', json="", headers=HEADERS)
        data = json.loads(res.data)

        # Check for lack of success with correct error code and message
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unprocessable Entity')



# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()