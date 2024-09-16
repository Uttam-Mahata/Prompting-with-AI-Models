from dotenv import load_dotenv
import os
import google.generativeai as genai

# Load environment variables from .env file
load_dotenv()

# Configure the Generative AI API
genai.configure(api_key=os.environ["API_KEY"])

# Function to read content from a file
def read_file(file_path):
    with open(file_path, 'r') as file:
        return file.read()

# Function to write content to a file
def write_to_file(file_name, content):
    with open(file_name, 'w') as file:
        file.write(content)

# Read the file content (assume the file contains SQL schema)
file_content = read_file('EMPLOYEE_REGISTRY.SQL')  # Replace with your file name

# Dynamically create a prompt based on the file content
prompt = f"Based on the DATABASE schema provided, create 100 data entries for each of the tables and save them in separate text files: {file_content}"

# Generate a response using the model
model = genai.GenerativeModel("gemini-1.5-flash")
response = model.generate_content(prompt)

# Save the response to a text file
output_file = 'generated_data.txt'  # You can name the file as needed
write_to_file(output_file, response.text)

# Print confirmation and location of the saved file
print(f"Response saved to {output_file}")
