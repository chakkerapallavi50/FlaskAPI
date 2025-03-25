import streamlit as st
import google.generativeai as genai
import fitz  # PyMuPDF

# Configure Gemini AI
GEMINI_API_KEY = "AIzaSyB0jEXbWexwC4VH5aNL3GuSjffxyxWk3QI"  # Replace with your actual API key
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-pro-latest")

# Function to extract text from the provided PDF file
def extract_text_from_pdf(pdf_path):
    document = fitz.open(pdf_path)
    full_text = ""
    for page_num in range(document.page_count):
        page = document.load_page(page_num)
        full_text += page.get_text("text")  # Extract text from each page
    return full_text

# Define the chatbot function
def chat_page():
    # Streamlit UI
   
    # Define the paths to the multiple PDF files
    pdf_paths = ["Invoice_1.pdf", "Invoice_2.pdf", "Invoice_3.pdf", "Invoice_4.pdf"]

    # Extract text from each PDF and combine it
    combined_text = ""
    for pdf_path in pdf_paths:
        extracted_text = extract_text_from_pdf(pdf_path)
        if extracted_text.strip() == "":
            st.warning(f"No text extracted from {pdf_path}. Please check the file.")
        else:
            combined_text += extracted_text + "\n\n"

    if combined_text.strip() == "":
        st.error("No text extracted from the PDFs. Please check the files.")
    else:
        st.session_state['invoice_data'] = combined_text  # Store extracted text

    # Initialize chat history
    if "invoice_chat_history" not in st.session_state:
        st.session_state.invoice_chat_history = []

    # Display chat history using chat_message
    st.write("### Chatbot")
    for role, message in st.session_state.invoice_chat_history:
        with st.chat_message(role):
            st.markdown(message)

    # User input using chat_input
    user_input = st.chat_input("Type your message here...", key="invoice_chat_input")

    if user_input:
        extracted_text = st.session_state.get('invoice_data', '')

        if not extracted_text:
            st.error("No invoice data available. Please check the extracted PDF text.")
        else:
            # Create context for conversation
            chat_context = "\n".join([f"{role}: {msg}" for role, msg in st.session_state.invoice_chat_history])
            prompt = (f"""
You are an intelligent invoice chatbot capable of answering questions **only** related to the extracted invoices.
Your responses must be accurate, relevant, and based **strictly** on the provided invoice data.
You must maintain separate details for different invoices and never merge them.
If a user asks about a specific invoice, provide details only for that invoice.
If a user asks about multiple invoices, respond accordingly.
Always refer to previous queries when answering if an invoice number or recipient name is not mentioned.

Extract the following details from the invoices:
- Invoice details (number, order number, invoice date, due date, total due)  
- Sender details (name, address, email)  
- Recipient details (name, address, email)  
- Items (quantity, service, rate, adjustment, sub-total)  
- Tax details (tax amount)  
- Bank details (bank name, account number, BSB number)  

### **Guidelines for Answering:**
1. **Focus on Invoice Content:**  
   - Answer **only** based on the invoice data provided.  
   - If a question is unrelated to invoices, politely state that you can only assist with invoice queries.  

2. **Analyze Carefully:**  
   - Search **all extracted invoices** before responding.  
   - Maintain invoice-specific accuracy.  

3. **Avoid Guessing:**  
   - If the answer is not found in the invoices, respond:  
     _"I couldn't find this information in the provided invoices."_  
   - If a question is unclear, ask for clarification.  

4. **Provide Direct Answers:**  
   - Do **not** repeat the user's question.  
   - Keep responses **concise and structured**.  

5. **Handle Greetings & Out-of-Scope Questions:**  
   - Respond professionally to greetings.  
   - If the question is unrelated to invoices, say:  
     _"I can only assist with invoice-related queries. Let me know how I can help with your invoice information!"_

### **Context for Answering the Query:**
- **Extracted Invoice Data:**  
{extracted_text}

- **Previous Conversation History:**  
{chat_context}

### **User Question:**  
{user_input}
""")

            # Generate response using Gemini AI
            response = model.generate_content(prompt)
            answer = response.text if response and hasattr(response, "text") else "I'm sorry, I couldn't process your request."

            # Display user input and bot response in the chat
            with st.chat_message("user"):
                st.markdown(user_input)

            with st.chat_message("bot"):
                st.markdown(answer)

            # Store the conversation in chat history
            st.session_state.invoice_chat_history.append(("user", user_input))
            st.session_state.invoice_chat_history.append(("bot", answer))
