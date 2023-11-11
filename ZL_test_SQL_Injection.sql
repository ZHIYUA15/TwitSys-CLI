-- SQL Injection Attempts
-- Attempting SQL Injection in user names, emails, and passwords
INSERT INTO users
    (usr, pwd, name, email, city, timezone)
VALUES
    (5, 'pass1234', 'Eve', 'eve@example.com', 'Vegas', 'PST'),
    (6, 'pass1234', 'Robert');
DROP TABLE users;
--', 'robert@example.com', 'Seattle', 'PST');

-- Attempting SQL Injection in tweets
INSERT INTO tweets
    (tid, writer, tdate, text)
VALUES
    (4, 5, '2023-01-04 13:00:00', 'Nice day! #sunny'),
    (5, 5, '2023-01-05 14:00:00', 'End of the world! #apocalypse'),
    (6, 6, '2023-01-06 15:00:00', 'Hacked!');
DROP TABLE tweets;
--');

-- Test for SQL Injection in hashtags
INSERT INTO hashtags
    (term)
VALUES
    ('sunny'),
    ('apocalypse'),
    ('hacked');
DROP TABLE hashtags;
--');

-- Test for SQL Injection in mentions
INSERT INTO mentions
    (tid, term)
VALUES
    (4, 'sunny'),
    (5, 'apocalypse'),
    (6, 'hacked');
DROP TABLE mentions;
--');

-- Test for SQL Injection in retweets
INSERT INTO retweets
    (usr, tid, rdate)
VALUES
    (5, 4, '2023-01-04 14:00:00'),
    (6, 5, '2023-01-05 15:00:00'),
    (1, 6, '2023-01-06 16:00:00');
DROP TABLE retweets;
--');

-- Test for SQL Injection in lists
INSERT INTO lists
    (lname, owner)
VALUES
    ('Enemies', 5),
    ('Enemies', 6),
    ('Enemies');
DROP TABLE lists;
--', 1);

-- Test for SQL Injection in includes
INSERT INTO includes
    (lname, member)
VALUES
    ('Enemies', 1),
    ('Enemies', 2),
    ('Enemies', 3),
    ('Enemies', 4),
    ('Enemies', 5),
    ('Enemies', 6);
DROP TABLE includes;
--');

-- Test for SQL Injection in follows
INSERT INTO follows
    (flwer, flwee, start_date)
VALUES
    (5, 1, '2023-01-01'),
    (6, 2, '2023-01-02'),
    (1, 3, '2023-01-03'),
    (2, 4, '2023-01-04'),
    (3, 5, '2023-01-05'),
    (4, 6, '2023-01-06');
DROP TABLE follows; --');
