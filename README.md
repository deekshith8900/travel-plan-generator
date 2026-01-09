I have created a travel plan generator application in which it gives a day by day travel itineray from the user inputs such as destination, days, budget, travel style, interests, extra notes. It gives a trip summary with daily Morning/Afternoon/Evening, estimated daily budget, transport tips, packing checklist, and 3 safety tips.

Travel Plan Generator
===================

AI-powered Travel Plan Generator (Streamlit)

This project is a Streamlit web app that generates day-by-day travel itineraries based on user inputs such as destination, trip length, budget, travel style and interests. It uses an LLM (via OpenAI or OpenRouter) to produce a human-readable Markdown plan and allows downloading the result.

Table of Contents
- About
- Features
- Getting Started
- Prerequisites
- Configuration (API key)
- Usage
- Project Structure



About
-----
The app creates realistic, budget-aware itineraries with daily morning/afternoon/evening suggestions, estimated daily budget, transport tips, packing checklist and safety notes.

Features
--------
- Streamlit UI for entering trip details
- Generates day-by-day Markdown itineraries
- Supports `OPENAI_API_KEY` or `OPENROUTER_API_KEY`
- Download the generated plan as a `.md` file

Getting Started
---------------

Prerequisites
-------------
- Python 3.8+
- A virtual environment (recommended)
- The Python dependencies listed in `requirements.txt`

Configuration (API key)
-----------------------
The app requires an LLM API key. Provide one of the following:

- Streamlit secrets file: create `./.streamlit/secrets.toml` with:

	```toml
	OPENAI_API_KEY = "your_openai_key"
	# or
	OPENROUTER_API_KEY = "your_openrouter_key"
	```

- Or set an environment variable before running:

	```bash
	export OPENAI_API_KEY="your_openai_key"
	# or
	export OPENROUTER_API_KEY="your_openrouter_key"
	```

Usage
-----
Create and activate a virtual environment, install dependencies, then run the Streamlit app from the project root:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

Run the commands from the repository root so `./.streamlit/secrets.toml` is discovered.

Project Structure
-----------------
- `app.py` — Streamlit application and UI
- `planner.py` — Core logic that calls the LLM and formats the itinerary
- `requirements.txt` — Python dependencies
- `readme.md` — This file
- `.venv/` — optional virtual environment (not committed)


