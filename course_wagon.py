import os
import sqlite3
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables from .env file
load_dotenv()

# Configure Gemini API
genai.configure(api_key=os.environ["API_KEY"])
model = genai.GenerativeModel("gemini-1.5-flash")

# Set up SQLite database connection
conn = sqlite3.connect('courses.db')
cursor = conn.cursor()

# Create tables
cursor.execute('''
CREATE TABLE IF NOT EXISTS courses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    description TEXT
)
''')
cursor.execute('''
CREATE TABLE IF NOT EXISTS subjects (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    course_id INTEGER,
    FOREIGN KEY (course_id) REFERENCES courses(id)
)
''')
cursor.execute('''
CREATE TABLE IF NOT EXISTS modules (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    subject_id INTEGER,
    FOREIGN KEY (subject_id) REFERENCES subjects(id)
)
''')
cursor.execute('''
CREATE TABLE IF NOT EXISTS topics (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    module_id INTEGER,
    content TEXT,
    FOREIGN KEY (module_id) REFERENCES modules(id)
)
''')
conn.commit()

# Function to create a new course
def create_course():
    course_name = input("Enter the course name: ")
    course_description = input("Enter the course description: ")
    cursor.execute('INSERT INTO courses (name, description) VALUES (?, ?)', (course_name, course_description))
    conn.commit()
    print(f"Course '{course_name}' created successfully.")

    course_id = cursor.lastrowid
    generate_subjects(course_id, course_name)

# Function to generate subjects using Google Gemini API
def generate_subjects(course_id, course_name):
    print("Generating subjects, please wait...")
    response = model.generate_content(f"Generate subjects for the course: {course_name}")
    subject_names = response.text.split("\n")  # Assuming subjects are returned as a list of names

    for subject_name in subject_names:
        cursor.execute('INSERT INTO subjects (name, course_id) VALUES (?, ?)', (subject_name.strip(), course_id))
    conn.commit()

    print(f"Subjects for course '{course_name}' created successfully.")
    subjects = cursor.execute('SELECT * FROM subjects WHERE course_id = ?', (course_id,)).fetchall()
    for subject in subjects:
        print(f"- {subject[1]}")
    
    subject_id = subjects[0][0] if subjects else None
    if subject_id:
        generate_modules(subject_id, subjects[0][1])

# Function to generate modules for a subject
def generate_modules(subject_id, subject_name):
    print(f"\nGenerating modules for subject '{subject_name}', please wait...")
    response = model.generate_content(f"Generate modules for the subject: {subject_name}")
    module_names = response.text.split("\n")

    for module_name in module_names:
        cursor.execute('INSERT INTO modules (name, subject_id) VALUES (?, ?)', (module_name.strip(), subject_id))
    conn.commit()

    print(f"Modules for subject '{subject_name}' created successfully.")
    modules = cursor.execute('SELECT * FROM modules WHERE subject_id = ?', (subject_id,)).fetchall()
    for module in modules:
        print(f"- {module[1]}")
    
    module_id = modules[0][0] if modules else None
    if module_id:
        generate_topics(module_id, modules[0][1])

# Function to generate topics for a module
def generate_topics(module_id, module_name):
    print(f"\nGenerating topics for module '{module_name}', please wait...")
    response = model.generate_content(f"Generate topics for the module from basic to Advanced all topics shoould be given: {module_name}")
    topic_names = response.text.split("\n")

    for topic_name in topic_names:
        cursor.execute('INSERT INTO topics (name, module_id) VALUES (?, ?)', (topic_name.strip(), module_id))
    conn.commit()

    print(f"Topics for module '{module_name}' created successfully.")
    topics = cursor.execute('SELECT * FROM topics WHERE module_id = ?', (module_id,)).fetchall()
    for topic in topics:
        print(f"- {topic[1]}")
    
    topic_id = topics[0][0] if topics else None
    if topic_id:
        generate_content(topic_id, topics[0][1])

# Function to generate content for a topic
def generate_content(topic_id, topic_name):
    print(f"\nGenerating content for topic '{topic_name}', please wait...")
    response = model.generate_content(f"Write content for the topic: {topic_name}")
    content = response.text

    cursor.execute('UPDATE topics SET content = ? WHERE id = ?', (content, topic_id))
    conn.commit()

    print(f"Content for topic '{topic_name}' generated successfully:")
    print(content)

# Main function to run the script
def main():
    print("Welcome to the Course Generator!")
    while True:
        print("\nOptions:")
        print("1. Create new course")
        print("2. Exit")

        choice = input("Enter your choice: ")
        if choice == "1":
            create_course()
        elif choice == "2":
            break
        else:
            print("Invalid option. Please try again.")

if __name__ == "__main__":
    main()
    conn.close()
