from flask import request, jsonify
from blogapi.authentication import Registration, Login, UpdateAccount, Posts
from blogapi import app, bcrypt, db
from blogapi.models import User, Post
from datetime import datetime


@app.route('/register', methods=['GET', 'POST'])
def register():
    authentication = Registration()
    if request.method == 'POST':
        if authentication.validate_on_submit():
            existing_user = User.query.filter_by(username=authentication.username.data).first()
            if existing_user:
                return jsonify({
                    'status': 'error',
                    'message': 'That username has been taken. Enter a different one.'
                }), 400
                
            existing_email = User.query.filter_by(email=authentication.email.data).first()
            if existing_email:
                return jsonify({
                    'status': 'error',
                    'message': 'That email has been taken. Enter a different one.'
                }), 400
                
            hashed_password = bcrypt.generate_password_hash(authentication.password.data).decode('utf-8')
            
           
            user = User(
                first_name=authentication.first_name.data,
                last_name=authentication.last_name.data,
                username=authentication.username.data,
                email=authentication.email.data,
                password=hashed_password
            )
            
            
            db.session.add(user)
            db.session.commit()
            
            user_data = {
                'first_name': authentication.first_name.data,
                'last_name' : authentication.last_name.data,
                'username': authentication.username.data,
                'email' : authentication.email.data,
            }
            return jsonify ({
                'status': 'success',
                'message': 'user account created successfuly',
                'user': user_data
            }), 201
            
        else:
            return jsonify({
                'status': 'error',
                'message': 'validation failed',
                'errors': authentication.errors
                
            }), 400
    
    
    return jsonify({
        'message': 'Send POST request with user data to register'
    })



@app.route('/login', methods=['GET', 'POST'])
def login():
    authentication = Login()
    
    if request.method == 'POST':
        if authentication.validate_on_submit():
           
            user = User.query.filter_by(email=authentication.email.data).first()
            
            if user and bcrypt.check_password_hash(user.password, authentication.password.data):
                user_data = {
                    'email': authentication.email.data,
                }
                return jsonify({
                    'status': 'success',
                    'message': 'login successful',
                    'user': user_data
                }), 200
            else:
                return jsonify({
                    'status': 'error',
                    'message': 'password incorrect. Try again'
                }), 401
        else:
            return jsonify({
                'status': 'error',
                'message': 'login unsuccessful',
                'errors': authentication.errors
            }), 400
    
    
    return jsonify({
        'message': 'Send POST request with email and password to login'
    })
    
    
@app.route('/logout', methods=['GET', 'POST'])
def logout():
    return jsonify({
        'status': 'success',
        'message': 'logout successful'
        
    }), 200
    

@app.route('/account', methods=['POST'])
def account():
    authentication = UpdateAccount()
    if request.method == 'POST':
        if authentication.validate_on_submit():
            
           
            user = User(
                first_name=authentication.first_name.data,
                last_name=authentication.last_name.data,
                username=authentication.username.data,
                email=authentication.email.data,
                
            )
            
            
            db.session.add(user)
            db.session.commit()
            
            user_data = {
                'first_name': authentication.first_name.data,
                'last_name' : authentication.last_name.data,
                'username': authentication.username.data,
                'email' : authentication.email.data,
            }
            return jsonify ({
                'status': 'success',
                'message': 'user account updated successfuly',
                'user': user_data
            }), 201
            
        else:
            return jsonify({
                'status': 'error',
                'message': 'validation failed',
                'errors': authentication.errors
                
            }), 400
            
            
@app.route('/posts', methods=['GET', 'POST'])
def posts():
    authentication = Posts()
    
    if request.method == 'POST':
        if authentication.validate_on_submit():
            post = Post(
                title=authentication.title.data,
                content=authentication.content.data,
                user_id=1
            )
            
            db.session.add(post)
            db.session.commit()
            
            post_data = {
                'post_id': post.id,
                'title': post.title,
                'content': post.content,
                'date_posted': post.date_posted.isoformat()
            }
            
            return jsonify({
                'status': 'success',
                'message': 'Your post has been added successfully',
                'post': post_data
            }), 201
            
        else:
            return jsonify({
                'status': 'error',
                'message': 'Post not added',
                'errors': authentication.errors
            }), 400
    
    return jsonify({
        'message': 'Send POST request with post data to create a post'
    })

    
    