The project is part of the udacity course and is the final project.
This project simulates a casting agency in which there are movies and actors which are in the movies.

The project has 2 sql tables in the backend. Movies table and actors table. For every movie there are mulitple actors and its a one to many relationship from movies to actors.

## Getting Started

### Installing Dependencies

##### Python 3.7

##### To install all the libraries

```bash
pip install -r requirements.txt
```

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)
- [SQLAlchemy](https://www.sqlalchemy.org/)
- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#)

## Database Setup

This project uses Postgres sql, restore a database using the capstone.psql file provided. From the terminal run:

```bash
psql trivia < trivia.psql
```

## Running the server

To run the server, execute:

```bash
export FLASK_APP=app
flask run --reload
```

## The URL for the project is

https://capstone-casting109.herokuapp.com/

## To login or set up and account the endpoint:

https://dev-9oonecyt.us.auth0.com/authorize?audience=capstone&response_type=token&client_id=1v3ywRRGr7gBReliJsBvnCVN1kUU6r1k&redirect_uri=http://127.0.0.1:5000/movies

The project has three main roles which include casting agent, casting director and executive producer.

## The login information for the three accounts:

### 1. Casting assistant:

```
username : casting@assistant.com
password : casting_123
```

### 2. Casting director:

```
username : casting@director.com
password : casting_123
```

### 3. Casting assistant:

```
username : executive@director.com
password : executive_123
```

## The API endpoints:

### GET '/movies'

- This endpoint fetches all the movies in the database and displays them as json
- Request payload: None
- Returns:

```
[
    {
        "actor": [
            {
                "age": 25,
                "gender": "male",
                "id": 4,
                "movie_id": 2,
                "name": "abc"
            },
            {
                "age": 25,
                "gender": "male",
                "id": 3,
                "movie_id": 2,
                "name": "rohan"
            },
            {
                "age": 25,
                "gender": "male",
                "id": 7,
                "movie_id": 2,
                "name": "abc"
            }
        ],
        "id": 2,
        "title": "something"
    },
    {
        "actor": [
            {
                "age": 25,
                "gender": "male",
                "id": 5,
                "movie_id": 3,
                "name": "abc"
            },
            {
                "age": 25,
                "gender": "male",
                "id": 6,
                "movie_id": 3,
                "name": "abc"
            }
        ],
        "id": 3,
        "title": "first movie"
    },
    {
        "actor": [],
        "id": 5,
        "title": "first movie"
    }
]
```

### GET '/actors'

- This endpoint fetches all the actors in the databse and displays them as json
- Request payload: None
- Returns

```
[
    {
        "age": 25,
        "gender": "male",
        "id": 4,
        "movie_id": 2,
        "name": "abc"
    },
    {
        "age": 25,
        "gender": "male",
        "id": 5,
        "movie_id": 3,
        "name": "abc"
    },
    {
        "age": 25,
        "gender": "male",
        "id": 6,
        "movie_id": 3,
        "name": "abc"
    },
    {
        "age": 25,
        "gender": "male",
        "id": 3,
        "movie_id": 2,
        "name": "rohan"
    },
    {
        "age": 25,
        "gender": "male",
        "id": 7,
        "movie_id": 2,
        "name": "abc"
    }
]
```

### POST '/movies'

- This endpoint will create a new movie in the database based on the json that is in the body of the request
- Request payload: `{"title":"New Movie"}`
- Returns:

```
{
    "movie": {
        "actor": [],
        "id": 6,
        "title": "New Movie"
    },
    "success": true
}
```

### POST '/actors'

- This endpoint will create a new actor in the database based on the json that is in the body of the request
- Request payload: `{"name":"Jhon Cena","gender":"male","age":45,"movie_id":5}`
- Returns

```
{
    "actor": {
        "age": 45,
        "gender": "male",
        "id": 8,
        "movie_id": 5,
        "name": "Jhon Cena"
    },
    "success": true
}
```

### DELETE '/movies/<movie_id>'

- This endpoint will delete the movie that corresponds to the movie ID that is passed into the url
- Request payload: None
- Returns:

```
{
    "message": "Movie deleted",
    "success": true
}

```

### DELETE '/actors/<actor_id>'

- This endpoint will delete the actor that corresponds to the actor ID that is passed into the url
- Request payload: None
- Returns:

```
{
    "message": "Actor deleted",
    "success": true
}
```

### PATCH '/actors/<actor_id>'

- This endpoint will modify the actor that corresponds to the actor ID that is passed into the url based on the json that is passed into the body of the request
- Request payload: `{"name":"some actor","gender":"male","age":25,"movie_id":2}`
- Returns:

```
{
    "message": "update done",
    "success": true
}
```

### PATCH '/movies/<movie_id>'

- This endpoint will modify the movie that corresponds to the movie ID that is passed into the url based on the json that is passed into the body of the request
- Request payload: `{"title":"some title"}`
  -Returns:
  {
  "message": "update done",
  "success": true
  }

## Test

- For the API endpoints tests refer the file `test_app.py`
- For RABC tests I have included 3 import files of the postman collection in the `Postman tests` folder
