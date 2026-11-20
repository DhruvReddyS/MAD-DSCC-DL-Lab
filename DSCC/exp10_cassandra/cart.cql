CREATE KEYSPACE IF NOT EXISTS store
WITH REPLICATION = {'class': 'SimpleStrategy', 'replication_factor': 1};
USE store;

CREATE TABLE IF NOT EXISTS shopping_cart (
    userid text PRIMARY KEY,
    item_count int,
    last_update_timestamp timestamp
);

-- CREATE (insert)
INSERT INTO shopping_cart (userid, item_count, last_update_timestamp)
VALUES ('9876', 2, toTimestamp(now()));
INSERT INTO shopping_cart (userid, item_count, last_update_timestamp)
VALUES ('1234', 5, toTimestamp(now()));
-- READ
SELECT * FROM shopping_cart;
-- UPDATE
UPDATE shopping_cart SET item_count = 7 WHERE userid = '9876';
-- DELETE
DELETE FROM shopping_cart WHERE userid = '1234';
SELECT * FROM shopping_cart;
