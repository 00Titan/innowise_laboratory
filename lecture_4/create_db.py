import os
import sqlite3

# Ensure lecture_4 directory exists and set file paths
os.makedirs("lecture_4", exist_ok=True)
db_path = os.path.join( "school.db")
sql_path = os.path.join("queries.sql")

# Connect to the SQLite database
conn = sqlite3.connect(db_path)
cur = conn.cursor()

# Enable foreign key constraints
cur.execute("PRAGMA foreign_keys = ON")

# Create tables if they do not exist
cur.executescript("""
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
    FOREIGN KEY (student_id) REFERENCES students(id)
        ON DELETE SET NULL
        ON UPDATE CASCADE
);
""")
conn.commit()

# Insert sample students
students_data = [
    ('Alice Johnson', 2005),
    ('Brian Smith', 2004),
    ('Carla Reyes', 2006),
    ('Daniel Kim', 2005),
    ('Eva Thompson', 2003),
    ('Felix Nguyen', 2007),
    ('Grace Patel', 2005),
    ('Henry Lopez', 2004),
    ('Isabella Martinez', 2006)
]
cur.executemany("INSERT INTO students (full_name, birth_year) VALUES (?, ?)", students_data)
conn.commit()

# Build a mapping from student full_name to id
cur.execute("SELECT id, full_name FROM students ORDER BY id")
students_id_map = {name: sid for sid, name in cur.fetchall()}

# Insert sample grades using student ids
grades_data = [
    (students_id_map['Alice Johnson'], 'Math', 88),
    (students_id_map['Alice Johnson'], 'English', 92),
    (students_id_map['Alice Johnson'], 'Science', 85),

    (students_id_map['Brian Smith'], 'Math', 75),
    (students_id_map['Brian Smith'], 'History', 83),
    (students_id_map['Brian Smith'], 'English', 79),

    (students_id_map['Carla Reyes'], 'Science', 95),
    (students_id_map['Carla Reyes'], 'Math', 91),
    (students_id_map['Carla Reyes'], 'Art', 89),

    (students_id_map['Daniel Kim'], 'Math', 84),
    (students_id_map['Daniel Kim'], 'Science', 88),
    (students_id_map['Daniel Kim'], 'Physical Education', 93),

    (students_id_map['Eva Thompson'], 'English', 90),
    (students_id_map['Eva Thompson'], 'History', 85),
    (students_id_map['Eva Thompson'], 'Math', 88),

    (students_id_map['Felix Nguyen'], 'Science', 72),
    (students_id_map['Felix Nguyen'], 'Math', 78),
    (students_id_map['Felix Nguyen'], 'English', 81),

    (students_id_map['Grace Patel'], 'Art', 94),
    (students_id_map['Grace Patel'], 'Science', 87),
    (students_id_map['Grace Patel'], 'Math', 90),

    (students_id_map['Henry Lopez'], 'History', 77),
    (students_id_map['Henry Lopez'], 'Math', 83),
    (students_id_map['Henry Lopez'], 'Science', 80),

    (students_id_map['Isabella Martinez'], 'English', 96),
    (students_id_map['Isabella Martinez'], 'Math', 89),
    (students_id_map['Isabella Martinez'], 'Art', 92)
]
cur.executemany("INSERT INTO grades (student_id, subject, grade) VALUES (?, ?, ?)", grades_data)
conn.commit()

# Create indexes to speed up common queries
cur.executescript("""
CREATE INDEX IF NOT EXISTS idx_grades_student_id ON grades(student_id);
CREATE INDEX IF NOT EXISTS idx_students_full_name ON students(full_name);
CREATE INDEX IF NOT EXISTS idx_grades_subject ON grades(subject);
""")
conn.commit()

# Create a view for average grades per student
cur.execute("DROP VIEW IF EXISTS average_grades")
cur.executescript("""
CREATE VIEW IF NOT EXISTS average_grades AS
SELECT s.id AS student_id, s.full_name, ROUND(AVG(g.grade),2) AS average_grade
FROM students s
LEFT JOIN grades g ON s.id = g.student_id
GROUP BY s.id;
""")
conn.commit()

# Write SQL script (CREATE / INSERT / SELECT / INDEX / VIEW) to file
sql_file_content = f"""
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
"""

cur.execute("SELECT full_name, birth_year FROM students ORDER BY id")
for name, by in cur.fetchall():
    safe_name = name.replace("'", "''")
    sql_file_content += f"INSERT INTO students (full_name, birth_year) VALUES ('{safe_name}', {by});\n"

sql_file_content += "\n-- INSERT GRADES\n"
cur.execute("SELECT student_id, subject, grade FROM grades ORDER BY id")
for sid, subj, gr in cur.fetchall():
    safe_subj = subj.replace("'", "''")
    sql_file_content += f"INSERT INTO grades (student_id, subject, grade) VALUES ({sid}, '{safe_subj}', {gr});\n"

sql_file_content += """
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
"""

with open(sql_path, "w", encoding="utf-8") as f:
    f.write(sql_file_content)

conn.close()