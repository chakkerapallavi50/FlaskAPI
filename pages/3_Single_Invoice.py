import streamlit as st
import SingleInvoice  # Your single invoice chatbot module

st.title("📄 Single Invoice Processing")
st.write("Interact with the chatbot for a single invoice.")

SingleInvoice.chat_page()
