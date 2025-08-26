import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI
from dotenv import load_dotenv

# Load API key
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=api_key)

app = Flask(__name__)
CORS(app)  # Allow frontend to talk to backend

@app.route("/api/prompt", methods=["POST"])
def generate_response():
    try:
        data = request.get_json()
        user_prompt = data.get("prompt", "")

        if not user_prompt:
            return jsonify({"response": "No prompt provided."}), 400

        # Call OpenAI
        completion = client.chat.completions.create(
            model="gpt-4o-mini",  # can switch to gpt-4.1 or gpt-3.5-turbo
            messages=[
                {"role": "system", "content": "You are a helpful AI assistant."},
                {"role": "user", "content": user_prompt},
            ],
            max_tokens=500,
            temperature=0.7
        )

        ai_response = completion.choices[0].message.content.strip()

        return jsonify({"response": ai_response})

    except Exception as e:
        return jsonify({"response": f"Error: {str(e)}"}), 500


if __name__ == "__main__":
    app.run(debug=True)
