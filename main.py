import sys
import os
from dotenv import load_dotenv
from openai import OpenAI

# Step 1: Load .env variables
print("Step 1: Loading environment variables...")
load_dotenv()

# Step 2: Get API key
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    print("ERROR: OPENAI_API_KEY not found in .env")
    sys.exit(1)
print("Step 2: API Key loaded.")

# Step 3: Initialize OpenAI client
client = OpenAI(api_key=api_key)
print("Step 3: OpenAI client initialized.")

if len(sys.argv) < 2:
    print("ERROR: No query provided. Example: python main.py 'fantasy books'")
    sys.exit(1)
query = sys.argv[1]
print(f"Step 4: Prompt = {query}")

# Step 5: Send request
try:
    print("Step 5: Sending request to API...")
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful book recommendation assistant."},
            {"role": "user", "content": f"Recommend 5 books for: {query}"}
        ],
        max_tokens=200
    )

    answer = response.choices[0].message.content
    print("\nRecommended Books:")
    print(answer)

except Exception as e:
    print(f"ERROR: {e}")
