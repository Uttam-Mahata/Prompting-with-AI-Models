from dotenv import load_dotenv
import os
import google.generativeai as genai
import PyPDF2

# Load environment variables from .env file
load_dotenv()

# Configure the Generative AI API
genai.configure(api_key=os.environ["API_KEY"])

# Function to read PDF content
def read_pdf(file_path):
    with open(file_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        pdf_text = ""
        for page in range(len(reader.pages)):
            pdf_text += reader.pages[page].extract_text()
    return pdf_text

# Function to write LaTeX content to a file
def write_to_latex(file_name, content):
    with open(file_name, 'w') as file:
        file.write(content)

# Read the PDF file content (assume the input file is a PDF)
pdf_content = read_pdf('ac.pdf')  # Replace with your PDF file name

# Dynamically create a prompt based on the PDF content
prompt = f"Based on the following content, create a set of questions that are saved in LaTeX format: {pdf_content}"

# Generate a response using the Generative AI model
model = genai.GenerativeModel("gemini-1.5-flash")
response = model.generate_content(prompt)

# Convert the response to LaTeX format (you can modify this based on how you want LaTeX formatting)
latex_content = f"\\documentclass{{article}}\n\\begin{{document}}\n{response.text}\n\\end{{document}}"

# Save the LaTeX content to a .tex file
output_file = 'generated_questions.tex'  # You can name the file as needed
write_to_latex(output_file, latex_content)

# Print confirmation and location of the saved file
print(f"LaTeX formatted questions saved to {output_file}")
