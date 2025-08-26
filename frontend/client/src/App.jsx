import React, { useState } from "react";
import axios from "axios";
import "./App.css";

function App() {
  const [prompt, setPrompt] = useState("");
  const [response, setResponse] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setResponse("");

    try {
      const res = await axios.post("http://127.0.0.1:5000/api/prompt", { prompt });
      setResponse(res.data.response);
    } catch (error) {
      console.error(error);
      setResponse("Error: Could not fetch response.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app-container">
      <div className="card">
        <h1>📚 AI Book Finder</h1>
        <form onSubmit={handleSubmit} className="search-form">
          <input
            type="text"
            value={prompt}
            onChange={(e) => setPrompt(e.target.value)}
            placeholder="Ask me about books..."
          />
          <button type="submit" disabled={loading}>
            {loading ? "Thinking..." : "Ask"}
          </button>
        </form>

        {response && (
          <div className="response-box">
            <strong>AI:</strong>
            <p>{response}</p>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
