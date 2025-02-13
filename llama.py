import os
from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage, AssistantMessage
from azure.core.credentials import AzureKeyCredential
import datetime
import json
import time

# Load environment variables
endpoint = "https://models.inference.ai.azure.com"
model_name = "Meta-Llama-3.1-405B-Instruct"
token = os.environ.get("GITHUB_TOKEN")

if not token:
    raise ValueError("Please set the GITHUB_TOKEN environment variable.")

# Initialize the ChatCompletionsClient
client = ChatCompletionsClient(
    endpoint=endpoint,
    credential=AzureKeyCredential(token),
)

# Helper function for loading data from json
def load_data(file_path):
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            return json.load(f)
    return {}

# Helper function for saving data to json
def save_data(file_path, data):
    with open(file_path, "w") as f:
        json.dump(data, f, indent=4)

# Initialize Healthcare professionals data
healthcare_professionals_file = "healthcare_professionals.json"
healthcare_professionals = load_data(healthcare_professionals_file)
if not healthcare_professionals:
    healthcare_professionals = {
        "1": {"name": "Dr. John Smith", "specialty": "General Physician", "location" : "123 Main Street", "phone" : "555-1234"},
        "2": {"name": "Dr. Jane Doe", "specialty": "Physiotherapist", "location" : "456 Oak Street", "phone" : "555-5678"},
        "3": {"name": "Dr. Michael Brown", "specialty": "Cardiologist", "location" : "789 Pine Street", "phone" : "555-9012"}
    }
    save_data(healthcare_professionals_file, healthcare_professionals)

class UserProfile:
    def __init__(self, user_id, name = None):
        self.user_id = user_id
        self.name = name
        self.medical_history = {}
        self.dietary_preferences = {}
        self.activity_levels = {}
        self.goals = {}
        self.progress = {}
        self.calendar = {}
        self.biometrics = {}
        self.soundscape = None

    def to_json(self):
        return json.dumps(self.__dict__)
    def from_json(self, data):
        self.__dict__.update(json.loads(data))

class AIHealthEngine:
    def __init__(self, client, model_name):
        self.client = client
        self.model_name = model_name
        self.system_message = SystemMessage(
            content="You are a helpful health and wellness assistant. Provide personalized guidance on diet, exercise, and stress management. Analyze both text queries and image descriptions to offer appropriate advice. Ask follow up questions if needed to provide better responses. Ask questions if you need any clarification. Maintain context from previous interactions. You should strive to make use of external tools wherever possible."
        )
        self.messages = [self.system_message]

    def get_response(self, user_message):
      self.messages.append(UserMessage(content=user_message))
      try:
        response = client.complete(messages=self.messages, model=self.model_name, temperature=0.7)
        if response.choices:
          ai_response = response.choices[0].message.content
          self.messages.append(AssistantMessage(content=ai_response))
          return ai_response
        else:
          return None
      except Exception as e:
        return f"Error: {e}"

    def simulate_image_analysis(self, user_input):
      print("\nSimulating Llama-3.2-90B-Vision-Instruct image analysis...")
      print("Please provide a description of what is visible in the image")
      image_description = input("Image Description: ")
      return f"Image description: {image_description}. Please take this into consideration with your response"

    def call_function(self, function_name, parameters):
        print("\nSimulating a function call...")
        if function_name == "get_calendar":
            return self._get_calendar_entries(parameters)
        elif function_name == "add_calendar_entry":
            return self._add_calendar_entry(parameters)
        elif function_name == "search_healthcare_professionals":
           return self._search_healthcare_professionals(parameters)
        elif function_name == "set_biometrics":
            return self._set_biometrics(parameters)
        else:
            return f"Function '{function_name}' is not supported."

    def _get_calendar_entries(self, parameters):
        # For simplicity, we assume user is always current.
        print("getting current user.")
        start_date = parameters.get("start_date")
        end_date = parameters.get("end_date")
        if start_date and end_date:
          return f"Getting calendar for {start_date} to {end_date}"
        else:
            return "Start and end dates not provided"
    def _add_calendar_entry(self, parameters):
         date = parameters.get("date")
         time = parameters.get("time")
         activity = parameters.get("activity")
         if date and time and activity:
            return f"Adding entry on {date} at {time} for {activity}"
         else:
            return f"Could not add calendar entry, please specify date, time and activity."
    def _search_healthcare_professionals(self, parameters):
         specialty = parameters.get("specialty")
         if specialty:
            results = [professional for id, professional in healthcare_professionals.items() if professional["specialty"].lower() == specialty.lower()]
            if results:
              return f"Found matching healthcare professionals: {results}"
            else:
              return "Could not find matching healthcare professionals"
         else:
            return "Please enter a specialty"
    def _set_biometrics(self, parameters):
        type = parameters.get("type")
        value = parameters.get("value")
        user_id = parameters.get("user_id")
        if type and value:
            return f"Setting biometrics for {user_id} with type {type} and value {value}"
        else:
             return "Please specify biometrics type and value."

    def clear_history(self):
      self.messages = [self.system_message]

    def sentiment_analysis(self, user_message):
        # Placeholder for sentiment analysis functionality.
        # In a real application this would be a separate AI model for sentiment analysis.
        # For now we are returning a basic positive/neutral/negative
        return "positive"

    def get_educational_module(self, module_name):
        modules = {
             "basic_nutrition" : "A balanced diet consists of carbohydrates, proteins, and fats. Remember to drink plenty of water throughout the day.",
              "stress_management": "Try deep breathing exercises or meditation to help manage stress.",
               "basic_exercise": "Try to perform 30 minutes of exercise at least 3 times per week"
         }
        return modules.get(module_name, "Module not available")

    def monitor_environment(self):
        # Placeholder function for monitoring air quality
        air_quality_level = "moderate"
        if "pollution" in self.messages[-1].content.lower():
           if "very bad" in self.messages[-1].content.lower():
             air_quality_level = "very bad"
           else:
              air_quality_level = "bad"
        if air_quality_level == "bad":
           return f"Air quality is {air_quality_level}, limit outdoor activities"
        elif air_quality_level == "very bad":
           return f"Air quality is {air_quality_level}, stay indoors"
        else:
             return f"Air quality is {air_quality_level}"

    def play_soundscape(self, soundscape_name):
        print("\nPlaying selected soundscape...")
        time.sleep(2)
        return f"playing: {soundscape_name}"

def format_output(output):
    # Format output for the user to be more readable.
    print("\n------------------")
    print(output)
    print("------------------")

def handle_input(ai_engine, user_profile):
    print("\nWhat would you like to do?")
    print("1. Text query for health advice")
    print("2. Submit an image for health assessment")
    print("3. Add a calendar entry")
    print("4. Get calendar entries")
    print("5. Search healthcare professionals")
    print("6. Set biometrics data")
    print("7. Request educational content")
    print("8. Monitor environment")
    print("9. Play Soundscapes")
    print("10. Clear Conversation History")
    print("11. Exit")

    choice = input("Enter your choice (1 - 11): ")
    if choice == "1":
        while True:
            user_input = input("You: (Type 'menu' to go back to the main menu): ")
            if user_input.lower() == "menu":
                break
            sentiment = ai_engine.sentiment_analysis(user_input)
            if sentiment == "negative":
                print("I can sense you might be feeling distressed, please remember to consult with a healthcare professional if your symptoms get worse.")
            response = ai_engine.get_response(user_input)
            format_output(response)

    elif choice == "2":
      user_input = ai_engine.simulate_image_analysis("")
      response = ai_engine.get_response(user_input)
      format_output(response)

    elif choice == "3":
      date = input("Enter date (YYYY-MM-DD): ")
      time = input("Enter time (HH:MM): ")
      activity = input("Enter activity: ")
      parameters = { "date" : date, "time": time, "activity": activity }
      response = ai_engine.call_function("add_calendar_entry", parameters)
      format_output(response)

    elif choice == "4":
      start_date = input("Enter start date for calendar entries (YYYY-MM-DD): ")
      end_date = input("Enter end date for calendar entries (YYYY-MM-DD): ")
      parameters = { "start_date" : start_date, "end_date" : end_date}
      response = ai_engine.call_function("get_calendar", parameters)
      format_output(response)

    elif choice == "5":
      specialty = input("Enter specialty for healthcare professional: ")
      parameters = { "specialty" : specialty }
      response = ai_engine.call_function("search_healthcare_professionals", parameters)
      format_output(response)

    elif choice == "6":
        type = input("Enter biometric type (weight, blood pressure, etc.): ")
        value = input("Enter biometric value: ")
        parameters = { "type" : type, "value": value, "user_id": user_profile.user_id }
        response = ai_engine.call_function("set_biometrics", parameters)
        user_profile.biometrics[type] = value
        save_data(f"{user_profile.user_id}_profile.json", user_profile.to_json())
        format_output(response)
    elif choice == "7":
        module_name = input("Enter the name of the educational module: (basic_nutrition, stress_management, basic_exercise) ")
        module_content = ai_engine.get_educational_module(module_name)
        format_output(module_content)

    elif choice == "8":
        env_response = ai_engine.monitor_environment()
        format_output(env_response)

    elif choice == "9":
        soundscape_name = input("Enter soundscape to play (forest, beach, rain): ")
        sound_response = ai_engine.play_soundscape(soundscape_name)
        user_profile.soundscape = soundscape_name
        save_data(f"{user_profile.user_id}_profile.json", user_profile.to_json())
        format_output(sound_response)

    elif choice == "10":
        ai_engine.clear_history()
        print("Conversation History Cleared.")
    elif choice == "11":
        print("Exiting the program...")
        save_data(f"{user_profile.user_id}_profile.json", user_profile.to_json())
        return False
    else:
        print("Invalid choice, please choose a valid option")
    return True


# Initialize user profile and AI engine
user_profile_file = "user123_profile.json"
if os.path.exists(user_profile_file):
    with open(user_profile_file, "r") as f:
        user_profile = UserProfile(user_id="user123")
        user_profile.from_json(f.read())
else:
    user_profile = UserProfile(user_id="user123", name="Test User")
ai_engine = AIHealthEngine(client, model_name)

# Main loop
while True:
    if not handle_input(ai_engine, user_profile):
        break

client.close()