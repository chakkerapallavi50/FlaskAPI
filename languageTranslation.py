import streamlit as st
import google.generativeai as genai
import json

def detect_language_with_gemini(text, api_key):
    """
    Uses Gemini AI to detect the language of the provided text.
    Returns the detected language.
    """
    genai.configure(api_key=api_key)
    
    # Define the structured prompt for language detection
    prompt = f"""
    You are a language expert. Please detect the language of the following text:
    
    "{text}"
    
    Respond only with a JSON object in the following format:
    {{
        "detected_language": "<Detected language here>"
    }}
    """
    
    # Initialize the Gemini model
    model = genai.GenerativeModel("gemini-1.5-flash")
    
    try:
        # Generate the response from Gemini AI
        response = model.generate_content(prompt)
        
        # Log the raw response from Gemini AI for debugging
        print("Raw Response from Gemini AI:", response.text)
        
        if not response.text.strip():
            raise ValueError("Empty response from Gemini AI.")
        
        # Clean up the response
        clean_response = response.text.strip().lstrip("```json").rstrip("```").strip()
        
        # Convert the cleaned response to JSON
        language_result = json.loads(clean_response)
        return language_result['detected_language']
    
    except Exception as e:
        print(f"Error during AI request: {e}")
        return None


def translate_text_with_gemini(text, source_lang, target_lang, api_key):
    """
    Uses Gemini AI to translate the provided text into the target language specified.
    Returns the translated text.
    """
    genai.configure(api_key=api_key)
    
    # Define the structured prompt for translation
    prompt = f"""
    You are a professional translator. Please translate the following text from {source_lang} to {target_lang}:
    
    "{text}"
    
    Respond only with a JSON object in the following format:
    {{
        "translated_text": "<Translated text here>"
    }}
    """
    
    # Initialize the Gemini model
    model = genai.GenerativeModel("gemini-1.5-flash")
    
    try:
        # Generate the response from Gemini AI
        response = model.generate_content(prompt)
        
        # Log the raw response from Gemini AI for debugging
        print("Raw Response from Gemini AI:", response.text)
        
        if not response.text.strip():
            raise ValueError("Empty response from Gemini AI.")
        
        # Clean up the response
        clean_response = response.text.strip().lstrip("```json").rstrip("```").strip()
        
        # Convert the cleaned response to JSON
        translation_result = json.loads(clean_response)
        return translation_result['translated_text']
    
    except Exception as e:
        print(f"Error during AI request: {e}")
        return None


def chat_page():
    # Streamlit UI
    st.title("🌍 Language Detection & Translation")
    st.write("""
        Select whether you want to detect the language of the text or translate it.
    """)

    # Dropdown to select either "Detection" or "Translation"
    task_option = st.selectbox("Choose Task", ["Language Detection", "Translation"])

    if task_option == "Language Detection":
        st.write("""
            Enter text and the AI will detect the language.
        """)

        # Text input for detection
        text_input = st.text_area("Enter text for language detection", height=200)
        api_key = "AIzaSyB0jEXbWexwC4VH5aNL3GuSjffxyxWk3QI"  # Replace with your actual Gemini API key

        if st.button("Detect Language"):
            if text_input:
                with st.spinner("Detecting... Please wait."):
                    detected_language = detect_language_with_gemini(text_input, api_key)
                    
                    if detected_language:
                        st.success("Detection Successful!")
                        st.markdown(f"**Detected Language:** {detected_language}")
                    else:
                        st.error("Error detecting language. Please try again.")
            else:
                st.warning("Please enter text for language detection.")

    elif task_option == "Translation":
        st.write("""
            Enter text to translate and select the source and target languages.
        """)

        # Text input for translation
        text_input = st.text_area("Enter text to translate", height=200)

        # Language selection for translation
        source_language = st.selectbox("Select Source Language", ["English", "Spanish", "French", "German", "Chinese", "telugu","Tamil"])
        target_language = st.selectbox("Select Target Language", ["English", "Spanish", "French", "German", "Chinese", "telugu","Tamil"])
        api_key = "AIzaSyB0jEXbWexwC4VH5aNL3GuSjffxyxWk3QI"  # Replace with your actual Gemini API key

        if st.button("Translate Text"):
            if text_input:
                with st.spinner("Translating... Please wait."):
                    translated_text = translate_text_with_gemini(text_input, source_language, target_language, api_key)
                    
                    if translated_text:
                        st.success("Translation Successful!")
                        st.markdown(f"**Translated Text:** {translated_text}")
                    else:
                        st.error("Error generating translation. Please try again.")
            else:
                st.warning("Please enter text for translation.")

# Run the Streamlit app
if __name__ == "__main__":
    chat_page()
