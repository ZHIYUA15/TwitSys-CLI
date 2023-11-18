from flask import Flask, render_template, request, jsonify, redirect, url_for
import sqlite3

app = Flask(__name__)
app.run(debug=True, port=5500)  # Use a different port number


def get_db_connection():
    # Replace with your actual database name
    conn = sqlite3.connect('your_database.db')
    conn.row_factory = sqlite3.Row
    return conn


@app.route('/api/users/<int:user_id>', methods=['GET', 'PUT', 'DELETE'])
def api_user(user_id):
    if request.method == 'GET':
        # Logic to get user data
        pass
    elif request.method == 'PUT':
        # Logic to update user data
        pass
    elif request.method == 'DELETE':
        # Logic to delete user
        pass
    return jsonify({'message': 'success'})


@app.route('/')
def home():
    return "Welcome to the Twitter-like app"


@app.route('/compose_tweet', methods=['GET', 'POST'])
def compose_tweet():
    if request.method == 'POST':
        # Assuming you have user authentication in place
        user_id = request.form['user_id']
        tweet_text = request.form['tweet']
        conn = get_db_connection()
        cur = conn.cursor()
        # Rest of your logic from compose_tweet goes here...
        # Ensure to modify the database operations to use the `conn` and `cur` objects
        conn.close()
        return redirect(url_for('home'))
    # Create a compose_tweet.html template for this
    return render_template('compose_tweet.html')


@app.route('/followers/<int:user_id>')
def followers(user_id):
    conn = get_db_connection()
    cur = conn.cursor()
    # Adapt your list_followers logic here to use conn and cur
    # Instead of printing the followers, store them in a variable
    followers = []  # This should be the result of your database query
    conn.close()
    # Create a followers.html template
    return render_template('followers.html', followers=followers)


@app.route('/follow_user', methods=['POST'])
def follow_user():
    # Assumes you have a user authentication system
    current_user_id = request.form['current_user_id']
    user_id_to_follow = request.form['user_id_to_follow']
    conn = get_db_connection()
    cur = conn.cursor()
    # Adapt the follow_user logic here
    conn.close()
    return redirect(url_for('home'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Add your authentication logic here
        return redirect(url_for('home'))
    return render_template('login.html')  # Create a login.html template


@app.route('/tweet/<int:tweet_id>')
def view_tweet(tweet_id):
    conn = get_db_connection()
    cur = conn.cursor()
    # Add your logic to retrieve the tweet by tweet_id
    tweet = {}  # Replace with the actual tweet data
    conn.close()
    # Create a tweet.html template
    return render_template('tweet.html', tweet=tweet)


@app.route('/profile/<int:user_id>')
def user_profile(user_id):
    conn = get_db_connection()
    cur = conn.cursor()
    # Add your logic to retrieve user information and their tweets
    user_info = {}  # Replace with actual user data
    tweets = []  # Replace with actual tweets
    conn.close()
    # Create a profile.html template
    return render_template('profile.html', user=user_info, tweets=tweets)


@app.route('/edit_tweet/<int:tweet_id>', methods=['GET', 'POST'])
def edit_tweet(tweet_id):
    # Add your logic for editing a tweet
    return redirect(url_for('view_tweet', tweet_id=tweet_id))


@app.route('/delete_tweet/<int:tweet_id>', methods=['POST'])
def delete_tweet(tweet_id):
    # Add your logic for deleting a tweet
    return redirect(url_for('home'))


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404  # Create a 404.html template


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500  # Create a 500.html template

# Placeholder routes for registration and logout


@app.route('/register', methods=['GET', 'POST'])
def register():
    # Add registration logic
    return render_template('register.html')  # Create register.html


@app.route('/logout')
def logout():
    # Add logout logic
    return redirect(url_for('home'))  # Redirect to home page


@app.route('/api/tweets', methods=['GET'])
def api_tweets():
    # Add logic to return tweets data in JSON format
    return jsonify({'tweets': []})


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5500)
