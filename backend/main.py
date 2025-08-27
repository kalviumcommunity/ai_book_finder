import os, requests, json
from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI
from dotenv import load_dotenv

app = Flask(__name__)
CORS(app)
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def get_books(query: str):
    url = f"https://www.googleapis.com/books/v1/volumes?q={query}"
    response = requests.get(url)
    data = response.json()
    results = []
    if "items" in data:
        for item in data["items"]:
            info = item.get("volumeInfo", {})
            results.append({
                "title": info.get("title"),
                "authors": info.get("authors"),
                "description": info.get("description"),
                "link": info.get("infoLink")
            })
    return results

functions = [{
    "name": "get_books",
    "description": "Fetch books from Google Books API",
    "parameters": {
        "type": "object",
        "properties": {
            "query": {
                "type": "string",
                "description": "Search term for books, can include author or topic"
            }
        },
        "required": ["query"]
    }
}]

@app.route("/api/prompt", methods=["POST"])
def run_prompt():
    data = request.json
    query = data.get("prompt", "")
    temperature = data.get("temperature", 0.7)
    top_p = data.get("top_p", 1.0)  
    top_k = data.get("top_k", None)  # user-provided top_k

    if not query:
        return jsonify({"error": "No prompt provided"}), 400
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful assistant. Call functions if needed."},
                {"role": "user", "content": query}
            ],
            functions=functions,
            function_call="auto",
            temperature=temperature,
            top_p=top_p,
            logprobs=True if top_k else False,  # only request logprobs if simulating top-k
        )

        message = response.choices[0].message

        # --- Simulate Top-K ---
        if top_k and hasattr(response.choices[0], "logprobs") and response.choices[0].logprobs:
            logprobs = response.choices[0].logprobs.content[0].top_logprobs
            # Take top_k tokens only
            top_k_tokens = sorted(logprobs.items(), key=lambda x: -x[1])[:top_k]
            return jsonify({
                "response": message.content.strip() if message.content else None,
                "top_k_tokens": top_k_tokens
            })

        if message.function_call:
            func_name = message.function_call.name
            args = json.loads(message.function_call.arguments)
            if func_name == "get_books":
                return jsonify({"response": get_books(args["query"])})

        return jsonify({"response": message.content.strip()})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(port=5000, debug=True)
