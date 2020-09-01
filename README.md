# Casting Agency Capstone Project
This a project for the Udacity Full Stacke Developer Nanodegree. The project shows a working API for the backend part of a Casting Agency. 
## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

## Setting up environment variables
To set up environment variable to be used by the scripts. run the following (You need to change the DATABASE_URL and DATABASE_TEST_URL to mtch your path):
```
source setup.sh
```
The file contains the tokens needed for accessing the endpoints.

## Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
python3 manage.py db init
python3 manage.py db migrate
python3 manage.py db upgrade
```

## Running the server

To run the server, execute:

```bash
export FLASK_APP=app.py
export FLASK_ENV=development
python3 app.py
```

## Endpoints Documentation

```

Endpoints
GET '/movies'
GET '/actors'
POST '/movies'
POST '/actors'
PATCH '/movies/<id>'
PATCH '/actors/<id>'
DELETE '/movies/<id>'
DELETE '/movies/<id>'

GET '/movies'
- Fetches a list of movies when running (curl http://127.0.0.1:8080/actors -H "Authorization: Bearer <ACCESS_TOKEN>")
- Request Arguments: Header with authorization of Casting Assitant or higher
- Returns: success status and list of movies 
{
    'success': True,
    'movies':[{
        'title': 'The Gentelment',
        'release_date': '2019'
    }]
    }

GET '/actors'
- Fetches a list of movies when running (curl http://127.0.0.1:8080/actors -H "Authorization: Bearer <ACCESS_TOKEN>")
- Request Arguments: Header with authorization of Casting Assitant or higher, and data sent as json.
- Returns: success status and list of actors 
{
    'success': True,
    'movies':[{
        'title': 'Tom Cruise',
        'age': 50,
        'gender': 'Male'
    }]
    }

POST '/movies'
- create a movie when running (curl -X POST http://127.0.0.1:8080/movies -H "Authorization: Bearer <ACCESS_TOKEN>" -d '{"title":"Avatar","release_date":"2009"}')
- Request Arguments: Header with authorization of Executive Producer, and data sent as json.
- Returns: success status and list of movies 
{
    'success': True,
    'movies':[{
        'title': 'The Gentelment',
        'release_date': '2019'
    },
    {
        'title': 'Avatar',
        'release_date': '2009'
    }]
    }

POST '/actors'
- create an actor when running (curl -X POST http://127.0.0.1:8080/acotrss -H "Authorization: Bearer <ACCESS_TOKEN>" -d '{"name":"Sarah Parker","age":40,"gender":"Female"}')
- Request Arguments: Header with authorization of Casting Director or Higher, and data sent as json.
- Returns: success status and list of actors 
{
    'success': True,
    'actors':[{
        'name': 'Tom Cruise',
        'age': 50,
        'gender': 'Male'
    },
    {
        'name': 'Sarah Parker',
        'age': 40,
        'gender': 'Female'
    }]
    }

PATCH '/movies/<id>'
- update a movie when running (curl -X PATCH http://127.0.0.1:8080/movies/<id> -H "Authorization: Bearer <ACCESS_TOKEN>" -d '{"title":"Avatar","release_date":"2001"}')
- Request Arguments: Header with authorization of Casting Director or higher, and data sent as json.
- Returns: success status and list of movies 
{
    'success': True,
    'movies':[{
        'title': 'The Gentelment',
        'release_date': '2019'
    },
    {
        'title': 'Avatar',
        'release_date': '2001'
    }]
    }

PATCH '/actors/<id>'
- update an actor when running (curl -X PATCH http://127.0.0.1:8080/acotrss/<id> -H "Authorization: Bearer <ACCESS_TOKEN>" -d '{"name":"Sarah Parker","age":45,"gender":"Female"}')
- Request Arguments: Header with authorization of Casting Director or higher, and data sent as json.
- Returns: success status and list of actors 
{
    'success': True,
    'actors':[{
        'name': 'Tom Cruise',
        'age': 50,
        'gender': 'Male'
    },
    {
        'name': 'Sarah Parker',
        'age': 45,
        'gender': 'Female'
    }]
    }

DELETE '/movies/<id>'
- delete a movie when running (curl -X DELETE http://127.0.0.1:8080/movies/<id> -H "Authorization: Bearer <ACCESS_TOKEN>")
- Request Arguments: Header with authorization of Executive Producer.
- Returns: success status and id of movie deleted 
{
    'success': True,
    'delete': <id>
    }

DELETE '/actors/<id>'
- delete an actor when running (curl -X DELETE http://127.0.0.1:8080/acotrss/<id> -H "Authorization: Bearer <ACCESS_TOKEN>")
- Request Arguments: Header with authorization of Casting Director or higher.
- Returns: success status and id of actor deleted
{
    'success': True,
    'delete':<id>
    }

```
## Roles:
- Casting Assistant `TOKEN1` in `setup.sh`
    - Can view actors and movies
- Casting Director `TOKEN2` un `setup.sh`
    - All permissions a Casting Assistant has and…
    - Add or delete an actor from the database
    - Modify actors or movies
- Executive Producer `TOKEN3` in `setup.sh`
    - All permissions a Casting Director has and…
    - Add or delete a movie from the database

## Testing
To run the tests, run
```
createdb casting_test
psql casting_test < casting_dump
python3 test_app.py
```
You can modify dummy data in the `test_app.py`

## Heroku
The app is hosted on heroku server [link](https://casting-app-udacity.herokuapp.com/). Included Postman collection to test the app on heroku. Can update the tokens (if its expired) from the setup file.