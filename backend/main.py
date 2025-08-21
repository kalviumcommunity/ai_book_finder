import os
from flask import Flask, request, jsonify
from flask_cors import CORS   # ✅ added

from openai import OpenAI
from dotenv import load_dotenv

# Load API key
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=api_key)

app = Flask(__name__)
CORS(app)   # ✅ added to allow frontend requests

@app.route("/api/prompt", methods=["POST"])
def run_prompt():
    data = request.json
    query = data.get("prompt", "")

    if not query:
        return jsonify({"error": "No prompt provided"}), 400

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a helpful assistant. The user may give zero-shot, "
                    "one-shot, or few-shot prompts. Detect the style and respond "
                    "appropriately with a direct answer."
                )
            },
            {"role": "user", "content": query}
        ]
    )

    output = response.choices[0].message.content.strip()
    return jsonify({"response": output})

if __name__ == "__main__":
    app.run(port=5000, debug=True)
