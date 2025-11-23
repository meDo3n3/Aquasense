from django.shortcuts import render
import os

def home(request):
    return render(request, 'reservations/index.html')

def courses(request):
    return render(request, 'reservations/courses.html')

from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from .forms import SignUpForm

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'reservations/login.html', {'form': form})

from django.contrib import messages

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created successfully! Please log in.')
            return redirect('login')
    else:
        form = SignUpForm()
    return render(request, 'reservations/signup.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home')

import json
import google.generativeai as genai
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

# Configure Gemini API
# API Key is loaded from .env file
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))


@csrf_exempt
def chat_view(request):
    if request.method == 'POST':
        try:
            # Check if API key exists
            api_key = os.getenv("GEMINI_API_KEY")
            if not api_key:
                print("ERROR: GEMINI_API_KEY not found in environment variables")
                return JsonResponse({
                    'error': 'API key not configured. Please contact support.'
                }, status=500)
            
            print(f"API Key found: {api_key[:10]}...")  # Log first 10 chars only
            
            data = json.loads(request.body)
            user_message = data.get('message', '')
            
            print(f"User message: {user_message}")
            
            # System prompt with business details
            system_prompt = """
            You are the AI Dive Advisor for AquaSense, a premier diving center.
            Your goal is to be helpful, friendly, and professional.
            
            Here is the information about AquaSense:
            - Location: 123 Ocean Drive, Atlantis, Ocean City 90210.
            - Contact: +1 (123) 456-7890, info@divingexcursions.com.
            - Mission: To share the passion of diving through safe, fun, and unforgettable experiences.
            - Founded: 2010.
            
            Courses & Prices:
            1. Open Water Diver: $350 (Beginner's access)
            2. Advanced Diving Skills: $450 (Enhance skills)
            3. Coral Reef Exploration: $200 (Marine life)
            4. Wreck Diving: $500 (Shipwreck adventures)
            
            If the user asks for a recommendation, ask them about their experience level and interests.
            Keep responses concise (under 100 words) unless detailed info is requested.
            """
            
            print("Initializing Gemini model...")
            model = genai.GenerativeModel('gemini-2.0-flash')
            chat = model.start_chat(history=[
                {'role': 'user', 'parts': [system_prompt]},
                {'role': 'model', 'parts': ["Understood. I am ready to assist AquaSense customers."]}
            ])
            
            print("Sending message to Gemini...")
            response = chat.send_message(user_message)
            print(f"Response received: {response.text[:50]}...")
            
            return JsonResponse({'response': response.text})
            
        except Exception as e:
            error_msg = str(e)
            print(f"ERROR in chat_view: {error_msg}")
            import traceback
            traceback.print_exc()
            
            # Return more specific error
            return JsonResponse({
                'error': f'Chat service error: {error_msg}'
            }, status=500)
    
    return JsonResponse({'error': 'Invalid request'}, status=400)

def details(request):
    return render(request, 'reservations/details.html')

def checkout(request):
    return render(request, 'reservations/checkout.html')

def about(request):
    return render(request, 'reservations/about.html')

def contact(request):
    return render(request, 'reservations/contact.html')
