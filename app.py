import streamlit as st
from planner import generate_plan

st.set_page_config(page_title="Travel Plan Generator", page_icon="🧳", layout="centered")

st.title("🧳 AI Travel Plan Generator")
st.write("Fill in the trip details and get a day-by-day plan!")

# Read API key from Streamlit secrets (works locally + on Streamlit Cloud)
# Support either OPENAI_API_KEY or OPENROUTER_API_KEY (allows using OpenRouter keys)
if "OPENAI_API_KEY" in st.secrets:
    api_key = st.secrets["OPENAI_API_KEY"]
elif "OPENROUTER_API_KEY" in st.secrets:
    api_key = st.secrets["OPENROUTER_API_KEY"]
else:
    st.error("Missing OPENAI_API_KEY or OPENROUTER_API_KEY in Streamlit secrets.")
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
