import os
from flask import Flask, request, jsonify, render_template
import google.generativeai as genai

app = Flask(__name__)

GEMINI_API_KEY = "AQ.Ab8RN6KOOoeXQhYDu0xwYvkN7u0kc_MAxlIXFESCXCoItCvevA"
genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel("gemini-2.5-flash")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.get_json(silent=True)
    if not data or not data.get("message", "").strip():
        return jsonify({"error": "Message is required"}), 400

    message = data["message"].strip()

    try:
        response = model.generate_content(message)
        return jsonify({"reply": response.text}), 200
    except Exception:
        return jsonify({"error": "Failed to get response from Gemini"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
    
