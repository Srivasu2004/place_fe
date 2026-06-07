import streamlit as st
import requests

BACKEND_URL = "https://place-be-7.onrender.com"

st.title("🧠 AI Resume Analyzer")

# Upload Resume
uploaded_file = st.file_uploader("Upload Resume (PDF)", type=["pdf"])

if uploaded_file:
    files = {"file": uploaded_file.getvalue()}
    res = requests.post(f"{BACKEND_URL}/upload-resume", files=files)
    st.success(res.json()["message"])

# Job Matching
st.subheader("📌 Job Matcher")
job_desc = st.text_area("Paste Job Description")

if st.button("Match Job"):
    res = requests.post(f"{BACKEND_URL}/job-match", params={"job_description": job_desc})
    st.write("Match Score:", res.json()["job_match_score"])

# ATS Score
st.subheader("📊 ATS Score")
keywords = st.text_input("Enter ATS Keywords (comma separated)")

if st.button("Calculate ATS Score"):
    res = requests.post(f"{BACKEND_URL}/ats-score", params={"keywords": keywords})
    st.write("ATS Score:", res.json()["ats_score"])
