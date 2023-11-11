-- Test Cases for Edge Cases
-- Inserting follows relationships with edge cases
INSERT INTO follows
    (flwer, flwee, start_date)
VALUES
    (1, 1, '2023-02-09'),
    -- User trying to follow themselves
    (1, 2, '2023-02-10');
-- Duplicate follow

-- Inserting tweets with non-existing hashtags
INSERT INTO tweets
    (tid, writer, tdate, text)
VALUES
    (7, 1, '2023-01-07 16:00:00', 'Unregistered hashtag! #unregistered');

-- Inserting mentions for non-existing tweets
INSERT INTO mentions
    (tid, term)
VALUES
    (999, 'nonexistent');
-- Tweet ID does not exist

-- Inserting retweets for non-existing tweets or users
INSERT INTO retweets
    (usr, tid, rdate)
VALUES
    (999, 1, '2023-01-07 17:00:00'); -- User ID does not exist