import sqlite3
import time
from datetime import datetime
from user_operations import *
from database import connect_to_db


def list_followers(user_id, db_name):
    """
    Responsibilities: List the followers of the logged-in user.

    @param user_id: The ID of the user whose followers are to be listed.
    @param db_name: The name of the database file.
    @return: None. Outputs the list of followers directly to the console.

    """
    # Connect to the database
    conn = sqlite3.connect(db_name)
    cur = conn.cursor()

    # Query to retrieve the followers
    query = f"""
    SELECT flwer, name
    FROM follows JOIN users ON follows.flwer = users.usr
    WHERE flwee = {user_id};
    """
    try:
        # Execute the query using the secure method from the database module
        cur.execute(query)
        followers = cur.fetchall()

        # Display the followers
        ids = [follower[0] for follower in followers]
        if followers:
            for idx, follower in enumerate(followers, 1):
                print(f"\n{idx}. User ID: {follower[0]}, Name: {follower[1]}")

            valid = False
            while not valid:
                user_followee = input(
                    '\nEnter user code of user to show more details, or press # to continue: ')
                if user_followee == '#':
                    valid = True
                    break
                # checks if input is correct and the input lies withing the proper range of options
                elif user_followee.isnumeric() and int(user_followee) in range(1, len(followers)+1):
                    display_user_details(
                        user_id, ids[int(user_followee)-1], db_name)
                    valid = True
        else:
            print("\nYou don't have any followers.")
            time.sleep(3)
    except Exception as e:
        print(f"An error occurred:## {e}")
