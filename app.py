from flask import Flask, render_template_string, request, jsonify
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

client = OpenAI(api_key="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")

PERSONALITY_PROMPT = """
You are Rishika Bhandari.

MBA in Business Analytics at IIT Dhanbad.
Former engineer at British Telecom.
Confident. Analytical. Emotionally deep.

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
<title>Rishika AI</title>
<meta name="viewport" content="width=device-width, initial-scale=1.0">

<style>
body {
    margin: 0;
    font-family: 'Segoe UI', sans-serif;
    background: linear-gradient(135deg, #1f1c2c, #928dab);
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100vh;
    color: white;
}

.chat-container {
    width: 95%;
    max-width: 700px;
    height: 90vh;
    backdrop-filter: blur(15px);
    background: rgba(255,255,255,0.08);
    border-radius: 25px;
    display: flex;
    flex-direction: column;
    box-shadow: 0 20px 40px rgba(0,0,0,0.4);
    overflow: hidden;
}

.header {
    padding: 20px;
    text-align: center;
    font-size: 22px;
    font-weight: bold;
    background: rgba(0,0,0,0.2);
}

.chat-box {
    flex: 1;
    padding: 20px;
    overflow-y: auto;
}

.message {
    margin-bottom: 15px;
    padding: 12px 16px;
    border-radius: 18px;
    max-width: 75%;
    animation: fadeIn 0.3s ease-in-out;
}

.user {
    background: #00c6ff;
    align-self: flex-end;
    color: black;
}

.bot {
    background: rgba(255,255,255,0.2);
}

.input-area {
    display: flex;
    padding: 15px;
    background: rgba(0,0,0,0.2);
}

input {
    flex: 1;
    padding: 12px;
    border-radius: 25px;
    border: none;
    outline: none;
}

button {
    margin-left: 10px;
    border: none;
    padding: 10px 15px;
    border-radius: 50%;
    cursor: pointer;
    font-size: 18px;
    transition: 0.3s;
}

.send {
    background: #00c6ff;
    color: black;
}

.mic {
    background: #ff4b2b;
    color: white;
}

button:hover {
    transform: scale(1.1);
}

.loader {
    border: 4px solid rgba(255,255,255,0.2);
    border-top: 4px solid white;
    border-radius: 50%;
    width: 20px;
    height: 20px;
    animation: spin 1s linear infinite;
    margin: auto;
}

@keyframes spin {
    100% { transform: rotate(360deg); }
}

@keyframes fadeIn {
    from { opacity: 0; transform: translateY(5px); }
    to { opacity: 1; transform: translateY(0); }
}
</style>
</head>

<body>

<div class="chat-container">
    <div class="header">
        Rishika AI ✨
    </div>

    <div class="chat-box" id="chatBox"></div>

    <div class="input-area">
        <input type="text" id="message" placeholder="Ask something powerful..." />
        <button class="mic" onclick="startListening()">🎤</button>
        <button class="send" onclick="sendMessage()">➤</button>
    </div>
</div>

<script>

function appendMessage(text, className) {
    let chatBox = document.getElementById("chatBox");
    let messageDiv = document.createElement("div");
    messageDiv.className = "message " + className;
    messageDiv.innerText = text;
    chatBox.appendChild(messageDiv);
    chatBox.scrollTop = chatBox.scrollHeight;
}

function showLoader() {
    let chatBox = document.getElementById("chatBox");
    let loader = document.createElement("div");
    loader.className = "loader";
    loader.id = "loader";
    chatBox.appendChild(loader);
    chatBox.scrollTop = chatBox.scrollHeight;
}

function removeLoader() {
    let loader = document.getElementById("loader");
    if(loader) loader.remove();
}

function sendMessage() {
    let input = document.getElementById("message");
    let message = input.value.trim();
    if (!message) return;

    appendMessage(message, "user");
    input.value = "";
    showLoader();

    fetch("/ask", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({ message: message })
    })
    .then(response => response.json())
    .then(data => {
        removeLoader();
        appendMessage(data.reply, "bot");

        let speech = new SpeechSynthesisUtterance(data.reply);
        speech.rate = 1;
        speech.pitch = 1;
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
    app.run(debug=True)
