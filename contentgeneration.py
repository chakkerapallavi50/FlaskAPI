import streamlit as st
import google.generativeai as genai

# Assign your Gemini API key to a variable
GEMINI_API_KEY = "AIzaSyB0jEXbWexwC4VH5aNL3GuSjffxyxWk3QI"  # Replace with your actual API key

def generate_content(topic, specifications):
    """
    Uses Gemini AI to generate content based on the topic and specifications.
    Returns the generated content.
    """
    if not GEMINI_API_KEY:
        return "API Key is missing!"
    
    genai.configure(api_key=GEMINI_API_KEY)
    
    prompt = f"""
    Generate content based on the given topic and specifications.
    
    Topic: {topic}
    
    Specifications: {specifications}
    
    Provide a well-structured response.
    """
    
    model = genai.GenerativeModel("gemini-1.5-flash")
    
    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"Error: {e}"

# Streamlit UI
def chat_page():
    st.title("📝 AI-Powered Content Generator")
    st.write("Enter a topic and specifications to generate high-quality content.")

    # Input fields
    topic = st.text_input("Enter Topic", "")
    specifications = st.text_area("Enter Specifications", "", height=150)

    # Generate Button
    if st.button("Generate Content"):
        if topic and specifications:
            with st.spinner("Generating content... Please wait."):
                generated_content = generate_content(topic, specifications)
                st.success("Content Generated Successfully!")
                st.text_area("Generated Content", generated_content, height=300)
        else:
            st.warning("Please enter both topic and specifications.")

# Run the Streamlit app
if __name__ == "__main__":
    chat_page()
