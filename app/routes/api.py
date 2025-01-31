import traceback
from flask import Blueprint, request, jsonify, session
from app.models import User
from app.db import get_db

bp = Blueprint('api', __name__, url_prefix='/api')

# resolves to /api/users
@bp.route('/users', methods=['POST'])
def signup():
    # use request package
    data = request.get_json()

    # global db session
    db = get_db()

    # test dictionary object
    # print(data)

    # attempt to create a new user
    try:
        # pass data object properties to a new User model instance
        newUser = User(
            username=data['username'],
            email=data['email'],
            password=data['password']
        )

        # INSERT the newUser in database
        db.add(newUser)
        db.commit()

    except Exception as e:
        # the INSERT has failed - use sys to print error on server and send an error response
        print(traceback.format_exc())
        # rollback the staged changes to the db on failure
        db.rollback()
        return jsonify(message='Signup failed.'), 500

    # use the session context to store user_id and loggedIn status
    session.clear()
    session['user_id'] = newUser.id
    session['loggedIn'] = True

    # return the id of the new user
    return jsonify(id = newUser.id)

# resolves to /api/logout
@bp.route('/users/logout', methods=['POST'])
def logout():
  # remove session variables
  session.clear()
  # Status 204 - no content
  return '', 204

# resolves to /api/login
@bp.route('/users/login', methods=['POST'])
def login():
  data = request.get_json()
  db = get_db()

  try:
      user = db.query(User).filter(User.email == data['email']).one()
      print(user)
      # if user exists we can use verify_password method in User
      # data['password'] becomes the second parameter in the verify_password() method of
      # the class, because the first parameter is reserved for self
      if user.verify_password(data['password']) == False:
          return jsonify(message='Incorrect credentials'), 400

      session.clear()
      session['user_id'] = user.id
      session['loggedIn'] = True

      return jsonify(id=user.id)

  except Exception as e:
      # the query has failed to return a matching user/email
      print(traceback.format_exc())

      return jsonify(message='Incorrect credentials'), 400