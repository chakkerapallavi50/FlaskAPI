import streamlit as st
import google.generativeai as genai
import fitz  # PyMuPDF
 
# Configure the page before anything else
st.set_page_config(page_title="Invoice Chatbot", layout="wide")
 
# Configure Gemini AI
GEMINI_API_KEY = "AIzaSyB0jEXbWexwC4VH5aNL3GuSjffxyxWk3QI"  # Replace with your actual API key
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-pro")
 
# Function to extract text from the provided PDF file
def extract_text_from_pdf(pdf_path):
    document = fitz.open(pdf_path)
    full_text = ""
    for page_num in range(document.page_count):
        page = document.load_page(page_num)
        full_text += page.get_text("text")  # Extract text from each page
    return full_text
 
# Streamlit UI
st.markdown("<h1 style='text-align: center;'>Invoice Chatbot</h1>", unsafe_allow_html=True)
 
# Define the paths to the multiple PDF files
pdf_paths = ["Invoice_1.pdf", "Invoice_2.pdf", "Invoice_3.pdf","Invoice_4.pdf"]  # Add your PDF file paths here
 
# Extract text from each PDF and combine it
combined_text = ""
for pdf_path in pdf_paths:
    extracted_text = extract_text_from_pdf(pdf_path)
    if extracted_text.strip() == "":
        st.warning(f"No text extracted from {pdf_path}. Please check the file.")
    else:
        combined_text += extracted_text + "\n\n"  # Add space between invoice contents
 
if combined_text.strip() == "":
    st.error("No text extracted from the PDFs. Please check the files.")
else:
    st.session_state['extracted_text'] = combined_text  # Store extracted text
 
# Initialize chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
 
# Display chat history using chat_message
st.write("### Chatbot")
for role, message in st.session_state.chat_history:
    with st.chat_message(role):
        st.markdown(message)
 
# User input using chat_input
user_input = st.chat_input("Type your message here...")
 
if user_input:
    extracted_text = st.session_state.get('extracted_text', '')
 
    if not extracted_text:
        st.error("No invoice data available. Please check the extracted PDF text.")
    else:
        # Create context for conversation
        chat_context = "\n".join([f"{role}: {msg}" for role, msg in st.session_state.chat_history])
        prompt = (f"Based on the extracted invoice data from multiple invoices, answer the following question. "
          "If the user greets you, provide a friendly response. "
          "If the user's question is outside the context of the invoices, politely inform them that you don't have knowledge about that. "
          "If you're unsure of the answer or if the information is incorrect, say 'I don't know'. "
          "When answering, carefully analyze the content and provide an accurate response. "
          "If an answer is found in one invoice, don't stop there—search the entire context as it may contain multiple answers. "
          "Only answer questions related to the invoice content. Do not repeat the user's question; simply provide the information directly.\n\n"
          f"Conversation History:\n{chat_context}\n\n"
          f"User: {user_input}\n\n"
          f"Extracted Invoice Data:\n{extracted_text}")
 
 
 
 
        # Generate response using Gemini AI
        response = model.generate_content(prompt)
        answer = response.text if response and hasattr(response, "text") else "I'm sorry, I couldn't process your request."
 
        # Display user input and bot response in the chat
        with st.chat_message("user"):
            st.markdown(user_input)
 
        with st.chat_message("bot"):
            st.markdown(answer)
 
        # Store the conversation in chat history
        st.session_state.chat_history.append(("user", user_input))
        st.session_state.chat_history.append(("bot", answer))
 