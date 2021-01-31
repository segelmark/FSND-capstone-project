import os
from flask import Flask, request, abort, jsonify
from models import setup_db, Therapist
from flask_cors import CORS

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

    @app.route('/')
    def get_greeting():
        excited = os.environ['EXCITED']
        greeting = "Hello" 
        if excited == 'true': greeting = greeting + "!!!!!"
        return greeting

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
            'total_therapists': len(therapists),
            'current_category': None
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