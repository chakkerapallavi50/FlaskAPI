import streamlit as st
import google.generativeai as genai
import json
 
# Function to classify sentiment using Gemini AI
def chat_page():
    def classify_sentiment_with_gemini(review_text, api_key):
        """
        Uses Gemini AI to classify review sentiment as POSITIVE, NEGATIVE, or NEUTRAL.
        """
        genai.configure(api_key=api_key)
        
        # Define the prompt for Gemini AI
        prompt = f"""
        Given the following customer review:
    
        {review_text}
    
        Please analyze the sentiment of this review and classify it into one of the following categories:
        
        - POSITIVE
        - NEGATIVE
        - NEUTRAL
        
        Respond only with a JSON object in the following format:
        {{
            "review": "<POSITIVE | NEGATIVE | NEUTRAL>"
        }}
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
            sentiment_result = json.loads(clean_response)
            return sentiment_result
    
        except Exception as e:
            print(f"Error during AI request: {e}")
            return None
    
    # Streamlit UI

    st.title("Customer Review Sentiment Analysis")

    
    # Input text box for the review content
    review_text = st.text_input("Enter Review Text")
    
    # Input for the Gemini API key
    api_key = "AIzaSyB0jEXbWexwC4VH5aNL3GuSjffxyxWk3QI"
    
    # Button to classify the review
    if st.button("Analyze Sentiment"):
        if review_text and api_key:
            with st.spinner("Analyzing..."):
                # Call the function to classify sentiment
                sentiment_result = classify_sentiment_with_gemini(review_text, api_key)
                
                # Display the result
                if sentiment_result:
                    st.json(sentiment_result)
                else:
                    st.error("Error during sentiment classification.")
        else:
            st.warning("Please enter review text.")
    
    