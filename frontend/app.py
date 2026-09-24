import streamlit as st
import requests


st.title("Welcome to github issues solver using LLM")
# user_input = st.text_input("tell me about whats in your mind! ")
# if st.button("send"):
#     response = requests.post(
#         "http://localhost:8000/input",
#         json = {
#             "input_str": user_input
#         }
#     )
#     st.write(response.json())

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])



# React to user input
if prompt := st.chat_input("What is up?"):

    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)


    # Add User message to chat history
    st.session_state.messages.append({"role":"user", "content": prompt})

    response = requests.post(
        "http://localhost:8000/input",
        json = {
            "input_str": prompt
        }
    )
    with st.chat_message("ai"):
        st.markdown(response)
    # Display ai response in chat message container
    st.session_state.messages.append({"role": "ai", "content": response})