import os
import json
import google.generativeai as genai
from dotenv import load_dotenv
from main import run_prompt  # import your existing function
from flask import Flask

load_dotenv()

# Configure Gemini API
genai.configure(api_key=os.getenv("API_Key"))
judge_model = genai.GenerativeModel("gemini-1.5-flash")

# ---------------------------
# Step 1: Define Evaluation Dataset
# ---------------------------
dataset = [
    {
        "input": "Suggest fantasy novels like Harry Potter",
        "expected": ["Harry Potter", "Percy Jackson", "The Hobbit", "Eragon", "Narnia"]
    },
    {
        "input": "Books on artificial intelligence basics",
        "expected": ["Artificial Intelligence", "Deep Learning", "Machine Learning", "AI Superpowers"]
    },
    {
        "input": "Best romance novels",
        "expected": ["Pride and Prejudice", "Me Before You", "The Notebook"]
    },
    {
        "input": "Business strategy books",
        "expected": ["Blue Ocean Strategy", "Good to Great", "The Lean Startup"]
    },
    {
        "input": "Motivational books for students",
        "expected": ["Atomic Habits", "The Power of Habit", "Make Your Bed"]
    },
]

# ---------------------------
# Step 2: Judge Prompt
# ---------------------------
def judge_response(user_input, model_output, expected_output):
    """
    Judge using LLM if the model output aligns with the expected output.
    """
    judge_prompt = f"""
    You are an evaluator. Compare the model's output with the expected output.

    User Input: {user_input}

    Model Output: {json.dumps(model_output, indent=2)}

    Expected Output: {json.dumps(expected_output, indent=2)}

    Evaluation Criteria:
    1. Relevance - Are the books suggested relevant to the query?
    2. Correctness - Do they overlap with expected answers?
    3. Completeness - Does the model cover at least 60% of expected?
    
    Respond in JSON with:
    {{
      "score": 0-1,
      "reason": "short explanation"
    }}
    """

    response = judge_model.generate_content(judge_prompt)
    return response.text.strip()


# ---------------------------
# Step 3: Run Evaluation
# ---------------------------
def run_evaluation():
    results = []
    for case in dataset:
        user_input = case["input"]
        expected_output = case["expected"]

        # Call your model (mocking Flask request here)
        test_request = {"prompt": user_input}
        with Flask(__name__).test_request_context(json=test_request):
            model_response = run_prompt().json["response"]

        # Judge
        evaluation = judge_response(user_input, model_response, expected_output)
        results.append({
            "input": user_input,
            "model_response": model_response,
            "expected": expected_output,
            "evaluation": evaluation
        })

    # Print results
    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    run_evaluation()
