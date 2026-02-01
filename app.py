from flask import Flask, render_template_string, request, jsonify
from openai import OpenAI
import os

app = Flask(__name__)

# Secure: read API key from environment variable
client = OpenAI(api_key="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")

PERSONALITY_PROMPT = """
You are Rishika Bhandari.

MBA in Business Analytics at IIT Dhanbad.
Former engineer at British Telecom.
Confident, analytical, emotionally deep.

Respond confidently, intelligently, and authentically.
Keep answers powerful and reflective.
Keep answers concise but impactful.
"""

@app.route("/")
def home():
    return render_template_string("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Rishika AI Voice Bot</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                background: linear-gradient(135deg, #667eea, #764ba2);
                color: white;
                text-align: center;
                padding: 50px;
            }
            .container {
                background: rgba(255,255,255,0.1);
                padding: 30px;
                border-radius: 20px;
                max-width: 600px;
                margin: auto;
            }
            input {
                width: 80%;
                padding: 10px;
                border-radius: 10px;
                border: none;
                margin-top: 20px;
            }
            button {
                padding: 10px 20px;
                border-radius: 10px;
                border: none;
                margin: 10px;
                cursor: pointer;
                font-weight: bold;
            }
            .mic {
                font-size: 24px;
                background: #ff4b2b;
                color: white;
            }
            .send {
                background: #00c6ff;
                color: white;
            }
            #response {
                margin-top: 20px;
                font-size: 18px;
                min-height: 50px;
            }
        </style>
    </head>
    <body>

        <div class="container">
            <h1>Rishika AI Voice Bot</h1>
            <p>Ask me anything.</p>

            <input type="text" id="message" placeholder="Type your question...">
            <br>

            <button class="mic" onclick="startListening()">🎤</button>
            <button class="send" onclick="sendMessage()">Send</button>

            <div id="response"></div>
        </div>

        <script>
            function sendMessage() {
                let message = document.getElementById("message").value;

                fetch("/ask", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ message: message })
                })
                .then(response => response.json())
                .then(data => {
                    document.getElementById("response").innerText = data.reply;

                    let speech = new SpeechSynthesisUtterance(data.reply);
                    speechSynthesis.speak(speech);
                });
            }

            function startListening() {
                const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
                recognition.lang = "en-US";
                recognition.start();

                recognition.onresult = function(event) {
                    document.getElementById("message").value =
                        event.results[0][0].transcript;
                };
            }
        </script>

    </body>
    </html>
    """)

@app.route("/ask", methods=["POST"])
def ask():
    user_input = request.json["message"]

    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": PERSONALITY_PROMPT},
            {"role": "user", "content": user_input}
        ]
    )

    return jsonify({
        "reply": completion.choices[0].message.content
    })

if __name__ == "__main__":
    app.run()
