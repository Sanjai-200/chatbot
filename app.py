import os
from flask import Flask, request, jsonify, render_template
from google import genai

app = Flask(__name__)

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY") or "AQ.Ab8RN6Kw9lZrbwJNSK9TLw2TOH7fFGuKxB94x0Xt2PBr2YUlhg"

client = genai.Client(api_key=GEMINI_API_KEY)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.get_json(silent=True)

    if not data or not data.get("message", "").strip():
        return jsonify({"error": "Message is required"}), 400

    try:
        response = client.models.generate_content(
            model="gemini-flash-latest",
            contents=data["message"].strip()
        )

        return jsonify({"reply": response.text})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5000))
    )
