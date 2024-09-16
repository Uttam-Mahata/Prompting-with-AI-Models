from dotenv import load_dotenv
import os
import google.generativeai as genai

load_dotenv()  # Load environment variables from .env file

genai.configure(api_key=os.environ["API_KEY"])

model = genai.GenerativeModel("gemini-1.5-flash")
response = model.generate_content("Write a summary of the following text:\n\nThe quick brown fox jumps over the lazy dog.") 
# Show Markdown formatted text
print(response.text)

