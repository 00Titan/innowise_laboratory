
-- CREATE TABLES
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY,
    full_name TEXT NOT NULL,
    birth_year INTEGER
);

CREATE TABLE IF NOT EXISTS grades (
    id INTEGER PRIMARY KEY,
    student_id INTEGER,
    subject TEXT NOT NULL,
    grade INTEGER CHECK (grade BETWEEN 1 AND 100),
    FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE SET NULL ON UPDATE CASCADE
);

-- INSERT STUDENTS
INSERT INTO students (full_name, birth_year) VALUES ('Alice Johnson', 2005);
INSERT INTO students (full_name, birth_year) VALUES ('Brian Smith', 2004);
INSERT INTO students (full_name, birth_year) VALUES ('Carla Reyes', 2006);
INSERT INTO students (full_name, birth_year) VALUES ('Daniel Kim', 2005);
INSERT INTO students (full_name, birth_year) VALUES ('Eva Thompson', 2003);
INSERT INTO students (full_name, birth_year) VALUES ('Felix Nguyen', 2007);
INSERT INTO students (full_name, birth_year) VALUES ('Grace Patel', 2005);
INSERT INTO students (full_name, birth_year) VALUES ('Henry Lopez', 2004);
INSERT INTO students (full_name, birth_year) VALUES ('Isabella Martinez', 2006);

-- INSERT GRADES
INSERT INTO grades (student_id, subject, grade) VALUES (1, 'Math', 88);
INSERT INTO grades (student_id, subject, grade) VALUES (1, 'English', 92);
INSERT INTO grades (student_id, subject, grade) VALUES (1, 'Science', 85);
INSERT INTO grades (student_id, subject, grade) VALUES (2, 'Math', 75);
INSERT INTO grades (student_id, subject, grade) VALUES (2, 'History', 83);
INSERT INTO grades (student_id, subject, grade) VALUES (2, 'English', 79);
INSERT INTO grades (student_id, subject, grade) VALUES (3, 'Science', 95);
INSERT INTO grades (student_id, subject, grade) VALUES (3, 'Math', 91);
INSERT INTO grades (student_id, subject, grade) VALUES (3, 'Art', 89);
INSERT INTO grades (student_id, subject, grade) VALUES (4, 'Math', 84);
INSERT INTO grades (student_id, subject, grade) VALUES (4, 'Science', 88);
INSERT INTO grades (student_id, subject, grade) VALUES (4, 'Physical Education', 93);
INSERT INTO grades (student_id, subject, grade) VALUES (5, 'English', 90);
INSERT INTO grades (student_id, subject, grade) VALUES (5, 'History', 85);
INSERT INTO grades (student_id, subject, grade) VALUES (5, 'Math', 88);
INSERT INTO grades (student_id, subject, grade) VALUES (6, 'Science', 72);
INSERT INTO grades (student_id, subject, grade) VALUES (6, 'Math', 78);
INSERT INTO grades (student_id, subject, grade) VALUES (6, 'English', 81);
INSERT INTO grades (student_id, subject, grade) VALUES (7, 'Art', 94);
INSERT INTO grades (student_id, subject, grade) VALUES (7, 'Science', 87);
INSERT INTO grades (student_id, subject, grade) VALUES (7, 'Math', 90);
INSERT INTO grades (student_id, subject, grade) VALUES (8, 'History', 77);
INSERT INTO grades (student_id, subject, grade) VALUES (8, 'Math', 83);
INSERT INTO grades (student_id, subject, grade) VALUES (8, 'Science', 80);
INSERT INTO grades (student_id, subject, grade) VALUES (9, 'English', 96);
INSERT INTO grades (student_id, subject, grade) VALUES (9, 'Math', 89);
INSERT INTO grades (student_id, subject, grade) VALUES (9, 'Art', 92);

-- 3) All grades for Alice Johnson
SELECT g.subject, g.grade
FROM grades g
JOIN students s ON s.id = g.student_id
WHERE s.full_name = 'Alice Johnson';

-- 4) Average grade per student
SELECT s.id, s.full_name, ROUND(AVG(g.grade),2) AS average_grade
FROM students s
LEFT JOIN grades g ON s.id = g.student_id
GROUP BY s.id;

-- 5) Students born after 2004
SELECT id, full_name, birth_year FROM students WHERE birth_year > 2004;

-- 6) Average grade per subject
SELECT subject, ROUND(AVG(grade), 2) AS average_grade FROM grades GROUP BY subject;

-- 7) Top 3 students with highest average
SELECT s.id, s.full_name, ROUND(AVG(g.grade),2) AS average_grade
FROM students s
JOIN grades g ON s.id = g.student_id
GROUP BY s.id
ORDER BY average_grade DESC
LIMIT 3;

-- 8) Students who scored below 80 in any subject
SELECT DISTINCT s.id, s.full_name, g.subject, g.grade
FROM students s
JOIN grades g ON s.id = g.student_id
WHERE g.grade < 80;

-- INDEXES
CREATE INDEX IF NOT EXISTS idx_grades_student_id ON grades(student_id);
CREATE INDEX IF NOT EXISTS idx_students_full_name ON students(full_name);
CREATE INDEX IF NOT EXISTS idx_grades_subject ON grades(subject);

-- VIEW average_grades
CREATE VIEW IF NOT EXISTS average_grades AS
SELECT s.id AS student_id, s.full_name, ROUND(AVG(g.grade),2) AS average_grade
FROM students s
LEFT JOIN grades g ON s.id = g.student_id
GROUP BY s.id;
