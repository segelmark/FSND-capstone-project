import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, Therapist, Booking

print("Enter an admin authentication token;")
admin_token='Bearer ' + input()
admin_headers={'Authorization': admin_token}

print("Enter a therapist authentication token;")
therapist_token='Bearer ' + input()
therapist_headers={'Authorization': therapist_token}

class BookingTestCase(unittest.TestCase):
    """This class represents the booking test case"""

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

    def test_get_bookings_unauthenticated(self):
        """ Test to see that we cannot access bookings page unauthenticated"""
        res = self.client().get('/bookings')
        self.assertEqual(res.status_code, 401)

    def test_get_bookings_success(self):
        """Test that we get a response when trying to get bookings """

        res = self.client().get('/bookings',headers=therapist_headers)
        data = json.loads(res.data)

        # Check success
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

        # Check data
        self.assertTrue(data['total_bookings'])
        self.assertTrue(len(data['bookings'])<=data['total_bookings'])

    def test_get_therapists_not_found(self):
        """ Test what happens if we try to look for therapist that doesn't exist """

        res = self.client().get('/therapists/9999',headers=admin_headers)
        data = json.loads(res.data)

        #Check for lack of success with correct error code and message
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource Not Found')

    def test_delete_therapist_page_not_found(self):
        """Test what happens if we try to delete something that doesn't exist"""
        res = self.client().get('/therapists/9999',headers=admin_headers)
        data = json.loads(res.data)

        #Check for lack of success with correct error code and message
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource Not Found')

    def test_create_and_delete_therapist_success(self):
        """ Test successful creation and deletion """

        #Count what is in the database
        therapists_initially = Therapist.query.all()

        res = self.client().post('/therapists', json=self.example_therapist,headers=admin_headers)
        data = json.loads(res.data)

        #Check for successful creation
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['created'])

        therapist_id = data['created']

        #Count again and compare to baseline
        therapists_created = Therapist.query.all()
        self.assertTrue(len(therapists_created)>len(therapists_initially))

        res_delete = self.client().delete('/therapists/'+str(therapist_id),headers=admin_headers)
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
        res = self.client().post('/therapists', json="", headers=admin_headers)
        data = json.loads(res.data)

        # Check for lack of success with correct error code and message
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unprocessable Entity')

    def test_create_and_delete_booking_success(self):
        """ Test successful booking workflow """

        # We need a new therapist
        res = self.client().post('/therapists', json=self.example_therapist,headers=admin_headers)
        data = json.loads(res.data)

        #Check for successful creation
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['created'])

        therapist_id = data['created']

        #Count how many bookings are in the database
        bookings_initially = Booking.query.all()
        
        example_booking = {
                    'therapist_id': therapist_id
        }
        res = self.client().post('/bookings', json=example_booking,headers=therapist_headers)
        data = json.loads(res.data)

        #Check for successful creation
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['created'])

        booking_id = data['created']

        #Count again and compare to baseline
        bookings_created = Booking.query.all()
        self.assertTrue(len(bookings_created)>len(bookings_initially))

        res_delete = self.client().delete('/bookings/'+str(booking_id),headers=therapist_headers)
        data_delete = json.loads(res_delete.data)

        #Check for successful deletion
        self.assertEqual(res_delete.status_code, 200)
        self.assertEqual(data_delete['success'], True)

        #Make sure we delete the right thing
        self.assertEqual(data_delete['deleted'], booking_id)

        #Count again after delete and compare to previous counts
        bookings_deleted = Booking.query.all()
        self.assertTrue(len(bookings_deleted)<len(bookings_created))
        self.assertTrue(len(bookings_deleted)==len(bookings_initially))

        #Make sure the therapist we deleted doesn't exist
        therapist = Booking.query.filter(Booking.id == booking_id).one_or_none()
        self.assertEqual(therapist, None)

    def test_get_bookings_unauthenticated(self):
        """ Test to see that we cannot delete bookings when unauthenticated"""
        res = self.client().delete('/bookings/'+str(1))
        self.assertEqual(res.status_code, 401)

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()