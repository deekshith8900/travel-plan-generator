import os
import streamlit as st
from streamlit.errors import StreamlitSecretNotFoundError
from planner import generate_plan

st.set_page_config(page_title="Travel Plan Generator", page_icon="🧳", layout="centered")

st.title("🧳 AI Travel Plan Generator")
st.write("Fill in the trip details and get a day-by-day plan!")

# Read API key from Streamlit secrets (works locally + on Streamlit Cloud)
# Support either OPENAI_API_KEY or OPENROUTER_API_KEY (allows using OpenRouter keys)

def _is_placeholder(key: str) -> bool:
    if not key:
        return True
    k = str(key).strip()
    return k == "" or k.lower().startswith("your_") or "replace" in k.lower()

api_key = None
try:
    if "OPENAI_API_KEY" in st.secrets and not _is_placeholder(st.secrets.get("OPENAI_API_KEY")):
        api_key = st.secrets["OPENAI_API_KEY"]
    elif "OPENROUTER_API_KEY" in st.secrets and not _is_placeholder(st.secrets.get("OPENROUTER_API_KEY")):
        api_key = st.secrets["OPENROUTER_API_KEY"]
    else:
        st.error(
            "Missing or placeholder API key. Add a real `OPENAI_API_KEY` or `OPENROUTER_API_KEY` to your Streamlit secrets (/.streamlit/secrets.toml) or the Streamlit Cloud Secrets UI."
        )
        st.info("If you use OpenRouter, set `OPENROUTER_API_KEY` (starts with `sk-or-`).")
        st.stop()
except StreamlitSecretNotFoundError:
    # No secrets file found; try environment variables as a fallback
    env_openai = os.environ.get("OPENAI_API_KEY")
    env_openrouter = os.environ.get("OPENROUTER_API_KEY")
    if env_openai and not _is_placeholder(env_openai):
        api_key = env_openai
    elif env_openrouter and not _is_placeholder(env_openrouter):
        api_key = env_openrouter
    else:
        st.error(
            "No Streamlit secrets found and no API key in environment variables. Create `./.streamlit/secrets.toml` or set `OPENAI_API_KEY`/`OPENROUTER_API_KEY` in the environment."
        )
        st.info("Run the app from the project root so `./.streamlit/secrets.toml` is discovered, or use the Streamlit Cloud Secrets UI.")
        st.stop()






with st.form("trip_form"):
    destination = st.text_input("Where are you going?", placeholder="Tokyo, Japan")
    days = st.number_input("How many days?", min_value=1, max_value=30, value=5)
    budget = st.selectbox("Budget level", ["Low", "Medium", "High"])
    travel_style = st.selectbox("Travel style", ["Relaxed", "Balanced", "Busy (see everything)"])
    interests = st.multiselect(
        "Pick interests",
        ["Food", "Museums", "Nature", "Shopping", "Beaches", "History", "Nightlife", "Theme parks", "Local culture"],
        default=["Food", "Local culture"]
    )
    extra_notes = st.text_area("Extra notes (optional)", placeholder="I’m vegetarian / I have kids / I hate early mornings...")

    submitted = st.form_submit_button("Generate my travel plan ✨")

if submitted:
    if not destination.strip():
        st.warning("Please type a destination.")
        st.stop()

    user_request = f"""
Destination: {destination}
Trip length: {days} days
Budget: {budget}
Travel style: {travel_style}
Interests: {", ".join(interests) if interests else "None"}
Extra notes: {extra_notes if extra_notes.strip() else "None"}

Make a day-by-day itinerary. Keep it realistic and not too expensive for the chosen budget.
"""

    with st.spinner("Planning your trip..."):
        try:
            plan_md = generate_plan(api_key=api_key, user_request=user_request)
        except Exception as e:
            st.error(f"Something went wrong: {e}")
            st.stop()

    st.success("Done! Here's your plan:")
    st.markdown(plan_md)

    st.download_button(
        "Download plan as .md",
        data=plan_md,
        file_name=f"travel_plan_{destination.replace(' ', '_').lower()}.md",
        mime="text/markdown"
    )
