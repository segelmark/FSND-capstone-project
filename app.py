import os
from flask import Flask, request, abort, jsonify, redirect
from models import setup_db, Therapist, Booking
from flask_cors import CORS
from flask_migrate import Migrate

from auth import AuthError, requires_auth, API_AUDIENCE, AUTH0_DOMAIN


ENTRIES_PER_PAGE=10
CLIENT_ID='AsZwgBsf4Gx4WEcXpRiuZ5rikSa7ePmi'

def paginate(entries,page,entries_per_page):
  """Paginates all entries returning the right page for a certain entries per page """
  start =  (page - 1) * entries_per_page
  end = start + entries_per_page
  return entries[start:end]

def format_entries(entries):
  """Formats categories correctly"""
  return [entry.format() for entry in entries]

def paginate_therapists(request, selection):
  """paginates a selecation for the right number of pages given by the get request argument """
  page = request.args.get('page', 1, type=int)
  entries = format_entries(selection)
  return paginate(entries,page,ENTRIES_PER_PAGE)

def create_app(test_config=None):

    app = Flask(__name__)
    setup_db(app)

    CORS(app, resources={r"/*": {"origins": "*"}})
 
    # CORS Headers - Setting access control allow
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
        return response
 
    @app.route('/')
    def get_greeting():
        return "lol"

    @app.route('/login')
    def login():
        return redirect('https://' + AUTH0_DOMAIN + '/authorize?audience=' + API_AUDIENCE + '&response_type=token&client_id=' + CLIENT_ID + '&redirect_uri=' + request.host_url + 'login-results')

    # Here we're using the /callback route.
    @app.route('/login-results')
    def callback_handling():
        return "Logged in"

    @app.route('/logout')
    def logout():
        return redirect('https://' + AUTH0_DOMAIN + '/v2/logout?audience=' + API_AUDIENCE + '&client_id=' + CLIENT_ID + '&returnTo=' + request.host_url + 'logout-results')

    @app.route('/logout-results')
    def loggedout():
        return "Logged in"

    @app.route('/therapists')
    def retrieve_therapists():
        """ Endpoint to handle GET requests for all questions paginated (10 questions) """
        try:
            therapists = Therapist.query.order_by(Therapist.id).all()
        except:
            abort(422)
        
        # Paginate list of therapists and make sure it is a valid page
        therapists_paginated = paginate_therapists(request, therapists)
        if not therapists_paginated:
             abort(404)

        return jsonify({
            'success': True,
            'therapists': therapists_paginated,
            'total_therapists': len(therapists)
        })
        
    @app.route('/therapists/<int:therapist_id>')
    @requires_auth('get:bookings')
    def retrieve_therapist(payload,therapist_id):
        """ Endpoint to handle GET requests for all questions paginated (10 questions) """
        try:
            therapist = Therapist.query.get(therapist_id)
        except:
            abort(422)
        
        if not therapist:
             abort(404)

        return jsonify({
            'success': True,
            'name': therapist.name,
            'id': therapist.id,
            'bookings': format_entries(therapist.bookings)
        })

    @app.route('/therapists/<int:therapist_id>', methods=['DELETE'])
    @requires_auth('delete:therapists')
    def delete_therapist(payload,therapist_id):
        """ Endpoint to DELETE therapist using it's ID. """
        try:
            therapist = Therapist.query.get(therapist_id)
        except:
            abort(422)
        #Make sure the therapist we want to delete exists
        if not therapist:
            abort(404)
        try:
            therapist.delete()
        except:
            abort(422)
        return jsonify({
            'success': True,
            'deleted': therapist_id
        })

    @app.route('/therapists', methods=['POST'])
    @requires_auth('post:therapists')
    def create_therapist(payload):
        """ Endpoint to POST a new question """
        body = request.get_json()

        # Check that we are getting the required fields
        if not ('name' in body):
            abort(422)

        new_name = body.get('name', None)

        try:
            therapist = Therapist(name=new_name)
            therapist.insert()
            return jsonify({
                'success': True,
                'created': therapist.id,
            })
        except:
            abort(422)     

    @app.route('/bookings')
    @requires_auth('get:bookings')
    def retrieve_bookings(payload):
        """ Endpoint to handle GET requests for all questions paginated (10 questions) """
        try:
            bookings = Booking.query.order_by(Booking.id).all()
        except:
            abort(422)
        
        # Paginate list of bookings and make sure it is a valid page
        bookings_paginated = paginate_therapists(request, bookings)
        if not bookings_paginated:
             abort(404)

        return jsonify({
            'success': True,
            'bookings': bookings_paginated,
            'total_bookings': len(bookings)
        })

    @app.route('/bookings/<int:booking_id>')
    @requires_auth('get:bookings')
    def retrieve_booking(payload,booking_id):
        """ Endpoint to handle GET requests for all questions paginated (10 questions) """
        try:
            booking = Booking.query.get(booking_id)
        except:
            abort(422)
        
        # Make sure it found a booking
        if not booking:
             abort(404)

        return jsonify({
            'success': True,
            'id': booking.id,
            'start_time': booking.start_time,
            'therapist_id': booking.therapist_id
        })

    @app.route('/bookings', methods=['POST'])
    @requires_auth('post:bookings')
    def create_booking(payload):
        """ Endpoint to POST a new booking """
        body = request.get_json()

        # Check that we are getting the required fields
        if not ('therapist_id' in body):
            abort(422)

        therapist = body.get('therapist_id', None)

        booking = Booking(therapist_id=therapist)
        try:
            booking.insert()
        except:
            abort(422)
        return jsonify({
            'success': True,
            'created': booking.id,
        })

    @app.route('/bookings/<int:booking_id>', methods=['PATCH'])
    @requires_auth('patch:bookings')
    def change_booking(payload,booking_id):
        """ Endpoint to PATCH an existing booking """
        body = request.get_json()
        
        # Check that we are getting the required fields
        if not (body):
            abort(422)

        try:
            booking = Booking.query.get(booking_id)
        except:
            abort(422)

        if not (booking):
            abort(404)

        if 'therapist_id' in body:
            booking.therapist_id = body.get('therapist_id', None)
        try:
            booking.update()
        except:
            abort(422)
        return jsonify({
            'success': True,
            'id': booking.id,
            'start_time': booking.start_time,
            'therapist_id': booking.therapist_id
        })
  
    @app.route('/bookings/<int:booking_id>', methods=['DELETE'])
    @requires_auth('delete:bookings')
    def delete_booking(payload,booking_id):
        """ Endpoint to DELETE booking using it's ID. """
        try:
            booking = Booking.query.get(booking_id)
        except:
            abort(422)
        #Make sure the booking we want to delete exists
        if not booking:
            abort(404)
        try:
            booking.delete()
        except:
            abort(422)
        return jsonify({
            'success': True,
            'deleted': booking_id
        })


    #Error handlers for all expected errors 

    @app.errorhandler(400)
    def error_bad_request(error):
        return jsonify({
        "success": False,
        "error": 400,
        "message": "Bad Request"
        }), 400

    @app.errorhandler(404)
    def error_not_found(error):
        return jsonify({
        "success": False,
        "error": 404,
        "message": "Resource Not Found"
        }), 404

    @app.errorhandler(422)
    def error_unprocessable(error):
        return jsonify({
        "success": False,
        "error": 422,
        "message": "Unprocessable Entity"
        }), 422

    @app.errorhandler(AuthError)
    def auth_error(error):
        return jsonify({
            "success": False,
            "error": error.status_code,
            "message": error.error['description']
        }), error.status_code

    return app

app = create_app()

if __name__ == '__main__':
    app.run()