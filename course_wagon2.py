import os
import google.generativeai as genai
import markdown2
import sqlite3
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure Gemini API
genai.configure(api_key=os.getenv("API_KEY"))

# Database connection using SQLite3
conn = sqlite3.connect('course_generator.db')
cursor = conn.cursor()

# Create necessary tables if they don't exist
def create_tables():
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Courses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        course_name TEXT UNIQUE NOT NULL,
        course_description TEXT NOT NULL
    )
    ''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Subjects (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        course_name TEXT,
        subject_name TEXT NOT NULL,
        FOREIGN KEY (course_name) REFERENCES Courses(course_name)
    )
    ''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Modules (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        course_name TEXT,
        subject_name TEXT,
        module_name TEXT NOT NULL,
        FOREIGN KEY (course_name) REFERENCES Courses(course_name),
        FOREIGN KEY (subject_name) REFERENCES Subjects(subject_name)
    )
    ''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Topics (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        course_name TEXT,
        subject_name TEXT,
        module_name TEXT,
        topic_name TEXT NOT NULL,
        topic_content TEXT NOT NULL,
        FOREIGN KEY (course_name) REFERENCES Courses(course_name),
        FOREIGN KEY (subject_name) REFERENCES Subjects(subject_name),
        FOREIGN KEY (module_name) REFERENCES Modules(module_name)
    )
    ''')
    
    conn.commit()

# Function to generate content using the Gemini API
def generate_content(prompt):
    model = genai.GenerativeModel("gemini-1.5-pro")
    response = model.generate_content(prompt)
    return markdown2.markdown(response.text, extras=["strip"])

# Function to add course to the database
def add_course_to_db(course_name, course_description):
    cursor.execute(
        "INSERT OR IGNORE INTO Courses (course_name, course_description) VALUES (?, ?)", 
        (course_name, course_description)
    )
    conn.commit()

# Function to add subjects, modules, and topics into the database
def add_subject_to_db(course_name, subject_name):
    cursor.execute(
        "INSERT INTO Subjects (course_name, subject_name) VALUES (?, ?)", 
        (course_name, subject_name)
    )
    conn.commit()

def add_module_to_db(course_name, subject_name, module_name):
    cursor.execute(
        "INSERT INTO Modules (course_name, subject_name, module_name) VALUES (?, ?, ?)", 
        (course_name, subject_name, module_name)
    )
    conn.commit()

def add_topic_to_db(course_name, subject_name, module_name, topic_name, topic_content):
    cursor.execute(
        "INSERT INTO Topics (course_name, subject_name, module_name, topic_name, topic_content) VALUES (?, ?, ?, ?, ?)", 
        (course_name, subject_name, module_name, topic_name, topic_content)
    )
    conn.commit()

# Generate Course Description
def generate_course_description(course_name):
    prompt = f"Generate a detailed course description for the course '{course_name}'"
    return generate_content(prompt)

# Generate Subjects
def generate_subjects(course_name):
    prompt = f"List  main subjects for the course '{course_name}'. Suppose Course is XI SCIENCE. Then Subjects should be like Mathematics, Physics, Chemistry, Biology"
    subjects = generate_content(prompt).split("\n")
    subjects = [subject for subject in subjects if subject]  # Clean up empty lines
    return subjects

# Generate Modules for a Subject
def generate_modules(course_name, subject_name):
    prompt = f"List  module names for the subject '{subject_name}' in the course '{course_name}'. Suppose subject is Physics then Module names shoulf be like Physical World and Measurements, Mition in 1 Dimension, Vectors etc.."
    modules = generate_content(prompt).split("\n")
    modules = [module for module in modules if module]  # Clean up empty lines
    return modules

# Generate Topics for a Module
def generate_topics(course_name, subject_name, module_name):
    prompt = f"""List  topic names for the module '{module_name}' in the subject '{subject_name}' for the course '{course_name}'. Suppose Module is PHYSICS AND MEASUREMENT then topics should be Units of measurements, System of Units, S I Units, fundamental and derived units, least count,
significant figures, Errors in measurements, Dimensions of Physics quantities, dimensional
analysis, and its applications. """
    topics = generate_content(prompt).split("\n")
    topics = [topic for topic in topics if topic]  # Clean up empty lines
    return topics

# Generate Detailed Topic Content
def generate_detailed_topic_content(course_name, subject_name, module_name, topic_name):
    prompt = f"Write a detailed explanation for the topic '{topic_name}' in the module '{module_name}' under the subject '{subject_name}' in the course '{course_name}'"
    return generate_content(prompt)

# Main function to drive the console application
def main():
    # Create tables
    create_tables()

    # Input course name
    course_name = input("Enter Course Name: ")

    # Generate course description
    course_description = generate_course_description(course_name)
    print(f"Generated Course Description:\n{course_description}")

    # Add course to database
    add_course_to_db(course_name, course_description)
    print(f"Course '{course_name}' added to database.")

    # Generate subjects
    subjects = generate_subjects(course_name)
    print(f"Generated Subjects:\n{', '.join(subjects)}")

    for subject in subjects:
        add_subject_to_db(course_name, subject)
        print(f"Subject '{subject}' added to database.")

        # Generate modules for each subject
        modules = generate_modules(course_name, subject)
        print(f"Generated Modules for '{subject}':\n{', '.join(modules)}")

        for module in modules:
            add_module_to_db(course_name, subject, module)
            print(f"Module '{module}' added to database.")

            # Generate topics for each module
            topics = generate_topics(course_name, subject, module)
            print(f"Generated Topics for '{module}':\n{', '.join(topics)}")

            for topic in topics:
                # Generate detailed topic content
                topic_content = generate_detailed_topic_content(course_name, subject, module, topic)
                print(f"Generated Detailed Content for Topic '{topic}':\n{topic_content}")

                # Add topic and its content to database
                add_topic_to_db(course_name, subject, module, topic, topic_content)
                print(f"Topic '{topic}' added to database with detailed content.")

if __name__ == "__main__":
    main()