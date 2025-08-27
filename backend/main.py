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

def goodreads_link(title: str):
    if not title:
        return None
    return f"https://www.goodreads.com/search?q={requests.utils.quote(title)}"

def get_books(query: str):
    url = f"https://www.googleapis.com/books/v1/volumes?q={query}"
    response = requests.get(url)
    data = response.json()
    results = []
    if "items" in data:
        for item in data["items"]:
            info = item.get("volumeInfo", {})
            title = info.get("title")
            results.append({
                "title": title,
                "authors": info.get("authors"),
                "description": info.get("description"),
                "link": info.get("infoLink"),
                "goodreads": goodreads_link(title)
            })
    return results

@app.route("/api/prompt", methods=["POST"])
def run_prompt():
    data = request.json
    query = data.get("prompt", "").strip()
    temperature = data.get("temperature", 0.7)  
    top_p = data.get("top_p", 0.9)  
    stop_sequences = data.get("stop", ["END"])  

    if not query:
        return jsonify({"error": "No prompt provided"}), 400
    
    try:
        # Always attempt to fetch books for any user prompt
        books = get_books(query)
        if len(books) >= 1:
            return jsonify({"response": books})

        # Fallback: ask the model to output 5 book titles, then search again
        prompt = (
            "Suggest 5 specific book titles (with authors) matching this request: "
            f"'{query}'. Return them as lines 'Title — Author'."
        )
        response = model.generate_content(
            prompt,
            generation_config=genai.GenerationConfig(
                temperature=temperature,
                top_p=top_p,
                stop_sequences=stop_sequences
            )
        )
        text = response.candidates[0].content.parts[0].text if response.candidates else ""
        titles = [line.split(" — ")[0].strip(" -–—") for line in text.splitlines() if line.strip()]

        aggregated = []
        for t in titles:
            search_results = get_books(t)
            if search_results:
                aggregated.append(search_results[0])
        if aggregated:
            return jsonify({"response": aggregated})

        # Last resort: return model text (rare)
        return jsonify({"response": text or "No results found."})

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
