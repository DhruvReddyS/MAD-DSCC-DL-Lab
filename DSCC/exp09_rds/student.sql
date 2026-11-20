CREATE DATABASE test;
USE test;

CREATE TABLE student (
    id INT PRIMARY KEY,
    name VARCHAR(50),
    marks INT
);

-- INSERT
INSERT INTO student VALUES
(1, 'Adithya', 85);

-- READ
SELECT * FROM student;

-- UPDATE
UPDATE student
SET marks = 90
WHERE id = 1;

-- DELETE
DELETE FROM student
WHERE id = 1;
