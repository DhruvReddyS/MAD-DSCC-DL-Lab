CREATE DATABASE test;
USE test;

CREATE TABLE student (
    id INT PRIMARY KEY,
    name VARCHAR(50),
    marks INT
);

-- CREATE (insert)
INSERT INTO student VALUES (1, 'Adithya', 85), (2, 'Ravi', 72);
-- READ
SELECT * FROM student;
-- UPDATE
UPDATE student SET marks = 90 WHERE id = 1;
SELECT * FROM student;
-- DELETE
DELETE FROM student WHERE id = 2;
SELECT * FROM student;
