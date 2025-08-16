import sys
import os
from dotenv import load_dotenv
from openai import OpenAI

# Load API key
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    print("ERROR: OPENAI_API_KEY not found in .env")
    sys.exit(1)

client = OpenAI(api_key=api_key)

if len(sys.argv) < 2:
    print("Usage: python main.py <your prompt>")
    sys.exit(1)

user_input = " ".join(sys.argv[1:])

# Detect style
example_count = user_input.count("\n")  # crude but works for now
if example_count == 0:
    prompt_type = "zero-shot"
elif example_count == 1:
    prompt_type = "one-shot"
else:
    prompt_type = "few-shot"

system_instruction = (
    f"You are a helpful assistant for book recommendations. "
    f"The user is giving you a {prompt_type} prompt. "
    "Always respond directly to the request with no clarifying questions, "
    "no step-by-step explanations, and no extra commentary. "
    "Format the answer cleanly and clearly."
)

messages = [
    {"role": "system", "content": system_instruction},
    {"role": "user", "content": user_input}
]

try:
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        max_tokens=300
    )

    print(response.choices[0].message.content.strip())

except Exception as e:
    print(f"ERROR: {e}")
