from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# A placeholder for user authentication (you should implement a real one)
def authenticate_user(username, password):
    # Replace this with your actual authentication logic
    if username == "your_username" and password == "your_password":
        return True
    return False

@app.route('/')
def home():
    return render_template('index.html')

# List of valid usernames and passwords (for testing purposes)
valid_users = [{'username': 'user1', 'password': 'password1'}, {'username': 'user2', 'password': 'password2'}]

@app.route('/login', methods=['GET', 'POST'])
def login():
    error_message = None  # Initialize the error message as None
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        # Check if the provided username and password match any valid user
        for user in valid_users:
            if username == user['username'] and password == user['password']:
                # Authentication successful, redirect to the dashboard
                return redirect(url_for('dashboard'))

        # If no match is found, show an error message
        error_message = "Invalid username or password. Please try again."

    return render_template('index.html', error_message=error_message)

# Define other routes...

@app.route('/dashboard')
def dashboard():
    # This route should only be accessible if the user is authenticated
    return "Welcome to the dashboard!"

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5500)
