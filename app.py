from flask import Flask, render_template, request, jsonify
import ollama

app = Flask(__name__)

client = ollama.Client(host='http://127.0.0.1:11434')

PERSONALITY_PROMPT = """
You are Rishika Bhandari.

MBA in Business Analytics at IIT Dhanbad.
Former engineer at British Telecom.
Confident, analytical, emotionally deep.
Future professor at Imperial College London.

Respond confidently, intelligently, and authentically.
Keep answers powerful and reflective.
"""

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/ask", methods=["POST"])
def ask():
    user_input = request.json["message"]

    response = client.chat(
        model="llama3",
        messages=[
            {"role": "system", "content": PERSONALITY_PROMPT},
            {"role": "user", "content": user_input}
        ]
    )

    return jsonify({"reply": response["message"]["content"]})

if __name__ == "__main__":
    app.run(debug=True)
