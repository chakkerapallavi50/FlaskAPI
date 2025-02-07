import streamlit as st
import google.generativeai as genai
import json

def summarize_text_with_gemini(text, api_key):
    genai.configure(api_key=api_key)
    
    prompt = f"""
    You are an AI assistant that summarizes text in a **well-structured format** with proper headings and bold text.

    Given the following text:
    
    "{text}"
    
    Please summarize the content and format it as follows:
    
    **Summary:**
    - Briefly summarize the main idea of the text in 2-3 sentences.

    **Key Points:**
    - List 3-5 key takeaways from the text.
    
    **Important Details:**
    - Mention any crucial statistics, dates, or facts.

    **Conclusion:**
    - Provide a short concluding remark.
    
    Ensure the response is formatted correctly with **bold text** and bullet points.
    """
    
    model = genai.GenerativeModel("gemini-1.5-flash")
    
    try:
        response = model.generate_content(prompt)
        if not response.text.strip():
            raise ValueError("Empty response from Gemini AI.")
        return response.text.strip()
    except Exception as e:
        print(f"Error during AI request: {e}")
        return None

def chat_page():
    st.title("📖 Text Summarization ")
    st.write("Enter a large text block below for text Summarization")

    text_input = st.text_area("Enter your text here", height=300)
    api_key = "AIzaSyB0jEXbWexwC4VH5aNL3GuSjffxyxWk3QI"

    if st.button("Summarize Text"):
        if text_input and api_key:
            with st.spinner("Summarizing... Please wait."):
                summary_result = summarize_text_with_gemini(text_input, api_key)
                if summary_result:
                    st.markdown(summary_result, unsafe_allow_html=True)
                else:
                    st.error("Error generating summary. Please try again.")
        else:
            st.warning("Please enter text before summarizing.")

# Ensure no conflicting imports
if __name__ == "__main__":
    chat_page()
