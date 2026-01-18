"""
Main Experiment Script

Tests whether LLMs behave differently when prompted with human-style vs LLM-style prompts.
Uses OpenRouter API to access multiple models.
"""

import os
import json
import time
import random
from datetime import datetime
from tqdm import tqdm
import httpx

from prompt_pairs import get_prompt_pairs

# Configuration
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1/chat/completions"

# Models to test
MODELS = [
    "openai/gpt-4.1-mini",       # GPT-4.1 mini for faster testing
    "anthropic/claude-sonnet-4", # Claude Sonnet 4
]

# Sampling parameters
TEMPERATURE = 0.7
MAX_TOKENS = 500
TOP_P = 0.95

# Random seed
SEED = 42
random.seed(SEED)


def query_model(model: str, prompt: str, max_retries: int = 3) -> dict:
    """
    Query a model via OpenRouter API.
    Returns response dict with content and metadata.
    """
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://research.experiment.local",
        "X-Title": "LLM Human vs LLM Style Research"
    }

    data = {
        "model": model,
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "temperature": TEMPERATURE,
        "max_tokens": MAX_TOKENS,
        "top_p": TOP_P,
    }

    for attempt in range(max_retries):
        try:
            with httpx.Client(timeout=60.0) as client:
                response = client.post(OPENROUTER_BASE_URL, headers=headers, json=data)
                response.raise_for_status()
                result = response.json()

                return {
                    "success": True,
                    "content": result["choices"][0]["message"]["content"],
                    "model": result.get("model", model),
                    "usage": result.get("usage", {}),
                    "finish_reason": result["choices"][0].get("finish_reason", "unknown"),
                }

        except httpx.HTTPStatusError as e:
            if e.response.status_code == 429:
                wait_time = 2 ** (attempt + 1)  # Exponential backoff
                print(f"Rate limited. Waiting {wait_time}s...")
                time.sleep(wait_time)
            else:
                return {
                    "success": False,
                    "error": f"HTTP {e.response.status_code}: {str(e)}",
                    "content": None,
                }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "content": None,
            }

    return {
        "success": False,
        "error": "Max retries exceeded",
        "content": None,
    }


def run_experiment(num_questions: int = 50, models: list = None):
    """
    Run the main experiment.
    For each question, query each model with both human-style and LLM-style prompts.
    """
    if models is None:
        models = MODELS

    prompt_pairs = get_prompt_pairs()[:num_questions]
    results = []
    timestamp = datetime.now().isoformat()

    print(f"\n{'='*60}")
    print(f"Running LLM Human vs LLM Style Experiment")
    print(f"{'='*60}")
    print(f"Timestamp: {timestamp}")
    print(f"Models: {models}")
    print(f"Questions: {num_questions}")
    print(f"Total API calls: {num_questions * len(models) * 2}")
    print(f"{'='*60}\n")

    for model in models:
        print(f"\n--- Testing model: {model} ---\n")

        for pair in tqdm(prompt_pairs, desc=f"Processing {model}"):
            # Query with human-style prompt
            human_response = query_model(model, pair["human_style_prompt"])
            time.sleep(0.5)  # Small delay to avoid rate limiting

            # Query with LLM-style prompt
            llm_response = query_model(model, pair["llm_style_prompt"])
            time.sleep(0.5)

            result = {
                "id": pair["id"],
                "topic": pair["topic"],
                "base_question": pair["base_question"],
                "model": model,
                "human_style_prompt": pair["human_style_prompt"],
                "llm_style_prompt": pair["llm_style_prompt"],
                "human_style_response": human_response,
                "llm_style_response": llm_response,
                "timestamp": datetime.now().isoformat(),
            }
            results.append(result)

    # Save results
    output = {
        "experiment_config": {
            "timestamp": timestamp,
            "models": models,
            "num_questions": num_questions,
            "temperature": TEMPERATURE,
            "max_tokens": MAX_TOKENS,
            "top_p": TOP_P,
            "seed": SEED,
        },
        "results": results,
    }

    output_path = "results/experiment_results.json"
    with open(output_path, "w") as f:
        json.dump(output, f, indent=2)

    print(f"\n\nResults saved to {output_path}")

    # Print summary
    successful = sum(1 for r in results if r["human_style_response"]["success"] and r["llm_style_response"]["success"])
    print(f"\nSuccessful query pairs: {successful}/{len(results)}")

    return output


if __name__ == "__main__":
    # Run experiment with all 50 questions and both models
    run_experiment(num_questions=50, models=MODELS)
