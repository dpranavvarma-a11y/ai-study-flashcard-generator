import os
from flask import Flask, render_template, request, jsonify
from google import genai
from google.genai import types

app = Flask(__name__)

# Initialize the Gemini client (Make sure GEMINI_API_KEY is set in your environment variables)
client = genai.Client()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    text_content = request.form.get('notes', '')
    
    prompt = f"""
    Based on the following notes, generate 3 study flashcards (Question & Answer) 
    and 2 multiple-choice quiz questions with options and the correct answer. 
    Keep the structure clean and predictable.

    Notes:
    {text_content}
    """

    try:
        response = client.models.generate_content(
            model='gemini-3.5-flash-lite',
            contents=prompt,
        )
        return jsonify({"result": response.text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)