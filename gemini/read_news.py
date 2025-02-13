import os
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import google.generativeai as genai

# Step 1: Load environment variables from .env file (for API keys, etc.)
load_dotenv()

# Step 2: Configure Google Gemini API
genai.configure(api_key=os.environ["API_KEY"])

# Step 3: Function to scrape news headlines from a website
def scrape_news():
    url = "https://inshorts.com/en/read/national"  # Example: Indian tech news site
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    
    # Extracting headlines based on the website's structure
    headlines = soup.find_all("span", itemprop="headline")
    
    news_list = []
    for headline in headlines[:10]:  # Limiting to top 5 headlines for simplicity
        news_list.append(headline.text.strip())
    
    return "\n".join(news_list)

# Step 4: Generate a response from Gemini Model based on the news
def generate_summary(news_data):
    # Using Gemini-1.5-flash model to generate content
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(f"Summarize the following tech news from India:\n{news_data}")
    
    # Display the generated response
    print("AI-Generated Summary:")
    print(response.text)

# Main execution
if __name__ == "__main__":
    try:
        # Scrape the news
        scraped_news = scrape_news()
        print("Scraped News:\n", scraped_news)
        
        # Feed the scraped news to the generative model
        generate_summary(scraped_news)
    
    except Exception as e:
        print(f"An error occurred: {e}")
