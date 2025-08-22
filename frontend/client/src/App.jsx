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
      const res = await axios.post("http://127.0.0.1:5000/api/prompt", {
        prompt,
      });
      setResponse(res.data.response);
    } catch (error) {
      console.error(error);
      setResponse("Error: Could not fetch response.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container">
      <h1>📚 AI Book Finder</h1>
      <form onSubmit={handleSubmit} className="search-form">
        <input
          type="text"
          value={prompt}
          onChange={(e) => setPrompt(e.target.value)}
          placeholder="e.g. Tell me about the book 'Pride and Prejudice'"
        />
        <button type="submit" disabled={loading}>
          {loading ? "Searching..." : "Search"}
        </button>
      </form>

      <div className="results">
        {response && (
          <>
            <h2>Results:</h2>
            <div className="response-box">{response}</div>
          </>
        )}
      </div>
    </div>
  );
}

export default App;
