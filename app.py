import streamlit as st
import requests
import json

# ======================
# BACKEND URL
# ======================
BACKEND_URL = "ORS_API_KEY"

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
# CITY INPUT
# ======================
city = st.text_input("Enter City", value="Hyderabad")

col1, col2 = st.columns(2)


# ======================
# AI RECOMMENDATION BUTTON
# ======================
with col1:
    if st.button("✨ Get AI Recommendations"):

        with st.spinner("AI is generating travel plan..."):

            try:
                response = requests.get(
                    f"{BACKEND_URL}/ai-recommend",
                    params={"city": city},
                    timeout=20
                )

                data = response.json()

                st.subheader("🧠 AI Output (Raw)")

                result_text = data.get("result", "")

                # Try parsing JSON from AI response
                try:
                    parsed = json.loads(result_text)

                    st.success(f"Top Places in {parsed.get('city', city)}")

                    for place in parsed["places"]:

                        with st.container():
                            st.markdown(f"### 📍 {place['name']}")
                            st.write(f"📝 {place['description']}")
                            st.write(f"⭐ Rating: {place['rating']}")
                            st.divider()

                except:
                    st.warning("AI returned non-JSON output, showing raw response")
                    st.text(result_text)

            except Exception as e:
                st.error(f"Backend Error: {e}")


# ======================
# SIMPLE CHAT-STYLE UI (OPTIONAL AI FEEL)
# ======================
with col2:
    st.subheader("💬 Travel Chat")

    user_query = st.text_input("Ask Travel Question", placeholder="Best places in Hyderabad?")

    if st.button("Ask AI"):

        with st.spinner("Thinking..."):

            try:
                response = requests.get(
                    f"{BACKEND_URL}/ai-recommend",
                    params={"city": user_query},
                    timeout=20
                )

                data = response.json()

                st.markdown("### 🤖 AI Answer")
                st.write(data["result"])

            except Exception as e:
                st.error(f"Error: {e}")


# ======================
# FOOTER
# ======================
st.markdown("---")
st.caption("🚀 Built as AI Travel Assistant Project (FastAPI + Groq + Streamlit)")
