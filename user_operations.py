import getpass  # To hide the password input
import hashlib
import re       # To extract hashtags using regular expressions
import sqlite3
from database import connect_to_db
from follow_user import follow_user

# We'll use the existing hash_password function for hashing passwords.

# checking valid email ID's
regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'


def login(db_name):
    '''
    Responsibility: Authenticates a user based on the provided username and password.

    @Param db_name (str): The name of the database file to connect to for user authentication.
    @Return: A tuple where the first element is the status code (0 for success, 1 for failure), and the second element is the user ID if authentication is successful.

    '''
    # Convert username to lowercase for case-insensitive comparison
    username = input("Enter your User ID: ").lower()
    password = getpass.getpass("Enter your password: ")

    conn = sqlite3.connect(db_name)
    cur = conn.cursor()

    # Compare the hashed password; also using LOWER for case-insensitive username match
    cur.execute("SELECT * FROM users WHERE LOWER(usr) = ? AND pwd = ?",
                (username, password))
    user = cur.fetchone()

    conn.close()

    if user:
        print("\nLogin successful!")
        # user[0] should be the user ID or username based on your schema
        return 0, user[0]
    else:
        print("\nInvalid username or password. Please try again.")
        return 1, None


def check(email):
    '''
    Responsibility: Validates the format of the provided email address using a regular expression.

    @Param email (str): The email address to be validated.
    @Return: True if the email address is valid, False otherwise, with an "Invalid Email" message printed to the console.

    '''
    # pass the regular expression
    # and the string into the fullmatch() method
    if (re.fullmatch(regex, email)):
        return True
        # print("Valid Email")
    else:
        print("Invalid Email")
        return False


def sign_up(db_name):
    """
    Responsibility: Registers a new user with the provided details and inserts them into the database.

    @Param db_name (str): The name of the database file to connect to for registering a new user.
    @Return: A tuple where the first element is the status code (0 for success, 1 for failure), and the second element is the newly generated user ID.

    """
    name1 = input("Enter your name: ").strip(' ')
    assert len(name1) > 0, "Wrong input"
    usr_id = generate_user_id(db_name)
    email = input("Enter your email: ").strip(' ')
    while not (check(email)):
        email = input("Enter your email: ")
    city = input("Enter your city: ").strip(' ')
    if not city:
        city = 'Edmonton'
        print('Default city set to Edmonton')
    timezone = input(
        "Enter your timezone in number (MST(UTC-7) is deflaut): ").strip(' ')
    if not timezone or timezone.isnumeric() == False:
        timezone = -7
        print('Default timezone set to MST(UTC-7)')
    timezone = float(timezone)
    password = ''
    while len(password) < 1:
        password = getpass.getpass(
            "Create a password: ")  # Hide password input

    # Connect to the database
    conn = sqlite3.connect(db_name)
    cur = conn.cursor()

    # adding data
    try:
        cur.execute("INSERT INTO users (usr, pwd, name, email, city, timezone) VALUES (?, ?, ?, ?, ?, ?)",
                    (usr_id, password, name1, email, city, timezone))
        conn.commit()

    except sqlite3.Error as e:
        conn.rollback()
        print("Error:", e)
        print()
        print("Oops! re-enter the information.")
        return 1

    # Committing the transaction
    conn.commit()
    print("\nSign-up successful! You can now login.")
    print("Your user id: ", usr_id)
    print()
    return 0, usr_id


def generate_user_id(db_name):
    """
    Responsibility: Generates a unique user ID for a new user.

    @Param db_name (str): The name of the database file to connect to for generating a user ID.
    @Return: The new unique user ID.

    """
    conn = sqlite3.connect(db_name)
    cur = conn.cursor()
    cur.execute("SELECT MAX(usr) FROM users")
    max_id = cur.fetchone()[0]
    conn.close()
    return max_id + 1 if max_id else 1


def logout():
    """
    Responsibility: Ends the user session and exits the application.

    @Return: None, but prints a logout confirmation message
    and terminates the program execution with sys.exit().

    """
    print("\nYou have been logged out successfully. Thank you for using the application!")


def search_users(keyword, db_name, userid):
    """
    Responsibility: Searches for users whose names or cities contain the specified keyword, excluding the current user.

    @Param keyword (str): The keyword to search for within user names and cities.
    @Param db_name (str): The name of the database file to connect to for searching users.
    @Param userid (int): The ID of the current user to exclude from the search results.
    @Return: A list of tuples containing the details of users that match the search criteria.

    """
    # Connect to the database
    conn = sqlite3.connect(db_name)
    cur = conn.cursor()

    # Executing the query
    query = f"""
    SELECT usr, name, email, city, timezone
    FROM users
    WHERE (name LIKE '%{keyword}%' OR city LIKE '%{keyword}%') AND usr != {userid}
    ORDER BY LENGTH(name), LENGTH(city)
    """
    cur.execute(query)
    users = cur.fetchall()

    # Close the database connection
    conn.close()

    # Display the results
    choice = 'y'
    initial = 0
    range_us = min(len(users), 5)
    len_us = len(users)
    if users:
        while range_us <= len_us and choice == 'y':
            temp_users = users[initial:range_us]
            for index, user in enumerate(users, 1):
                print("\nCode: ", index)
                print(f"User ID: {user[0]}")
                print(f"Name: {user[1]}")
                print(f"Email: {user[2]}")
                print(f"City: {user[3]}")
                print(f"Timezone: {user[4]}")

            valid = False
            while not valid:
                choice = input(
                    "Enter user's code for more information or press # to continue: ")
                if choice == '#':
                    valid = True
                    break
                elif choice in '1234567890' and (int(choice) in range(initial, range_us + 1)):
                    valid = True
                    try:
                        display_user_details(
                            userid, temp_users[int(choice)-1][0], db_name)
                    except sqlite3.Error as e:
                        print(f'Error: {repr(e)}')
                    except Exception as e:
                        print("Error: ", repr(e))
                else:
                    print("Wrong choice")
            if len_us > range_us:
                choice = input("Show more users? y/n  :")
                if choice == 'y':
                    initial += 5
                    range_us += min(5, len_us - range_us)
            else:
                choice = 'n'
    else:
        print("\n ###### Oops!! No users found matching your keyword. ######")


def display_user_details(userid_self, user_id, db_name):
    '''
    Responsibility: Fetches and displays details for the specified user, including recent tweets and follow statistics.

    @Param userid (int): The ID of the user requesting the details.
    @Param user_id (int): The ID of the user whose details are to be displayed.
    @Param db_name (str): The name of the database file to connect to for fetching user details.
    @Return: None, but prompts the user for a follow action or to view more tweets.

    '''
    conn = sqlite3.connect(db_name)
    cur = conn.cursor()

    # Fetch the required details for the user
    cur.execute("SELECT COUNT(*) FROM tweets WHERE writer = ?", (user_id,))
    tweet_count = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM follows WHERE flwer = ?", (user_id,))
    following_count = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM follows WHERE flwee = ?", (user_id,))
    follower_count = cur.fetchone()[0]

    cur.execute(
        "SELECT * FROM tweets WHERE writer = ? ORDER BY tdate DESC", (user_id,))
    recent_tweets = cur.fetchall()

    # Display the details
    print(f"\nUser ID: {user_id}")
    print(f"Number of tweets: {tweet_count}")
    print(f"Number of following: {following_count}")
    print(f"Number of followers: {follower_count}")
    print("Most recent tweets:")

    initial = 0
    choice = 'm'
    len_tw = len(recent_tweets)
    range_tw = min(len_tw, 3)
    if recent_tweets:
        while range_tw <= len_tw and choice == 'm':
            for tweet in recent_tweets[initial: range_tw]:
                print(f"- {tweet[3]} (Date: {tweet[2]})")
            valid = False
            while not valid:
                if len_tw > range_tw:
                    choice = input('\nPress f to follow user, m to load more tweets and # to continue: ')
                else:
                    choice = input('\nPress f to follow and # to continue: ')

                if choice == 'f':
                    valid = True
                    follow_user(userid_self, user_id, db_name)
                elif choice == 'm' and len_tw > range_tw:
                    initial += 3
                    range_tw += min(3, len_tw - range_tw)
                    valid = True
                elif choice == '#':
                    valid = True
                    continue
                else:
                    print('\nWrong input')
    else:
        print('\nNo tweets found')
        valid = False
        while not valid:
            choice = input('\nPress f to follow or # to continue: ')
            if choice == 'f':
                valid = True
                follow_user(userid_self, user_id, db_name)
            elif choice == '#':
                valid = True
                break
            else:
                print('\nWrong input.')
    # Close the database connection
    conn.close()
