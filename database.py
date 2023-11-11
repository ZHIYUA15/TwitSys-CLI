import sqlite3


def connect_to_db(db_name):
    """
    Responsibility: Establishes a connection to the SQLite database file specified by db_name.

    @Param db_name (str): The name of the database file to connect to.
    @Return: The database connection object or None if the connection fails.
    """
    try:
        conn = sqlite3.connect(db_name)
        return conn
    except sqlite3.Error as e:
        print(f"An error occurred while connecting to the database: {e}")
        return None


def initial_query(conn):
    '''
    Responsibility: Executes a series of SQL queries to create the initial database schema or reset it.

    @Param conn (sqlite3.Connection): The active database connection.
    @Return: None.

    '''
    cur = conn.cursor()
    query = [
        '''DROP TABLE IF EXISTS includes;''',
        '''DROP TABLE IF EXISTS lists;''',
        '''DROP TABLE IF EXISTS retweets;''',
        '''DROP TABLE IF EXISTS mentions;''',
        '''DROP TABLE IF EXISTS hashtags;''',
        '''DROP TABLE IF EXISTS tweets;''',
        '''DROP TABLE IF EXISTS follows;''',
        '''DROP TABLE IF EXISTS users;''',
        '''CREATE TABLE users (
              usr         INT PRIMARY KEY,
              pwd         TEXT NOT NULL,
              name        TEXT NOT NULL,
              email       TEXT NOT NULL,
              city        TEXT,
              timezone    REAL
           );''',
        '''CREATE TABLE follows (
              flwer       INT NOT NULL,
              flwee       INT NOT NULL,
              start_date  DATE NOT NULL,
              PRIMARY KEY (flwer, flwee),
              FOREIGN KEY (flwer) REFERENCES users(usr),
              FOREIGN KEY (flwee) REFERENCES users(usr)
           );''',
        '''CREATE TABLE tweets (
              tid         INTEGER PRIMARY KEY,
              writer      INT NOT NULL,
              tdate       DATE NOT NULL,
              text        TEXT NOT NULL,
              replyto     INT,
              FOREIGN KEY (writer) REFERENCES users(usr),
              FOREIGN KEY (replyto) REFERENCES tweets(tid)
           );''',
        '''CREATE TABLE hashtags (
              term        TEXT PRIMARY KEY
           );''',
        '''CREATE TABLE mentions (
              tid         INT NOT NULL,
              term        TEXT NOT NULL,
              PRIMARY KEY (tid, term),
              FOREIGN KEY (tid) REFERENCES tweets(tid),
              FOREIGN KEY (term) REFERENCES hashtags(term)
           );''',
        '''CREATE TABLE retweets (
              usr         INT NOT NULL,
              tid         INT NOT NULL,
              rdate       DATE NOT NULL,
              PRIMARY KEY (usr, tid),
              FOREIGN KEY (usr) REFERENCES users(usr),
              FOREIGN KEY (tid) REFERENCES tweets(tid)
           );''',
        '''CREATE TABLE lists (
              lname       TEXT PRIMARY KEY,
              owner       INT NOT NULL,
              FOREIGN KEY (owner) REFERENCES users(usr)
           );''',
        '''CREATE TABLE includes (
              lname       TEXT NOT NULL,
              member      INT NOT NULL,
              PRIMARY KEY (lname, member),
              FOREIGN KEY (lname) REFERENCES lists(lname),
              FOREIGN KEY (member) REFERENCES users(usr)
           );'''
    ]
    for q in query:
        cur.execute(q)
    conn.commit()
