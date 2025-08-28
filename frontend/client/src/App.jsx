import React, { useEffect, useRef, useState } from "react";
import axios from "axios";
import "./App.css";

const API_BASE = import.meta.env?.VITE_API_BASE || "https://ai-book-finder-2.onrender.com";

function App() {
  const [prompt, setPrompt] = useState("");
  const [messages, setMessages] = useState([
    {
      role: "bot",
      type: "text",
      text:
        "Hello! I'm your personal book curator. Tell me what kind of story you're in the mood for – maybe something with a strong female lead and complex characters? I'll find the perfect book for you!",
    },
  ]);
  const [loading, setLoading] = useState(false);
  const bottomRef = useRef(null);

  const suggestions = [
    "Books with strong female protagonists",
    "Fantasy romance with enemies-to-lovers",
    "Mystery novels set in Victorian England",
    "Sci-fi with time travel elements",
    "Historical fiction about WWII",
  ];

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, loading]);

  const sendPrompt = async (text) => {
    const clean = text.trim();
    if (!clean) return;

    // push user message
    setMessages((prev) => [...prev, { role: "user", type: "text", text: clean }]);
    setPrompt("");
    setLoading(true);

    try {
      const res = await axios.post(`${API_BASE}/api/prompt`, { prompt: clean });
      const data = res.data.response;

      if (Array.isArray(data)) {
        setMessages((prev) => [...prev, { role: "bot", type: "books", books: data }]);
      } else if (typeof data === "string") {
        setMessages((prev) => [...prev, { role: "bot", type: "text", text: data }]);
      } else {
        setMessages((prev) => [
          ...prev,
          { role: "bot", type: "text", text: typeof data === "object" ? JSON.stringify(data) : String(data) },
        ]);
      }
    } catch (error) {
      console.error(error);
      setMessages((prev) => [...prev, { role: "bot", type: "text", text: "Error: Could not fetch response." }]);
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    sendPrompt(prompt);
  };

  const handleSuggestion = (text) => {
    setPrompt(text);
    sendPrompt(text);
  };

  return (
    <div className="page">
      <header className="topbar">
        <div className="brand">
          <img src="📚" alt="BookBot Logo" className="logo" />
          <div>
            <div className="brand-title">Book Finder AI</div>
            <div className="brand-sub">Your AI Book Curator</div>
          </div>
        </div>
        <button className="connect-btn">Find A Book You'll Love</button>
      </header>

      <main className="content">
        <section className="chat">
          {messages.map((m, idx) => {
            if (m.type === "text") {
              return (
                <div key={idx} className={m.role === "bot" ? "bot-msg" : "user-msg"}>
                  <div className={m.role === "bot" ? "bot-avatar" : "user-avatar"}>{m.role === "bot" ? "🤖" : "🧑"}</div>
                  <div className={m.role === "bot" ? "bubble" : "bubble user-bubble"}>{m.text}</div>
                </div>
              );
            }

            // books message (bot only)
            return (
              <div key={idx} className="bot-msg">
                <div className="bot-avatar">🤖</div>
                <div className="bubble" style={{ width: "100%" }}>
                  Based on your request, I've found some amazing books that match your criteria! Here are my top recommendations:
                  <div className="grid">
                    {m.books?.map((b, i) => (
                      <div className="card" key={i}>
                        <div className="card-body">
                          <div className="card-title">{b.title || "Untitled"}</div>
                          {b.authors && (
                            <div className="card-sub">{Array.isArray(b.authors) ? b.authors.join(", ") : b.authors}</div>
                          )}
                          {b.description && <p className="card-desc">{b.description}</p>}
                          <div className="card-actions">
                            {b.link && (
                              <a className="btn" href={b.link} target="_blank" rel="noreferrer">
                                View
                              </a>
                            )}
                            {(b.goodreads || b.title) && (
                              <a
                                className="btn-outline"
                                href={b.goodreads || `https://www.goodreads.com/search?q=${encodeURIComponent(b.title)}`}
                                target="_blank"
                                rel="noreferrer"
                              >
                                Goodreads
                              </a>
                            )}
                          </div>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            );
          })}

          {loading && (
            <div className="bot-msg">
              <div className="bot-avatar">🤖</div>
              <div className="bubble">Thinking…</div>
            </div>
          )}

          <div ref={bottomRef} />

          <form onSubmit={handleSubmit} className="composer">
            <input
              type="text"
              value={prompt}
              onChange={(e) => setPrompt(e.target.value)}
              placeholder="Describe your perfect book... (e.g., 'I want a fantasy with a strong female lead and enemies-to-lovers romance')"
            />
            <button type="submit" disabled={loading}>
              {loading ? "Thinking..." : "Send"}
            </button>
          </form>

          <div className="chips">
            {suggestions.map((s) => (
              <button key={s} type="button" className="chip" onClick={() => handleSuggestion(s)}>
                {s}
              </button>
            ))}
          </div>
        </section>
      </main>
    </div>
  );
}

export default App;
