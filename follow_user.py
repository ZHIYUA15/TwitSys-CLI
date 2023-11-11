import sys
from datetime import datetime
import sqlite3


def follow_user(current_user_id, user_id_follow, db_name):
    '''
    Responsibility: Follow another user.

    @param current_user_id: The ID of the current user who wants to follow another user.
    @param user_id_follow: The ID of the user to be followed.
    @param db_name: The name of the database file.
    @return: None. Outputs the result of the operation directly to the console.

    '''
    conn = sqlite3.connect(db_name)
    cur = conn.cursor()

    # Get the current date
    current_date = datetime.now().strftime("%Y-%m-%d")
    # Debug print
    print(
        f"\nAttempting to follow user with ID {user_id_follow} on date {current_date}")

    # Insert new follow relationship with the current date as start_date
    try:
        cur.execute("INSERT INTO follows (flwer, flwee, start_date) VALUES (?, ?, ?)",
                    (current_user_id, user_id_follow, current_date))
        conn.commit()
    except sqlite3.Error as e:
        # if row already exists
        if "UNIQUE constraint failed: follows.flwer, follows.flwee" in str(e):
            print('\nYou already follow this user.')
        else:
            print("\nAn error occurred:", e)
        conn.rollback()
    else:
        print(f"\nYou are now following ", user_id_follow)
        print("\nKeep on tweeting!")

    # Close the database connection
    conn.close()
