from dotenv import load_dotenv
import os
import google.generativeai as genai

# Load environment variables from .env file
load_dotenv()

# Configure API key for Google Generative AI
genai.configure(api_key=os.environ["API_KEY"])

# Function to generate a question from AI
def generate_question(prompt):
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(prompt)
    return response.text.strip()

# Function to automatically calculate the number of questions based on total marks and marks per type
def calculate_num_questions(total_marks, question_types):
    num_questions = {}
    remaining_marks = total_marks

    for q_type, marks in question_types.items():
        num_questions[q_type] = remaining_marks // marks
        remaining_marks -= num_questions[q_type] * marks
    
    return num_questions

# Function to generate the exam paper
def generate_exam(subject_name, total_marks, selected_types, question_styles, question_types):
    # File path for saving the exam as a .txt file
    txt_file_path = f"{subject_name}_exam_paper.txt"
    
    # Open the text file for writing
    with open(txt_file_path, 'w', encoding='utf-8') as txt_file:
        # Write the exam title and details
        txt_file.write(f"Exam Paper\n")
        txt_file.write(f"Subject: {subject_name}\n")
        txt_file.write(f"Total Marks: {total_marks}\n")
        txt_file.write("\n")

        # Calculate number of questions based on marks
        num_questions = calculate_num_questions(total_marks, {k: question_types[k] for k in selected_types})
        remaining_marks = total_marks
        question_number = 1

        # Generate questions for each selected type
        for q_type in selected_types:
            marks = question_types[q_type]
            for _ in range(num_questions[q_type]):
                if remaining_marks <= 0:
                    break

                # Select prompt based on the question style
                style_prompt = f"{question_styles[q_type]} on {subject_name}."
                
                # Set question prompt based on question type and style
                if q_type == 'MCQ':
                    prompt = f"Create a multiple-choice {style_prompt}"
                elif q_type == 'SAQ':
                    prompt = f"Create a short answer {style_prompt}"

                # Generate the question text
                question_text = generate_question(prompt)

                # Write the question to the text file
                txt_file.write(f"Q{question_number}. {question_text} [{marks} Marks]\n\n")

                # Update the remaining marks and question number
                remaining_marks -= marks
                question_number += 1

    print(f"Exam paper generated and saved as {txt_file_path}")

# Example input for generating the exam paper
subject_name = input("Enter the subject name: ")
total_marks = int(input("Enter the total marks for the exam: "))

# Define question types with corresponding marks per question
question_types = {
    "MCQ": 2,   # Multiple Choice Questions worth 2 marks each
    "VSAQ": 2,  # Very Short Answer Questions worth 2 marks each
    "SAQ": 5,   # Short Answer Questions worth 5 marks each
    "LAQ": 10   # Long Answer Questions worth 10 marks each
}

# Prompt user to select which question types to include
available_types = ["MCQ", "VSAQ", "SAQ", "LAQ"]
selected_types = []
print("Select the question types to include (MCQ, VSAQ, SAQ, LAQ). You can choose any combination.")
for q_type in available_types:
    include = input(f"Include {q_type}? (yes/no): ").strip().lower()
    if include == 'yes':
        selected_types.append(q_type)

# Define question styles (Theoretical, Numerical, Analytical, etc.)
question_styles = {}
for q_type in selected_types:
    question_styles[q_type] = input(f"Enter style for {q_type} (e.g., Theoretical, Numerical, Analytical): ")

# Generate the exam paper and save as a text file
generate_exam(subject_name, total_marks, selected_types, question_styles, question_types)
