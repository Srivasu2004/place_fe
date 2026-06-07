import streamlit as st
import requests

BACKEND_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="AI Tourist Guide",
    layout="wide"
)

st.title("🌍 AI Tourist Recommendation System")

city = st.text_input(
    "Enter City",
    value="Hyderabad"
)

if st.button("Find Places"):

    with st.spinner("AI is finding places..."):

        response = requests.get(
            f"{BACKEND_URL}/recommend",
            params={"city": city}
        )

        data = response.json()

        st.success(
            f"Recommendations for {city}"
        )

        st.write(data["recommendation"])
