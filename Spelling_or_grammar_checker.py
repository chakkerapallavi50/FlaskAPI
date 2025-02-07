import streamlit as st
import google.generativeai as genai
import json

def chat_page():
    def correct_grammar_with_gemini(text, api_key):
        """
        Uses Gemini AI to correct grammar and spelling in the provided text.
        Returns the corrected text.
        """
        genai.configure(api_key=api_key)
        
        # Define the structured prompt
        prompt = f"""
        You are an AI language assistant that corrects grammar and spelling mistakes.
        
        Given the following text:
        
        "{text}"
        
        Please correct any grammar and spelling mistakes while preserving the original meaning.
        
        Respond only with a JSON object in the following format:
        {{
            "corrected_text": "<Corrected text here>"
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
            correction_result = json.loads(clean_response)
            return correction_result
        
        except Exception as e:
            print(f"Error during AI request: {e}")
            return None

    # Streamlit UI
    st.title("📝 Grammar & Spelling Corrector")
    st.write("""
        Enter a text below, and the AI will correct grammar and spelling errors.
    """)

    # Text input box for the content
    text_input = st.text_area("Enter text to correct", height=200)

    # Hardcoded Gemini API key
    api_key = "AIzaSyB0jEXbWexwC4VH5aNL3GuSjffxyxWk3QI"

    # Button to correct the text
    if st.button("Correct Text"):
        if text_input and api_key:
            with st.spinner("Correcting... Please wait."):
                # Call the correction function
                correction_result = correct_grammar_with_gemini(text_input, api_key)
                
                # Display the corrected text
                if correction_result:
                    st.success("Correction Successful!")
                    st.markdown(f"**Corrected Text:** {correction_result['corrected_text']}")
                else:
                    st.error("Error generating correction. Please try again.")
        else:
            st.warning("Please enter text before correcting.")

# Run the Streamlit app
if __name__ == "__main__":
    chat_page()
