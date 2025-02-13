import time
import os
from dotenv import load_dotenv
import google.generativeai as genai
import yt_dlp

# Load environment variables from the .env file
load_dotenv()

# Configure the GenAI API with the API key from the .env file
genai.configure(api_key=os.environ["API_KEY"])

# Download the video from video using yt-dlp
video_url = "https://youtu.be/r773-Cv8mK4?si=179a5EY-UpM1IxcX"
output_path = "media/Downloaded_Video.mp4"

# Specify yt-dlp options
ydl_opts = {
    'format': 'best',  # Get the highest quality available
    'outtmpl': output_path,  # Save the file to the specified path
}

# Download the video
with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    ydl.download([video_url])

print(f"Video downloaded at: {output_path}")

# Upload the file using GenAI
myfile = genai.upload_file(output_path)
print(f"{myfile=}")

# Videos need to be processed before you can use them.
while myfile.state.name == "PROCESSING":
    print("processing video...")
    time.sleep(15)
    myfile = genai.get_file(myfile.name)

# Generate content using GenAI to describe the video clip
model = genai.GenerativeModel("gemini-1.5-pro")
result = model.generate_content([myfile, "Describe this video clip shown between 0:00 and 0:10."])
print(f"{result.text=}")