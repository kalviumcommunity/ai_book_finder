# AI Book Finder

AI Book Finder is an intelligent assistant that helps users discover books by describing what they’re looking for in plain language. It understands user preferences and suggests relevant books using modern AI techniques.

## Features

- Understands natural language queries
- Recommends books based on genre, characters, and themes
- Retrieves relevant books from a dataset using semantic search
- Returns structured book details like title, author, genre, and summary
- Supports additional actions like adding to reading list or filtering results

## How it works

This project makes use of the following AI capabilities:

### Prompting
The application takes natural language input from the user, such as "Recommend a mystery novel with a strong female lead," and uses prompts to guide the language model in understanding the user's intent clearly.

### RAG (Retrieval-Augmented Generation)
Instead of relying solely on the model’s memory, the system performs a search over a dataset of books to find relevant matches. These results are passed back into the language model to generate informed recommendations.

### Structured Output
The language model is instructed to return results in a structured JSON-like format. This makes it easy to display consistent information such as:
- Title
- Author
- Genre
- Summary
- Rating

### Function Calling
Based on user actions or follow-up questions, the application can trigger backend functions such as:
- Adding a book to a personal reading list
- Fetching purchase or preview links
- Filtering books by genre or rating


