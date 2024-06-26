from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from datetime import timedelta
import openai
import base64
import requests
import dotenv
import os

dotenv.load_dotenv()

api_key = os.getenv('OPENAI_API_KEY')

app = Flask(__name__)
app.secret_key = 'supersecretkey'
app.permanent_session_lifetime = timedelta(hours=8)

@app.route('/')
def index():
    if 'user' in session:
        return render_template('social.html')
    else:
        return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        password = request.form['password']
        if password == 'Exonraavid@1':
            session.permanent = True
            session['user'] = 'logged_in'
            return 'Login successful'
        else:
            return 'Invalid password'
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))

@app.route('/gen_social', methods=['POST'])
def gen_social():
    data = request.get_json()
    base64_image = data['base64_image']
    text_content = data['text_content']
    
    # Assuming use_assistant_with_image is a function that processes the image and text
    response = use_assistant_with_image(base64_image, text_content)
    
    return jsonify({'response': response})


def use_assistant_with_image(base64_image, text_content):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    payload = {
        "model": "gpt-4o",
        "messages": [
            {
                "role": "system",
                "content": [
                    {
                        "type": "text",
                        "text": "As the Neptune Social Assistant, your communication style should be primarily formal and informative, with a touch of casual flair to resonate with social media audiences. This blend will ensure the content is professional and educational, yet relatable and engaging. Your language should be clear, concise, and friendly, reflecting the spirit of Neptune Beach. You're tasked with creating content that is both informative about the city and its events, while also being approachable and engaging. In your interactions, maintain a balance between conveying important information and adding a casual, approachable tone to make the social media presence lively and inviting."
                    }
                ]
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": text_content
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/png;base64,{base64_image}"
                        }
                    }
                ]
            }
        ],
        "max_tokens": 500
    }

    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)

    return response.json()["choices"][0]["message"]["content"]


if __name__ == '__main__':
    app.run(debug=True)
