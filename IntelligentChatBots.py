import streamlit as st

# Set page configuration
st.set_page_config(page_title="Multi-Chatbot App", page_icon="📚")

st.sidebar.success("Select a task from the sidebar.")

st.markdown("<center><h1 style='text-align: center;'>Welcome to the Multi-Chatbot App! 🤖</h1></center>", unsafe_allow_html=True)
st.write("Use the sidebar to navigate different LLM tasks.")

