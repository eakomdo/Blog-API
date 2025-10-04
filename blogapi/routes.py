from flask import request, jsonify
from blogapi.authentication import Registration, Login, UpdateAccount, Posts
from blogapi import app, bcrypt, db
from blogapi.models import User, Post, Comment, Tag



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
    
    elif request.method == 'GET':
        posts = Post.query.all()
        posts_data = []
        for post in posts:
            post_dict = {
                'id': post.id,
                'title': post.title,
                'content': post.content,
                'date_posted': post.date_posted.isoformat(),
                'user_id': post.user_id
            }
            posts_data.append(post_dict)
        
        return jsonify({
            'status': 'success',
            'posts': posts_data
        }), 200
    

@app.route('/posts/delete/<int:post_id>', methods=['DELETE'])
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if request.method == 'DELETE':
        db.session.delete(post)
        db.session.commit()
        return jsonify({
            'status': 'success',
            'message': 'Your post has been deleted successfully'
        }), 200
            
    return jsonify({
        'message': 'Send DELETE request to delete a post'
    }) 


@app.route('/posts/update/<int:post_id>', methods=['PUT'])
def update_post(post_id):
    authentication = Posts ()
    post = Post.query.get_or_404(post_id)
    if request.method == 'PUT':
        if authentication.validate_on_submit():
            post.title = authentication.title.data
            post.content = authentication.content.data
            
            db.session.commit()
                
            post_data = {
                'post_id': post.id,
                'title': post.title,
                'content': post.content,
                'date_posted': post.date_posted.isoformat()
            }
            
            return jsonify({
                'status': 'success',
                'message': 'Your post has been updated successfully',
                'post': post_data
            }), 200
            
        else:
            return jsonify({
                'status': 'error',
                'message': 'Post not updated',
                'errors': authentication.errors
            }), 400

    return jsonify({
        'message': 'Send PUT request with post data to update a post'
    })
    

@app.route('/posts/<int:post_id>/comments', methods=['GET', 'POST'])
def post_comment(post_id):
    post = Post.query.get_or_404(post_id)
    
    if request.method == 'POST':
        data = request.get_json()
        if not data or 'content' not in data or 'user_id' not in data:
            return jsonify({
                'status': 'error',
                'message': 'Content is required to be able to comment'
            }), 400
        
        comment = Comment(
            content=data['content'],
            user_id=data['user_id'],
            post_id=post_id,   
        )
        
        db.session.add(comment)
        db.session.commit()
        
        comment_data = {
            'id': comment.id,
            'content': comment.content,
            'date_posted': comment.date_posted.isoformat(),
            'user_id': comment.user_id,
            'post_id': comment.post_id, 
        }
        
        return jsonify({
            'status': 'success',
            'message': 'Comment added successfully',
            'comment': comment_data
        }), 201
    
    elif request.method == 'GET':
        comments = Comment.query.filter_by(post_id=post_id).all()
        comments_data = []
        
        for comment in comments:
            comment_dict = {
                'id': comment.id,
                'content': comment.content,
                'date_posted': comment.date_posted.isoformat(),
                'user_id': comment.user_id,
                'author_username': comment.author.username,
            }
            comments_data.append(comment_dict)
        
        return jsonify({
            'status': 'success',
            'comments': comments_data
        }), 200


@app.route('/tag-post', methods=['POST'])
def tag_post():
    data = request.get_json()
    
    if not data or 'tag_name' not in data or 'post_id' not in data:
        return jsonify({
            'status': 'error',
            'message': 'tag_name and post_id are required'
        }), 400
    
    post = Post.query.get_or_404(data['post_id'])
    
   
    tag = Tag.query.filter_by(name=data['tag_name']).first()
    
    if not tag:
        tag = Tag(
            name=data['tag_name'],
            description=data.get('description', '')
        )
        db.session.add(tag)
    
   
    if tag not in post.tags:
        post.tags.append(tag)
        db.session.commit()
        
        return jsonify({
            'status': 'success',
            'message': f'Post {data["post_id"]} tagged with "{data["tag_name"]}" successfully',
            'post_id': data['post_id'],
            'post_title': post.title,
            'tag': {
                'id': tag.id,
                'name': tag.name,
                'description': tag.description
            }
        }), 200
    else:
        return jsonify({
            'status': 'info',
            'message': f'Post {data["post_id"]} already has tag "{data["tag_name"]}"'
        }), 200