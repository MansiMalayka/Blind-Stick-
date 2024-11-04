import tkinter as tk
import pyttsx3
import requests
import json

# Initialize text-to-speech engine
engine = pyttsx3.init()

# Function to convert text to speech
def speak_text(text):
    engine.say(text)
    engine.runAndWait()

# Function to fetch weather data for Vellore Katpadi
def get_weather():
    city = "Vellore Katpadi"
    api_key = 'H4MQ7T5QHSQS9DTUURS5BE2E2'  # Replace with your Visual Crossing API key
    base_url = f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{city}?unitGroup=metric&key={api_key}&contentType=json"
    
    try:
        response = requests.get(base_url)
        data = response.json()
        
        if "error" in data:
            return f"Error: {data['error']['description']}"
        
        # Fetching weather details for the next few hours
        temp = data['days'][0]['temp']
        condition = data['days'][0]['conditions']
        description = f"The weather in {city} for the coming hours is {condition} with a temperature of {temp}°C."
        return description
    except Exception as e:
        return f"Failed to fetch weather data: {str(e)}"

# Button callback function
def get_weather_report():
    weather_summary = get_weather()
    print(weather_summary)
    speak_text(weather_summary)

# Create GUI
root = tk.Tk()
root.title("Weather Report for Vellore")

# Add a button to trigger weather report
button = tk.Button(root, text="Get Weather Report", command=get_weather_report, height=2, width=20)
button.pack(pady=20)

# Start the GUI event loop
root.mainloop()
