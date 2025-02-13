from dotenv import load_dotenv
import os
import google.generativeai as genai

# Load environment variables from .env file
load_dotenv()

# Configure API key for Google Generative AI
genai.configure(api_key=os.environ["API_KEY"])

# Define the path to the PDF file
media_dir = "media"  # Directory where the file is located
pdf_file = "test.pdf"  # Name of the PDF file
pdf_path = os.path.join(media_dir, pdf_file)

# Check if the file exists
if os.path.exists(pdf_path):
    # Upload the file
    sample_pdf = genai.upload_file(pdf_path)
    
    # Generate content based on the PDF (e.g., a summary)
    response = genai.GenerativeModel("gemini-1.5-flash").generate_content([f"Give me a summary of this document:", sample_pdf])
    
    # Output the summary
    print(f"Summary: {response.text}")
else:
    print(f"File not found at {pdf_path}")
