import streamlit as st
import requests
import json

# ======================
# BACKEND URL (FIXED)
# ======================
BACKEND_URL = "http://127.0.0.1:8000"

# ======================
# PAGE CONFIG
# ======================
st.set_page_config(
    page_title="AI Travel Assistant",
    layout="wide"
)

st.title("🌍 AI Travel Assistant")
st.caption("Powered by FastAPI + Groq AI + Streamlit")


# ======================
# INPUT
# ======================
city = st.text_input("Enter City", "Hyderabad")

col1, col2 = st.columns(2)


# ======================
# AI BUTTON
# ======================
with col1:
    if st.button("✨ Get AI Recommendations"):

        try:
            response = requests.get(
                f"{BACKEND_URL}/ai-recommend",
                params={"city": city},
                timeout=20
            )

            data = response.json()
            result_text = data.get("result", "")

            st.subheader("🧠 AI Response")

            try:
                parsed = json.loads(result_text)

                st.success(f"Top Places in {parsed['city']}")

                for place in parsed["places"]:
                    st.markdown(f"### 📍 {place['name']}")
                    st.write(place["description"])
                    st.write("⭐", place["rating"])
                    st.divider()

            except:
                st.warning("Raw AI output")
                st.text(result_text)

        except Exception as e:
            st.error(f"Backend Error: {e}")


# ======================
# CHAT MODE
# ======================
with col2:
    st.subheader("💬 Travel Chat")

    user_query = st.text_input("Ask anything about travel")

    if st.button("Ask AI"):

        try:
            response = requests.get(
                f"{BACKEND_URL}/ai-recommend",
                params={"city": user_query},
                timeout=20
            )

            data = response.json()
            st.write(data["result"])

        except Exception as e:
            st.error(f"Error: {e}")


st.markdown("---")
st.caption("🚀 AI Travel Assistant using FastAPI + Groq + Streamlit")
