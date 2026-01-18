import os
import json
import random
import functions_framework
import flask
from flask import jsonify
import google.generativeai as genai

# Configure Gemini API
# In a production environment, use os.environ.get("GEMINI_API_KEY")
# For this deployment, we will set it directly as requested.
API_KEY = "AIzaSyDSPSxYzXHwNNV6goNZjDBGyiCAmyz4DJA"
genai.configure(api_key=API_KEY)

# Curated list of fun, distinct themes to ensure variety
RANDOM_THEMES = [
    "The 1980s", "Pirates", "Vampires", "Space Exploration", "Deep Sea", 
    "The Circus", "Kitchen Utensils", "Camping", "Hollywood Movies", "School Subjects",
    "Farm Animals", "Countries of Europe", "Types of Cheese", "Olympic Sports",
    "Harry Potter", "Star Wars", "Superheroes", "Dinosaurs", "Ancient Egypt",
    "Tools", "Musical Instruments", "Fruits", "Cars", "Famous Cities",
    "Winter Olympics", "Desserts", "Board Games", "Video Games", "Insects",
    "Flowers", "Medieval Times", "Office Supplies", "Jobs", "Hobbies",
    "The Jungle", "The Desert", "Islands", "Types of Pasta", "Vegetables",
    "Clothing", "Furniture", "Electronics", "Birds", "Fish", "Holidays"
]

@functions_framework.http
def imposter_game(request: flask.Request):
    """
    HTTP Cloud Function that acts as the backend for the Imposter game.
    Handles serving the frontend and the AI generation API.
    """
    
    # CORS headers
    headers = {
        'Access-Control-Allow-Origin': '*'
    }
    
    if request.method == 'OPTIONS':
        options_headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET, POST',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Max-Age': '3600'
        }
        return ('', 204, options_headers)

    # ROUTE 1: Serve Static HTML
    if request.path == "/" or request.path == "/index.html":
        try:
            print(f"DEBUG: Handling request for {request.path}")
            print(f"DEBUG: Unknown CWD: {os.getcwd()}")
            print(f"DEBUG: Listing CWD: {os.listdir(os.getcwd())}")
            
            # Try absolute path first
            base_dir = os.path.dirname(os.path.abspath(__file__))
            print(f"DEBUG: Base Dir: {base_dir}")
            template_path = os.path.join(base_dir, "templates/index.html")
            print(f"DEBUG: Target Path: {template_path}")
            
            if os.path.exists(template_path):
                 with open(template_path, "r") as f:
                    content = f.read()
            else:
                # Fallback to simple relative path
                print("DEBUG: Absolute path failed, trying relative 'templates/index.html'")
                with open("templates/index.html", "r") as f:
                    content = f.read()
            
            return (content, 200, headers)
        except Exception as e:
            print(f"ERROR: {str(e)}")
            return (f"Error loading game interface: {str(e)}", 500, headers)

    # ROUTE 2: API Generation
    if request.path == "/api/generate" and request.method == "POST":
        try:
            req_json = request.get_json(silent=True)
            if not req_json:
                return (jsonify({"error": "Invalid JSON"}), 400, headers)
                
            input_category = req_json.get("category", "").strip() or "Random"
            
            # Select strict category
            if input_category.lower() in ["random", "general knowledge", ""]:
                target_category = random.choice(RANDOM_THEMES)
            else:
                target_category = input_category
            
            prompt = f"""
            You are a game engine for a 'Spyfall'-style party game.
            
            Task:
            1. Generate 20 simple, distinct, SINGLE-WORD nouns related EXACTLY to the theme: '{target_category}'.
            2. The words MUST be one word only (e.g. "Car" not "Race Car", "Beach" not "Sandy Beach").
            3. They should be distinct places, objects, or concepts that allow for subtle hints.
            
            Return ONLY valid JSON in this format:
            {{
                "category": "{target_category}",
                "words": ["Word1", "Word2", "Word3", ...]
            }}
            Do not include markdown formatting.
            """
            
            # Try multiple model versions for robustness
            # Based on available models for this key
            model_names = [
                'gemini-2.0-flash',
                'gemini-2.0-flash-lite',
                'gemini-flash-latest',
                'gemini-pro-latest'
            ]
            
            response = None
            last_error = None
            
            for m_name in model_names:
                try:
                    print(f"Proping model: {m_name}")
                    model = genai.GenerativeModel(m_name)
                    response = model.generate_content(prompt)
                    if response:
                        break
                except Exception as e:
                    print(f"Model {m_name} failed: {e}")
                    last_error = e
            
            if not response:
                raise last_error or Exception("All models failed")
                
            text = response.text.strip()
            
            # Sanitize response
            if text.startswith("```json"):
                text = text[7:]
            elif text.startswith("```"):
                text = text[3:]
            
            if text.endswith("```"):
                text = text[:-3]
            
            data = json.loads(text.strip())
            
            # Validate structure
            if "category" not in data or "words" not in data:
                 # Fallback for older model behavior if it returns just a list
                 if isinstance(data, list):
                     data = {"category": category, "words": data}
                 else:
                     raise Exception("Invalid JSON structure")
            
            return (jsonify(data), 200, headers)
            
        except Exception as e:
            print(f"Error in /api/generate: {e}")
            return (jsonify({"error": str(e)}), 500, headers)

    return ("Not Found", 404, headers)
