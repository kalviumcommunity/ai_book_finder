import os, requests, json
from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai
from dotenv import load_dotenv

app = Flask(__name__)
CORS(app)
load_dotenv()

# Configure Gemini API
genai.configure(api_key=os.getenv("API_Key"))
model = genai.GenerativeModel('gemini-1.5-flash')
embedding_model = genai.GenerativeModel('embedding-001')

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

@app.route("/api/prompt", methods=["POST"])
def run_prompt():
    data = request.json
    query = data.get("prompt", "")
    temperature = data.get("temperature", 0.7)  
    top_p = data.get("top_p", 0.9)  
    stop_sequences = data.get("stop", ["END"])  

    if not query:
        return jsonify({"error": "No prompt provided"}), 400
    
    try:
        # Check if the query is asking for books
        if any(keyword in query.lower() for keyword in ['book', 'books', 'reading', 'author', 'title']):
            # Extract search terms from the query
            search_terms = query.replace('find', '').replace('search', '').replace('books', '').replace('book', '').strip()
            books = get_books(search_terms)
            return jsonify({"response": books})
        
        response = model.generate_content(
            f"You are a helpful assistant. Always respond in a helpful and informative way. User query: {query}",
            generation_config=genai.GenerationConfig(
                temperature=temperature,
                top_p=top_p,
                stop_sequences=stop_sequences
            )
        )

        if response.candidates:
            text_content = response.candidates[0].content.parts[0].text
            return jsonify({"response": text_content})
        else:
            return jsonify({"error": "No response generated"}), 500

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/embeddings", methods=["POST"])
def generate_embeddings():
    try:
        data = request.json
        text = data.get("text", "")

        if not text:
            return jsonify({"error": "No text provided"}), 400

        # Generate embedding using Gemini's embedding model
        embedding = embedding_model.embed_content(text)
        embedding_vector = embedding.embedding

        return jsonify({
            "text": text,
            "embedding": embedding_vector,
            "dimensions": len(embedding_vector)
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(port=5000, debug=True)
