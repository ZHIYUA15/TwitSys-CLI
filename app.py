import pymysql
from flask import Flask, render_template, request, redirect, url_for
# from flask_sqlalchemy import SQLAlchemy
# from sqlalchemy.sql import text

# Create a variable to deal with SQL commands
# db = SQLAlchemy()
# Create the app
app = Flask(__name__)
# Name of database (add the name please)
# db_name = "/tweets_table"
# user = "tweets_table"
# pwd = "tweets_table"
# server = "db4free.net"
# userpass = 'mysql+pymysql://' + user + ':' + pwd + '@'

# Extract data from MySQL
conn = pymysql.connect(
    host='db4free.net',
    user='tweets_table',
    password='tweets_table',
    db='tweets_table'
)
cursor = conn.cursor()
cursor.execute("SELECT name, pwd FROM users")
result = cursor.fetchall()
print(result)

# # app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + db_name # For SQLite only
# app.config["SQLALCHEMY_DATABASE_URI"] = userpass + server + db_name # For MySQL (replace the variables and it should work)

# app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True

# # initialize the app with Flask-SQLAlchemy
# db.init_app(app)

# Test database connection
# def testdb():
#     try:
#         db.session.query(text('1')).from_statement(text('SELECT 1')).all()
#         return '<h1>It works.</h1>'
#     except Exception as e:
#         # e holds description of the error
#         error_text = "<p>The error:<br>" + str(e) + "</p>"
#         hed = '<h1>Something is broken.</h1>'
#         return hed + error_text

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
        for userpwd in result:
            if username == userpwd[0] and password == userpwd[1]:
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
