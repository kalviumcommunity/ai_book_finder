import React, { useState } from "react";
import axios from "axios";
import "./App.css"; // add CSS file

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

  // Format AI response → split into list items if numbered
  const formatResponse = (text) => {
    const lines = text.split(/\d+\.\s/).filter((line) => line.trim() !== "");
    if (lines.length > 1) {
      return (
        <ol>
          {lines.map((item, i) => (
            <li key={i} className="book-item">{item.trim()}</li>
          ))}
        </ol>
      );
    }
    return <p>{text}</p>;
  };

  return (
    <div className="container">
      <h1>📚 AI Book Finder</h1>
      <form onSubmit={handleSubmit} className="search-form">
        <input
          type="text"
          value={prompt}
          onChange={(e) => setPrompt(e.target.value)}
          placeholder="e.g. Recommend 5 books for teenagers"
        />
        <button type="submit" disabled={loading}>
          {loading ? "Searching..." : "Search"}
        </button>
      </form>

      <div className="results">
        {response && (
          <>
            <h2>Results:</h2>
            <div className="response-box">{formatResponse(response)}</div>
          </>
        )}
      </div>
    </div>
  );
}

export default App;
