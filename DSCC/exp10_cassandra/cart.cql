-- Step 5: Create Keyspace
CREATE KEYSPACE IF NOT EXISTS store
WITH REPLICATION = {
'class': 'SimpleStrategy',
'replication_factor': 1
};

USE store;

-- Step 6: Create Table
CREATE TABLE shopping_cart (
  userid text PRIMARY KEY,
  item_count int,
  last_update_timestamp timestamp
);

-- Step 7: CRUD Operations
-- INSERT
INSERT INTO shopping_cart
(userid, item_count, last_update_timestamp)
VALUES ('9876', 2, toTimestamp(now()));

INSERT INTO shopping_cart
(userid, item_count, last_update_timestamp)
VALUES ('1234', 5, toTimestamp(now()));

-- READ
SELECT * FROM shopping_cart;

-- UPDATE
UPDATE shopping_cart
SET item_count = 5,
last_update_timestamp = toTimestamp(now())
WHERE userid = '9876';

-- DELETE
DELETE FROM shopping_cart
WHERE userid = '1234';
