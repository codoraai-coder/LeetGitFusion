import streamlit as st
import requests

API_BASE = "http://127.0.0.1:8000"

st.title("🤖 AI Agent Leaderboard & GitHub Analyzer")

mode = st.sidebar.selectbox("Choose Mode", ["LeetCode Leaderboard", "GitHub Profile Analysis"])

if mode == "LeetCode Leaderboard":
    usernames = st.text_input("Enter LeetCode usernames (comma separated)")
    if st.button("Analyze") and usernames:
        res = requests.get(f"{API_BASE}/leetcode/leaderboard", params={"usernames": usernames})
        st.json(res.json())

elif mode == "GitHub Profile Analysis":
    username = st.text_input("Enter GitHub username")
    if st.button("Analyze") and username:
        res = requests.get(f"{API_BASE}/github/analyze/{username}")
        st.json(res.json())
