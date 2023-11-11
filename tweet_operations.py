import sqlite3
import re
from datetime import datetime  # To get the current date and time
from database import connect_to_db


def compose_tweet(user_id, db_name):
    """
    Responsibility: Allow a user to compose and post a tweet.
    @param user_id: The ID of the user posting the tweet.
    @param db_name: The name of the database file.
    @return: None. The result of the tweet post is output directly to the console.

    """
    tweet_text = input("Compose your tweet: ")

    # Extract hashtags from the tweet
    hashtags = re.findall(r"#(\w+)", tweet_text)

    # Get the current date and time
    current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Connect to the database
    conn = sqlite3.connect(db_name)
    cur = conn.cursor()

    # Inserting the tweet into the tweets table
    cur.execute("INSERT INTO tweets (writer, tdate, text) VALUES (?, ?, ?)",
                (user_id, current_datetime, tweet_text))

    # Getting the tweet ID of the inserted tweet
    tweet_id = cur.lastrowid

    # Inserting the hashtags into the hashtags and mentions tables
    for hashtag in hashtags:
        cur.execute(
            "INSERT OR IGNORE INTO hashtags (term) VALUES (?)", (hashtag,))
        cur.execute("INSERT INTO mentions (tid, term) VALUES (?, ?)",
                    (tweet_id, hashtag))

    # Committing the transaction
    conn.commit()

    # Close the database connection
    conn.close()

    print("\nYour tweet has been posted successfully!")

# You can call this function with the user ID of the logged-in user
# compose_tweet(user_id)


def search_tweets(keywords, db_name):
    """
    Responsibility: Search for tweets matching the given keywords or hashtags.
    @param keywords: A list of keywords to search for within the tweets.
    @param db_name: The name of the database file to connect to for searching tweets.
    @return: A tuple containing the action code (0 for no action, 1 for retweet, 2 for reply) and the tweet ID of interest, if any.

    """
    # Connect to the database
    conn = sqlite3.connect(db_name)
    cur = conn.cursor()

    keyword_conditions = []
    parameters = []
    for keyword in keywords:
        if keyword.startswith("#"):
            # Remove the '#' character from the keyword
            hashtag = keyword[1:]
            # Include a condition to check for mentions in the 'mentions' table
            keyword_conditions.append(
                "(text LIKE ? OR tid IN (SELECT tid FROM mentions WHERE term = ?))"
            )
            parameters.append('%' + keyword + '%')
            parameters.append(hashtag)
        else:
            keyword_conditions.append("text LIKE ?")
            parameters.append(f'%{keyword}%')

    # Create a tuple of parameters for the query
    parameters = tuple(parameters)
    condition = " OR ".join(keyword_conditions)

    # Executing the query with parameters
    query = f"""
    SELECT tid, writer, tdate, text
    FROM tweets
    WHERE {condition}
    ORDER BY tdate DESC;
    """
    cur.execute(query, parameters)
    tweets = cur.fetchall()

    # Close the database connection
    conn.close()

    # Display the results
    choice = 'y'
    initial = 0
    range_tw = min(len(tweets), 5)
    len_tw = len(tweets)

    # main logic to execute display and options for the user
    if tweets:
        while range_tw <= len_tw and choice == 'y':
            temp_tweet = tweets[initial:range_tw]
            for index, tweet in enumerate(tweets[initial:range_tw], 1):
                print("\nCode: ", index)
                print(f"Tweet ID: {tweet[0]}")
                print(f"Writer: {tweet[1]}")
                print(f"Date: {tweet[2]}")
                print(f"Text: {tweet[3][:15]}...")

            valid = False
            while not valid:
                choice = input(
                    'Choose tweet for more information [enter code for tweet or # to not search]: ')
                if choice == '#':
                    valid = True
                    break
                elif choice in '1234567890' and (int(choice) in range(1, range_tw+1)):
                    valid = True
                    choice = int(choice)
                    # call below function to display tweet information
                    code = show_tweet_detail(temp_tweet[choice - 1][0], temp_tweet[choice - 1][3],
                                             temp_tweet[choice - 1][1], temp_tweet[choice - 1][2], db_name)
                    return code, temp_tweet[choice - 1][0]
                else:
                    print('\nWrong Input')

            valid = False   # to check if the correct input [y/n] is entered
            if len_tw > range_tw:
                while not valid:
                    choice = input("\nShow more tweets? y/n  :")
                    if choice == 'y':
                        initial += 5            # adds 5 to initial
                        # increases last tweet range
                        range_tw += min(5, len_tw-range_tw)
                        valid = True
                    elif choice == 'n':
                        valid = True
                        return 0, None
                    else:
                        print("Wrong input")
            else:
                choice = 'n'
                return 0, None

            if not valid:
                return 0, None
    else:
        print("\n##### Oops!! No tweets found matching your keywords. ######")
        return 0, None

# You can call this function with a list of keywords
# search_tweets(["#example", "keyword"])


def display_tweets(user_id, db_name, cont=False, tweet_lis=[], initial_g=None, range_t=None):
    """
    Display the tweets and retweets from users followed by the logged-in user.
    """

    if not cont:
        # Connect to the database
        conn = sqlite3.connect(db_name)
        cur = conn.cursor()

        # Query to retrieve the tweets and retweets
        query = f"""
        SELECT DISTINCT tweets.tid, tweets.writer, tweets.tdate, tweets.text
        FROM tweets
        WHERE (
        tweets.writer IN (
            SELECT flwee
            FROM follows
            WHERE flwer = {user_id}
        )
        OR tweets.tid IN (
            SELECT rt.tid
            FROM retweets rt
            WHERE rt.usr IN (
                SELECT flwee
                FROM follows
                WHERE flwer = {user_id}
            )
        )
        )
        AND tweets.writer != {user_id}
        ORDER BY tweets.tdate DESC;

        """
        cur.execute(query)
        tweets = cur.fetchall()
        conn.close()     # Close the database connection
        initial = 0
        range_twe = min(len(tweets), 5)

    elif cont is True:
        tweets = tweet_lis
        initial = initial_g
        range_twe = range_t

    # Display the tweets and retweets
    if tweets:
        temp_tweet = tweets[initial:range_twe]
        for index, tweet in enumerate(temp_tweet, 1):
            print("\nCode id: ", index)
            print(f"Tweet ID: {tweet[0]}")
            print(f"Writer: {tweet[1]}")
            print(f"Date: {tweet[2]}")
            print(f"Text: {tweet[3][:15]}...")

        if cont is True:
            return temp_tweet   # current tweet page, choice of user
        else:
            # current tweet page, all tweets, choice of user, start point of tweet, last point of tweet
            return temp_tweet, tweets, initial, range_twe

    else:
        print("\n:( Oops! No tweets found from the users you follow.")
        return [], [], 0, 0

# You can call this function with the user ID of the logged-in user
# display_tweets(user_id)


def show_tweet_detail(tweet_id, text, writer, date, db_name):
    """
    When a tweet is chosen, it will fetch more details about the tweet, and will give you further options
    input: tid -> tweet id to be searched for
    """

    conn = sqlite3.connect(db_name)
    cur = conn.cursor()
    query = f"""
    SELECT COUNT(*) as count
    FROM retweets as re
    WHERE tid = {tweet_id};
    """
    cur.execute(query)
    count_retweet = cur.fetchone()[0]

    query = f"""
    SELECT COUNT(*) as count
    FROM tweets as t 
    WHERE replyto = {tweet_id}
    """

    cur.execute(query)
    replies = -1
    try:
        replies = cur.fetchone()[0]
    except Exception as e:
        print('Something went wrong!')
    conn.close()

    print('\n**************************')
    print("Tweet information: ")
    print('Tweet id: ', tweet_id)
    print('Writer: ', writer)
    print('Date: ', date)
    print('Text: ', text)
    print('Retweets: ', count_retweet)
    print('Replies: ', replies)

    print('\nPress 1 to retweet')
    print('Press 2 to reply')
    print('Press 3 to return to Homepage')

    valid = False
    while not valid:
        choice = input('\nChoice: ')
        if choice in '123':
            valid = True

    return int(choice)


def retweet(userid, tweet_id, db_name):
    conn = sqlite3.connect(db_name)
    cur = conn.cursor()
    current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    query = f"""
    INSERT INTO retweets (usr, tid, rdate) VALUES (?, ?, ?)
    """

    try:
        cur.execute(query, (userid, tweet_id, current_datetime))
    except sqlite3.Error:
        print('\n Problem encountered. Try again.')

    print('\nRetweet successful.')
    conn.commit()
    conn.close()


def reply(userid, tweet_id, db_name):

    text = input('\nWrite your reply: ')

    conn = sqlite3.connect(db_name)
    cur = conn.cursor()
    current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    query = f"""
    INSERT INTO tweets (writer, tdate, text, replyto) VALUES (?, ?, ?, ?);"""

    try:
        cur.execute(query, (userid, current_datetime, text, tweet_id))
    except sqlite3.Error as e:
        print('\nProblem encountered. Try again.')
        return

    print('\nReply added.')
    conn.commit()
    conn.close()
