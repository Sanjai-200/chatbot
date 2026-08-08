import os
from flask import Flask, request, jsonify, render_template
from google import genai

app = Flask(__name__)

GEMINI_API_KEY = "AQ.Ab8RN6JfupVzRYuPaeTO0lf_SpbrbtA_GOICbOGZ4FaRG1xKdw"
client = genai.Client(api_key=GEMINI_API_KEY)

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
        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=message
        )
        return jsonify({"reply": response.text}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
    
