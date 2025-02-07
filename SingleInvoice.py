import streamlit as st
import google.generativeai as genai
import fitz  # PyMuPDF

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

# Define chat_page function correctly
def chat_page():
    
    pdf_path = "invoice_.pdf"  # Update with your actual PDF file path

    # Extract text from the PDF
    extracted_text = extract_text_from_pdf(pdf_path)

    if extracted_text.strip() == "":
        st.error("No text extracted from the PDF. Please check the file.")
    else:
        st.session_state['extracted_text'] = extracted_text  # Store extracted text

    # Initialize chat history
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # Display chat history
    st.write("### Chatbot")
    for role, message in st.session_state.chat_history:
        with st.chat_message(role):
            st.markdown(message)

    # User input
    user_input = st.chat_input("Type your message here...", key="chat_input_app")

    if user_input:
        extracted_text = st.session_state.get('extracted_text', '')

        if not extracted_text:
            st.error("No invoice data available. Please check the extracted PDF text.")
        else:
            # Create context for conversation
            chat_context = "\n".join([f"{role}: {msg}" for role, msg in st.session_state.chat_history])
            prompt = (f"Using the extracted invoice data, answer the following question while remembering the chat contextif user greets you give response friendly and respond professionally,give accuarate results give only correct answers if  the questiuon is out of context reply-i dont know:\n\n"
                      f"{chat_context}\n\nUser: {user_input}\n\nInvoice Data:\n{extracted_text}")

            # Generate response using Gemini AI
            response = model.generate_content(prompt)
            answer = response.text if response and hasattr(response, "text") else "I'm sorry, I couldn't process your request."

            # Display bot response
            with st.chat_message("user"):
                st.markdown(user_input)

            with st.chat_message("bot"):
                st.markdown(answer)

            # Store conversation in chat history
            st.session_state.chat_history.append(("user", user_input))
            st.session_state.chat_history.append(("bot", answer))
