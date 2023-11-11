import getpass  # To hide the password input
import os.path
import sqlite3  # To interact with the SQLite database
import re       # To extract hashtags using regular expressions
import sys
import time
from datetime import datetime  # To get the current date and time

# Importing custom modules for different operations
from follower_operations import * # Importing all functions from follower_operations module
from tweet_operations import * # Importing all functions from tweet_operations module
from user_operations import * # Importing all functions from user_operations module
from database import connect_to_db as connect, initial_query as initiate # Importing specific functions from database module



def display_menu1():
    """
    Responsibility: Display the initial login/signup menu options to the user.

    @return: The choice of the user as an integer.

    """
    print("\nWelcome to the Twitter-like CLI Application!")
    valid = False

    while not valid:
        print("1. Login")
        print("2. Sign Up")
        print("3. Exit")
        choice = input("Please enter your choice (1/2/3): ")
        if choice not in ['1', '2', '3']:
            print("Wrong input ")
        else:
            valid = True

    return int(choice)


def display_menu2():
    """
    Responsibility: Display the main menu options to the user after login.

    @return: The choice of the user as an integer or a special character.

    """
    print("\n")
    valid = False

    choice = 0
    while not valid:
        print("*. Main Menu")
        print("6. Search for tweets")
        print("7. Search for users")
        print("8. Compose a tweet")
        print("9. List followers")
        print("0. Logout")
        print()

        choice = input(
            "Please enter your choice [code found in front of tweets and options]: ")
        if choice not in '0123456789#*':
            print("Wrong\n")
        else:
            valid = True

    if choice in '#*':
        return choice
    return int(choice)

# Code for displaying menus and handling user inputs


def main_menu():
    '''
    Responsibility: Handle the initial menu logic including login, signup, and exit.

    @return: A tuple with the user ID and an exit code.

    '''
    choice = display_menu1()

    if choice == 1:
        # call login
        cond_login = 1  # stores if login was successful
        # only exits loop when cond_login = 0
        cond_login, userid = login(db_name)
        if cond_login == 1:
            return -1, 2
        return userid, 0

    elif choice == 2:
        cond = 1
        while cond == 1:
            try:
                cond, userid = sign_up(db_name)     # only exits when cond = 0
                for i in range(10):
                    time.sleep(0.5)
                    print('*', end='', flush=True)          # creates a buffer
                print('\n')
            except AssertionError as e:
                print(e)
        return userid, 0

    elif choice == 3:           # for exiting the program
        print('Thank you')
        return None, 1


def internal_menu(len_tw=0, last=0,):
    '''
    Responsibility: Handle the internal menu logic after a user is logged in.
    @param len_tw: The number of tweets currently loaded.
    @param last: The index of the last tweet loaded.
    @return: An exit code indicating the state of the menu (continue, error, or logout).

    '''
    def fetch_tweet_info(temp_tweet, index):
        return temp_tweet[index][0], temp_tweet[index][1], temp_tweet[index][2], temp_tweet[index][3]

    cont = False  # cont = false => first run, cont = True => load more tweet run
    temp_tweet = tweets = []
    initial = last = 0
    while True:

        time.sleep(2)
        print("\n*************************************************************")
        print("Homepage")
        print("*************************************************************")

        # display tweets at the homepage
        if not cont:
            temp_tweet, tweets, initial, last = display_tweets(
                userid, db_name, False)
            len_temp_tweet = len(temp_tweet)
            len_tw = len(tweets)

        else:
            len_tw = len(tweets)
            initial += 5
            last += min(5, len_tw - last)
            temp_tweet = display_tweets(
                userid, db_name, True, tweets, initial, last)
            len_temp_tweet = len(temp_tweet)

        if len_tw > last:
            print("\nPress # to load more tweets.")

        choice_main = display_menu2()

        if choice_main == '#' and len_tw > last:
            cont = True
            continue
        elif choice_main == '*':
            return 2
        elif choice_main == 1 and len_temp_tweet >= 1:
            tweet_id, tweet_writer, tweet_date, tweet_text = fetch_tweet_info(
                temp_tweet, 0)
            # display the chosen tweet stats
            code = show_tweet_detail(
                tweet_id, tweet_text, tweet_writer, tweet_date, db_name)
            # user will choose an option and based on that functions will run - returns choice of the user
            if code == 1:
                # allows user to retweet
                retweet(userid, tweet_id, db_name)
                cont = False
            elif code == 2:
                reply(userid, tweet_id, db_name)
                cont = False  # allows user to reply
            else:
                cont = False
                pass

        elif choice_main == 2 and len_temp_tweet >= 2:
            tweet_id, tweet_writer, tweet_date, tweet_text = fetch_tweet_info(
                temp_tweet, 1)
            code = show_tweet_detail(
                tweet_id, tweet_text, tweet_writer, tweet_date, db_name)
            if code == 1:
                retweet(userid, tweet_id, db_name)
                cont = False
            elif code == 2:
                reply(userid, tweet_id, db_name)
                cont = False
            else:
                cont = False
                pass

        elif choice_main == 3 and len_temp_tweet >= 3:
            tweet_id, tweet_writer, tweet_date, tweet_text = fetch_tweet_info(
                temp_tweet, 2)
            code = show_tweet_detail(
                tweet_id, tweet_text, tweet_writer, tweet_date, db_name)
            if code == 1:
                retweet(userid, tweet_id, db_name)
                cont = False
            elif code == 2:
                reply(userid, tweet_id, db_name)
                cont = False
            else:
                cont = False
                pass

        elif choice_main == 4 and len_temp_tweet >= 4:
            tweet_id, tweet_writer, tweet_date, tweet_text = fetch_tweet_info(
                temp_tweet, 3)
            code = show_tweet_detail(
                tweet_id, tweet_text, tweet_writer, tweet_date, db_name)
            if code == 1:
                retweet(userid, tweet_id, db_name)
                cont = False
            elif code == 2:
                reply(userid, tweet_id, db_name)
                cont = False
            else:
                cont = False
                pass

        elif choice_main == 5 and len_temp_tweet >= 5:
            tweet_id, tweet_writer, tweet_date, tweet_text = fetch_tweet_info(
                temp_tweet, 4)
            code = show_tweet_detail(
                tweet_id, tweet_text, tweet_writer, tweet_date, db_name)
            if code == 1:
                retweet(userid, tweet_id, db_name)
                cont = False
            elif code == 2:
                reply(userid, tweet_id, db_name)
                cont = False
            else:
                cont = False
                pass

        elif choice_main == 6:
            keywords = [word for word in input(
                'Provide keywords: ').split(' ')]
            print("*************************************************************")
            code, tweet_id = search_tweets(keywords, db_name)
            if code == 1:
                retweet(userid, tweet_id, db_name)
            elif code == 2:
                reply(userid, tweet_id, db_name)
            else:
                pass

        elif choice_main == 7:
            keywords = input('Provide name or keyword: ')
            print("*************************************************************")
            search_users(keywords, db_name, userid)

        elif choice_main == 8:
            print("*************************************************************")
            compose_tweet(userid, db_name)

        elif choice_main == 9:
            print("*************************************************************")
            list_followers(userid, db_name)

        elif choice_main == 0:
            print("*************************************************************")
            print("\nThank you. You have been successfully logged out!")
            return 0
        else:
            print("*************************************************************")
            cont = False
            print('\nWrong input')


def main():
    """
    Runs main functionality of the application
    """
    global db_name
    db_name = 'tweets_table.db'     # initially
    global userid

    if len(sys.argv) == 2:
        if os.path.exists(sys.argv[1]):
            db_name = sys.argv[1]
            print('Connection established with existing database.')
        else:
            db_name = sys.argv[1]
            conn = connect(db_name)
            if conn:
                initiate(conn)
                print('Connection established with new database.')
            else:
                print('Please retry')
    elif len(sys.argv) > 2:
        print('Wrong argument entry')
        print('Use: python main.py [db_name: optional]')
        print('We recommend keeping .db file in the root folder as this python file to avoid path errors')

    while True:
        # after successful initialisation
        try:
            userid, e_code = main_menu()
        except Exception as e:
            print('Some error occured, returning to homepage')
        if e_code == 1:
            return 0
        elif e_code == 2:
            continue
        # tweet functionality
        try:
            exit_code = internal_menu()
        except:
            print('Some error occurred, logging you out.')
        if exit_code == 0:
            return 0
        elif exit_code == 1:
            print('Some error detected')
        elif exit_code == 2:
            userid = None


if __name__ == '__main__':
    main()
