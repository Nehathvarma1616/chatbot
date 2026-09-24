import streamlit as st
import requests


st.title("Welcome to github issues solver using LLM")
user_input = st.text_input("tell me about whats in your mind! ")
if st.button("send"):
    response = requests.post(
        "http://localhost:8000/input",
        json = {
            "input_str": user_input
        }
    )
    st.write(response.json())