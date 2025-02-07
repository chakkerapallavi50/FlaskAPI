import streamlit as st
import google.generativeai as genai
import json
def chat_page():
# Function to classify email as Spam or Not Spam using Gemini AI
    def classify_email_with_gemini(email_text, api_key):
        """
        Uses Gemini AI to classify email text as spam or not spam.
        """
        genai.configure(api_key=api_key)
        
        # Define the prompt for Gemini AI
        prompt = f"""
    You are an AI email classifier. Your job is to analyze the given email content and determine whether it is **Spam** or **Not Spam**.
    Follow these classification rules:
    if the user greets you respond friendly and give professional reply
    ### **Spam Emails:**
    - Unsolicited promotional messages or excessive advertisements.
    - Phishing attempts, fraudulent content, or scam emails.
    - Requests for sensitive information (passwords, bank details, etc.).
    - Suspicious links, attachments, or urgent messages trying to create panic.
    - Fake lottery wins, job offers, or get-rich-quick schemes.

    ### **Not Spam Emails:**
    - Genuine personal, business, or work-related messages.
    - Emails from trusted sources or known contacts.
    - Service notifications, invoices, customer inquiries, or order confirmations.

    ### **Email Text:**
    {email_text}

    ### **Classification:**
    Respond with only **Spam** or **Not Spam** and nothing else. give output in the form of json here key is email type and value is your answer whether that email is spam or not
    """
        
        # Initialize the Gemini model
        model = genai.GenerativeModel("gemini-1.5-flash")
        
        try:
            # Generate the response from Gemini AI
            response = model.generate_content(prompt)
            
        
            
            if not response.text.strip():
                raise ValueError("Empty response from Gemini AI.")
            
            # Clean the response and return it
            classification = response.text.strip()
            print("Cleaned Response from Gemini AI:", classification)
            
            return classification
        
        except Exception as e:
            print(f"Error during AI request: {e}")
            return None
    
    # Streamlit UI

    st.title("Email Spam Detection")
    st.write("""
        Enter the text of the email you want to classify as spam or not spam.
        The model will analyze it and return the classification.
    """)
    
    # Input text box for the email content
    email_text = st.text_area("Enter Email Text", height=300)
    
    # Input for the Gemini API key
    api_key = "AIzaSyB0jEXbWexwC4VH5aNL3GuSjffxyxWk3QI"
    
    # Button to classify the email
    if st.button("Classify Email"):
        if email_text and api_key:
            with st.spinner("Classifying..."):
                # Call the classify_email_with_gemini function
                classification = classify_email_with_gemini(email_text, api_key)
                
                # Display the result
                if classification:
                    if classification.lower() == "spam":
                        st.markdown(f"**This email is classified as**: 🔴 Spam")
                    elif classification.lower() == "not spam":
                        st.markdown(f"**This email is classified as**: 🟢 Not Spam")
                    else:
                        st.markdown(f" {classification}")
                else:
                    st.error("Error during classification.")
        else:
            st.warning("Please provide both email text and Gemini API key.")