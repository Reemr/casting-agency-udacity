import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import setup_db, Movie, Actor
from auth import AuthError, requires_auth

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  CORS(app)

  '''
  GET movies list
  '''
  @app.route('/movies')
  @requires_auth('get:movies')
  def get_movies():
    try:
      selection = Movie.query.order_by(Movie.id).all()
      movies = [movie.format() for movie in selection]

      return jsonify({
        'success': True,
        'movies': movies
        })
    except:
        abort(422)
  '''
  GET movies list
  '''
  @app.route('/actors')
  @requires_auth('get:actors')
  def get_actors():
    try:
      selection = Actor.query.order_by(Actor.id).all()
      actors = [actor.format() for actor in selection]

      return jsonify({
        'success': True,
        'actors': actors
        })
    except:
        abort(422)
  
  '''
  DELETE movie
  '''
  @app.route('/movies/<int:id>', methods=['DELETE'])
  @requires_auth('delete:movie')
  def delete_movie(id):
    movie = Movie.query.filter(Movie.id == id).one_or_none()
    if movie:
      movie.delete()
    else:
      abort(404)

    return jsonify({
      'success': True,
      'delete': id
    })

  '''
  DELETE actor
  '''
  @app.route('/actors/<int:id>', methods=['DELETE'])
  @requires_auth('delete:actor')
  def delete_actors(id):
    actor = Actor.query.filter(Actor.id == id).one_or_none()
    if actor:
      actor.delete()
    else:
      abort(404)

    return jsonify({
      'success': True,
      'delete': id
    })

  '''
  POST movies
  '''
  @app.route('/movies', methods=['POST'])
  @requires_auth('add:movie')
  def create_movie():
    body = request.get_json()

    new_title = body.get('title', None)
    new_release_date = body.get('release_date', None)

    if new_title and new_release_date:
      movie = Movie(title=new_title, release_date=new_release_date)
      movie.insert()

      selection = Movie.query.filter(Movie.title == new_title).all()
      movies = [mve.format() for mve in selection]

    else:
      abort(422)

    return jsonify({
      'success': True,
      'movie': movies
    })

  '''
  POST actors
  '''
  @app.route('/actors', methods=['POST'])
  @requires_auth('add:actor')
  def create_actor():
    body = request.get_json()

    new_name = body.get('name', None)
    new_age = body.get('age', None)
    new_gender = body.get('gender', None)

    if new_name:
      actor = Actor(name=new_name, age=new_age, gender=new_gender)
      actor.insert()

      selection = Actor.query.filter(Actor.name == new_name).all()
      actors = [act.format() for act in selection]

    else:
      abort(422)

    return jsonify({
      'success': True,
      'actor': actors
    })

  '''
  PATCH movies
  '''
  @app.route('/movies/<int:id>', methods=['PATCH'])
  @requires_auth('edit:movie')
  def update_movie(id):
    movie = Movie.query.filter(Movie.id == id).one_or_none()

    if movie:
      body = request.get_json()
      updt_title = body.get('title', None)
      updt_release_date = body.get('release_date', None)

      movie.title = updt_title
      movie.release_date = updt_release_date

      movie.update()

      selection = Movie.query.filter(Movie.id == id).all()
      movies = [mve.format() for mve in selection]

    else:
      abort(404)

    return jsonify({
      'success':True,
      'movies': movies
    })
  
  '''
  PATCH actors
  '''
  @app.route('/actors/<int:id>', methods=['PATCH'])
  @requires_auth('edit:actor')
  def update_actor(id):
    actor = Actor.query.filter(Actor.id == id).one_or_none()

    if actor:
      body = request.get_json()
      updt_name = body.get('name', None)
      updt_age = body.get('age', None)
      updt_gender = body.get('gender', None)

      actor.name = updt_name
      actor.age = updt_age
      actor.gender = updt_gender

      actor.update()

      selection = Actor.query.filter(Actor.id == id).all()
      actors = [act.format() for act in selection]

    else:
      abort(404)

    return jsonify({
      'success':True,
      'actors': actors
    })

  ## Error Handling

  @app.errorhandler(422)
  def unprocessable(error):
      return jsonify({
                      "success": False, 
                      "error": 422,
                      "message": "unprocessable"
                      }), 422

  '''
  @TODO implement error handler for 404
      error handler should conform to general task above 
  '''
  @app.errorhandler(404)
  def not_found(error):
      return jsonify({
                      "success": False, 
                      "error": 404,
                      "message": "resource not found"
                      }), 404

  '''
  @TODO implement error handler for AuthError
      error handler should conform to general task above 
  '''

  @app.errorhandler(AuthError)
  def auth_error(error):
      return jsonify({
          'success': False,
          'error': error.status_code,
          'message': error.error['code']
      }), error.status_code

  return app

APP = create_app()

if __name__ == '__main__':
  APP.run()