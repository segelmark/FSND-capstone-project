import os
from flask import Flask, request, abort, jsonify
from models import setup_db, Therapist, Booking
from flask_cors import CORS
from flask_migrate import Migrate


ENTRIES_PER_PAGE=10

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
    def retrieve_therapist(therapist_id):
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
    def delete_therapist(therapist_id):
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
    def create_therapist():
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
    def retrieve_bookings():
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

    @app.route('/bookings/<int:booking_id>', methods=['DELETE'])
    def delete_booking(booking_id):
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

    @app.route('/bookings', methods=['POST'])
    def create_booking():
        """ Endpoint to POST a new question """
        body = request.get_json()

        # Check that we are getting the required fields
        if not ('therapist_id' in body):
            abort(422)

        therapist = body.get('therapist_id', None)

        booking = Booking(therapist_id=therapist)
        booking.insert()
        return jsonify({
            'success': True,
            'created': booking.id,
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

    return app

app = create_app()

if __name__ == '__main__':
    app.run()