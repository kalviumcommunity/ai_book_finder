import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI
from dotenv import load_dotenv
import requests

# Load API key
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=api_key)

app = Flask(__name__)
CORS(app)   # Allow frontend requests

# Example: function to fetch book details from Open Library API
def get_book_info(title: str):
    url = f"https://openlibrary.org/search.json?title={title}"
    res = requests.get(url).json()
    if res["docs"]:
        first = res["docs"][0]
        return {
            "title": first.get("title"),
            "author": first.get("author_name", ["Unknown"])[0],
            "year": first.get("first_publish_year", "N/A"),
        }
    return {"error": "No book found"}

@app.route("/api/prompt", methods=["POST"])
def run_prompt():
    data = request.json
    query = data.get("prompt", "")

    if not query:
        return jsonify({"error": "No prompt provided"}), 400

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful AI that finds books."},
            {"role": "user", "content": query}
        ],
        tools=[  # ✅ Function calling definition
            {
                "type": "function",
                "function": {
                    "name": "get_book_info",
                    "description": "Fetch book info from Open Library",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "title": {"type": "string", "description": "Book title"}
                        },
                        "required": ["title"],
                    },
                },
            }
        ],
        tool_choice="auto"  # Let model decide when to call
    )

    message = response.choices[0].message

    # If AI called a function
    if message.tool_calls:
        tool_call = message.tool_calls[0]
        if tool_call.function.name == "get_book_info":
            args = tool_call.function.arguments
            import json
            args = json.loads(args)
            result = get_book_info(args["title"])

            # Send function response back to model for natural language formatting
            followup = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a helpful AI."},
                    {"role": "user", "content": query},
                    message,
                    {
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "name": "get_book_info",
                        "content": str(result)
                    }
                ]
            )
            final_output = followup.choices[0].message.content.strip()
            return jsonify({"response": final_output})

    # If no function call
    return jsonify({"response": message.content})

if __name__ == "__main__":
    app.run(port=5000, debug=True)
