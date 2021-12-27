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
* GET '/therapists/id'
* POST '/therapists'
* DELETE '/therapists/id'
* GET '/bookings'
* GET '/bookings/id'
* POST '/bookings'
* PATCH '/bookings'
* DELETE '/bookings'

#### GET '/therapists'
- Fetches a list of therapists and their data 
- Request Arguments: None
- Returns: An object with key "therapists" containing an array of objects with key "id": Int and "name": String 
```
{
    "therapists": [
        {
            name: "Ally",
            id: 1
        },
        ...
    ],
    "success": true
}
```

### GET '/therapists/{therapist_id}'
- Fetches a list of particular therapist and their data
- Request Arguments:
  - URL Params: Therapist ID as Int
- Returns: An object with key "therapists" containing an array with on object with key "id": Int and "name": String 
```
{
    "therapists": [
        {
            name: "Ally",
            id: 1
        }
    ],
    "success": true
}
```

### POST '/therapists/'
- Creates a new therapist
- Request Arguments:
  - Body: JSON Object containing "name": String
```
{
    "name": "Ally",
}
```

- Returns: Object with "created": Int
```
{
  "success": True,
  "created": therapist_id
}
```

### DELETE '/therapists/{therapist_id}'
- Deletes therapist with therapist_id from database
- Request Arguments:
  - URL Params: Therapist ID as Int
- Returns: Object with "deleted": Int
```
{
  "success": True,
  "deleted": therapist_id
}
...
```

#### GET '/bookings'
- Fetches a list of bookings and their related data 
- Request Arguments: None
- Returns: An object with key "therapists" containing an array of objects with key "id": Int, "therapist_id": Int, "start": datetime, "end": datetime
```
{
    "bookings": [
        {
            id: 1,
            therapist_id: 1,
            start_time: "2016-04-08 11:43:36.309721"
        },
        ...
    ],
    "success": true
}
```

### GET '/bookings/{therapist_id}'

- Fetches a booking and its data 
- Request Arguments:
  - URL Params: Therapist ID as Int
- Returns: An object with key "therapists" containing an array with one object with key "id": Int, "therapist_id": Int, "start": datetime, "end": datetime
```
{
    "bookings": [
        {
            id: 1,
            therapist_id: 1,
            start_time: "2016-04-08 11:43:36.309721"
        }
    ],
    "success": true
}
```
### POST '/bookings/'
- Creates a new booking
- Request Arguments:
  - Body: JSON Object containing "therapist_id": Int, "start": datetime, "end": datetime
```
{
    therapist_id: 1,
    start: 2016-04-08 11:43:36.309721,
    end: 2016-04-08 11:43:36.309721
}
```

- Returns: Object with "created": Int
```
{
  "success": True,
  "created": therapist_id
}
```


### DELETE '/bookings/{booking_id}'
- Deletes booking with booking_id from database
- Request Arguments:
  - URL Params: Booking ID as Int
- Returns: Object with "deleted": Int
```
{
  "success": True,
  "deleted": booking_id
}
...
```

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