import streamlit as st
import google.generativeai as genai
import json

# Function to classify text using Gemini AI
def chat_page():
    def classify_text_with_gemini(text, api_key):
        """
        Uses Gemini AI to classify the given text into predefined labels.
        """
        genai.configure(api_key=api_key)
        
        # Define the prompt for Gemini AI
        prompt = f"""
        Given the following text:
        
        {text}
        
        Please classify the text into one of the following categories:
        
        - Technology
        - Finance
        - Medical
        - Agriculture
        
        Respond only with a JSON object in the following format:
        {{
            "{text}": "<Technology | Finance | Medical | Agriculture>"
        }}      if the user input doesnot belongs to any of the mentioned  <Technology | Finance | Medical | Agriculture>  give output as "general"
        """
        
        # Initialize the Gemini model
        model = genai.GenerativeModel("gemini-1.5-flash")
        
        try:
            # Generate the response from Gemini AI
            response = model.generate_content(prompt)
            
            # Log the raw response to check what is returned
            print("Raw Response from Gemini AI:", response.text)
            
            if not response.text.strip():
                raise ValueError("Empty response from Gemini AI.")
            
            # Clean up the response
            clean_response = response.text.strip().lstrip("```json").rstrip("```").strip()
            
            # Convert the cleaned response to JSON
            classification_result = json.loads(clean_response)
            return classification_result
        
        except Exception as e:
            print(f"Error during AI request: {e}")
            return None

    # Streamlit UI
    st.title("Text Classification")

    # Input text box for the text content
    text_input = st.text_input("Enter Text")

    # Input for the Gemini API key
    api_key = "AIzaSyB0jEXbWexwC4VH5aNL3GuSjffxyxWk3QI"  # Replace with your actual Gemini API key

    # Button to classify the text
    if st.button("Classify Text"):
        if text_input and api_key:
            with st.spinner("Classifying..."):
                # Call the function to classify text
                classification_result = classify_text_with_gemini(text_input, api_key)
                
                # Display the result in JSON format
                if classification_result:
                    st.json(classification_result)
                else:
                    st.error("Error during text classification.")
        else:
            st.warning("Please enter text and provide the API key.")
