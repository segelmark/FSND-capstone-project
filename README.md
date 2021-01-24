# FSND-capstone-project
Udacity Fullstack Developer Nanodegree Capstone Project combining all of the concepts and the skills taught in the courses to build an API from start to finish and host it

## Project assignment
* Models includes at least…
    * Two classes with primary keys at at least two attributes each
    * One-to-many or many-to-many relationships between classes
* Endpoints includes at least…
    * Two GET requests
    * One POST request
    * One PATCH request
    * One DELETE request
* Roles includes at least…
    * Two roles with different permissions
    * Permissions specified for all endpoints
* Tests includes at least…
    * One test for success behavior of each endpoint
    * One test for error behavior of each endpoint
    * At least two tests of RBAC for each role

## Local Development Setup

### Setup virtual environment
To create a virtual environment, run the venv module as a script in the FSND-Capstone-Project directory:
```
python3 -m venv venv
```

Once you’ve created the virtual environment, activate it.
```
. venv/bin/activate
```

### Install dependencies
Use pip to install the required dependencies.
```
pip install -r requirements.txt
```

### Run the server
Start the server using the FLASK development server:
```
export FLASK_APP=myapp
export FLASK_ENV=development # enables debug mode
python3 app.py
```

### Open browser
Navigate to project homepage [http://localhost:5000](http://localhost:5000) 

## API Documentation
This describes the resources available through the Dolphin Therapy API, which allows for easy integration of the booking capaibilities into any web or mobile application.

### Endpoints (to be implemented)
* GET '/therapists'
* POST '/therapists'
* PATCH '/therapists'
* DELETE '/therapists'
* GET '/bookings'
* POST '/bookings'
* PATCH '/bookings'
* DELETE '/bookings'
* GET '/patients'
* POST '/patients'
* PATCH '/patients'
* DELETE '/patients'

#### GET '/therapists' (to be implemented)
- Fetches a list of therapists and their availability 
- Request Arguments: None
- Returns: An object with key "therapists" containing an array of objects with key "id": Int and "name": String 
```
{
    "therapists": [
        {
            name: "Tammy",
            id: 1
        },
        ...
    ],
    "success": true
}
```

...

(to be defined)

### Status Codes

Trivia API returns the following status codes in its API:

| Status Code | Description |
| :--- | :--- |
| 200 | `Success` |
| 400 | `Bad Request` |
| 404 | `Resource Not Found` |
| 422 | `Unprocessable Entity` |
 
For all status codes a JSON object is included with a "success": Boolean and the correct data or error code and message.

```
{
  "error": 404, 
  "message": "Resource Not Found", 
  "success": false
}
```