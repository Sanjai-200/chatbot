import os
from flask import Flask, request, jsonify, render_template
import google.generativeai as genai

app = Flask(__name__)

api_key = os.environ.get("AQ.Ab8RN6KOOoeXQhYDu0xwYvkN7u0kc_MAxlIXFESCXCoItCvevA")
if api_key:
    genai.configure(api_key=api_key)

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

    if not api_key:
        return jsonify({"error": "Server is missing GEMINI_API_KEY"}), 500

    try:
        response = model.generate_content(message)
        return jsonify({"reply": response.text}), 200
    except Exception:
        return jsonify({"error": "Failed to get response from Gemini"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
  
