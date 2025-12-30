from openai import OpenAI

SYSTEM_PROMPT = """
You are a helpful travel planner.
Create safe, realistic plans.
If the user budget is low, suggest cheaper options.
Return the final answer in clear Markdown with headings.

Must include:
1) Trip Summary
2) Day-by-day itinerary (Morning / Afternoon / Evening)
3) Estimated daily budget
4) Local transport tips
5) Packing checklist
6) 3 safety tips
"""

def generate_plan(api_key: str, user_request: str) -> str:
    if not api_key or not api_key.strip():
        raise ValueError("Missing API key (OPENAI_API_KEY or OPENROUTER_API_KEY)")

    # Prepare headers with explicit Bearer token so OpenRouter receives Authorization
    default_headers = {
        "Authorization": f"Bearer {api_key}",
        "HTTP-Referer": "http://localhost:8501",  # change to your deployed Streamlit URL later
        "X-Title": "Travel Plan Generator",
    }

    # If the key looks like an OpenRouter key, use the OpenRouter base URL and model name.
    is_openrouter = str(api_key).startswith("sk-or-") or str(api_key).startswith("or-")
    base_url = "https://openrouter.ai/api/v1" if is_openrouter else None
    model_name = "openai/gpt-4o-mini" if is_openrouter else "gpt-4o-mini"

    client = OpenAI(
        api_key=api_key,
        base_url=base_url,
        default_headers=default_headers,
    )

    response = client.chat.completions.create(
        model=model_name,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_request},
        ],
        temperature=0.7,
    )

    # Return the assistant message content (compat with OpenRouter/OpenAI response shape)
    try:
        return response.choices[0].message.content
    except Exception:
        # Fallback in case response shape differs
        return getattr(response, "text", str(response))
