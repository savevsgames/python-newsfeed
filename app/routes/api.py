import traceback
from flask import Blueprint, request, jsonify, session
from app.models import User, Post, Comment, Vote
from app.db import get_db
from app.utils.auth import login_required

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

@bp.route('/comments', methods=['POST'])
@login_required
def comment():
  data = request.get_json()
  db = get_db()

  try:
      # create a new comment
      newComment = Comment(
          comment_text=data['comment_text'],
          post_id=data['post_id'],
          user_id=session.get('user_id')
      )

      db.add(newComment)
      db.commit()

      return jsonify(id=newComment.id)

  except Exception as e:
      # the query has failed to INSERT new comment
      print(traceback.format_exc())

      db.rollback()
      return jsonify(message='Comment failed'), 500


# upvote endpoint creates new record in votes table
@bp.route('/posts/upvote', methods=['PUT'])
@login_required
def upvote():
  data = request.get_json()
  db = get_db()

  try:
    # create a new vote with incoming post id and user/session id
    newVote = Vote(
      post_id = data['post_id'],
      user_id = session.get('user_id')
    )

    db.add(newVote)
    db.commit()
  except Exception as e:
    # the query has failed to INSERT new upvote
    print(traceback.format_exc())

    db.rollback()
    return jsonify(message = 'Upvote failed'), 500

  return '', 204


# create a post
@bp.route('/posts', methods=['POST'])
@login_required
def create():
  data = request.get_json()
  db = get_db()

  try:
    # create a new post
    newPost = Post(
      title = data['title'],
      post_url = data['post_url'],
      user_id = session.get('user_id')
    )

    db.add(newPost)
    db.commit()
  except Exception as e:
    # the query has failed to INSERT new post
    print(traceback.format_exc())

    db.rollback()
    return jsonify(message = 'Post failed'), 500

  return jsonify(id = newPost.id)


# update posts
@bp.route('/posts/<id>', methods=['PUT'])
@login_required
def update(id):
  data = request.get_json()
  db = get_db()

  try:
    # retrieve post and update title property
    post = db.query(Post).filter(Post.id == id).one()
    post.title = data['title']
    db.commit()
  except Exception as e:
    # the query has failed to UPDATE post
    print(traceback.format_exc())

    db.rollback()
    return jsonify(message = 'Post not found'), 404

  return '', 204

# delete posts
@bp.route('/posts/<id>', methods=['DELETE'])
@login_required
def delete(id):
  db = get_db()

  try:
    # delete post from db
    db.delete(db.query(Post).filter(Post.id == id).one())
    db.commit()
  except Exception as e:
    # the query has failed to DELETE post
    print(traceback.format_exc())

    db.rollback()
    return jsonify(message = 'Post not found'), 404

  return '', 204