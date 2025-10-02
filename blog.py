from flask import Flask, request, jsonify
from authentication import Registration, Login
app = Flask(__name__)

app.config['SECRET_KEY'] = 'fb9cf91dc75ad7e4a499d552d3f28b4f'


@app.route('/register', methods=['GET', 'POST'])
def register():
    authentication = Registration()
    if request.method == 'POST':
        if authentication.validate_on_submit():
            
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
                'message': 'login unsuccessful',
                'errors': authentication.errors
            }), 400
    
    
    return jsonify({
        'message': 'Send POST request with email and password to login'
    })
            


if __name__ == '__main__':
    app.run(debug=True)
    
    