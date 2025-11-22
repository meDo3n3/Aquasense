import google.generativeai as genai
import os

# Use the API key from the user's code
genai.configure(api_key="AIzaSyD2XYcghB818uiaKhPjSBrP5dOUUGb34ZQ")

print("Listing available models...")
try:
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(m.name)
except Exception as e:
    print(f"Error: {e}")
