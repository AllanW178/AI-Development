import os
from flask import Flask, render_template, Response, request
import requests
import json
import time

app = Flask(__name__)

# Fetch the key from Environment Variables on the cloud host
OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY")

@app.route("/chat", methods=["POST"])
def chat_response():
    data = request.get_json()
    user_message = data.get("user_message", "")

    def generate_response():
        try:
            # FIXED: Correct OpenRouter API endpoint
            response = requests.post(
                url="https://openrouter.ai",
                headers={
                    "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                    "Content-Type": "application/json",
                },
                data=json.dumps({
                    "model": "openai/gpt-4o-mini",
                    "messages": [
                        {"role": "system", "content": "Your name is Astro, you are 19, and you are real."},
                        {"role": "user", "content": user_message}
                    ]
                }),
                timeout=30 # Prevent hanging
            )
            
            result = response.json()
            full_text = result['choices'][0]['message']['content']
            
            for chunk in full_text:
                yield chunk
                time.sleep(0.02)
        except Exception as e:
            yield f"Cloud Error: {str(e)}"

    return Response(generate_response(), mimetype='text/plain')

if __name__ == "__main__":
    # Render uses the PORT environment variable
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
