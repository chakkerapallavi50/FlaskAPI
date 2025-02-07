import streamlit as st
import os
import json
from p import extract_text_from_pdf, extract_invoice_with_gemini, save_data_as_json

# Define the chat_page function to handle the invoice data extraction
def chat_page():
  
    
    # File uploader for PDF
    uploaded_file = st.file_uploader("Upload PDF", type=["pdf"])

    # Button to process the uploaded PDF
    if uploaded_file is not None:
        st.success("File uploaded successfully!")

        if st.button("Extract & Generate JSON"):
            with st.spinner("Processing..."):
                # Save uploaded PDF locally
                pdf_path = f"temp_{uploaded_file.name}"
                with open(pdf_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())

                # Extract text from PDF
                text = extract_text_from_pdf(pdf_path)

                # API Key (Replace with your own)
                api_key = "AIzaSyB0jEXbWexwC4VH5aNL3GuSjffxyxWk3QI"
                
                # Extract invoice data using Gemini AI
                invoice_data = extract_invoice_with_gemini(text, api_key)

                if invoice_data:
                    try:
                        # Parse the cleaned JSON response from Gemini AI
                        json_data = json.loads(invoice_data)
                        json_path = pdf_path.replace(".pdf", ".json")

                        # Save extracted data as JSON
                        save_data_as_json(json_data, json_path)
                        st.success("✅ JSON file created successfully!")

                        # Provide download link for JSON
                        with open(json_path, "r") as file:
                            st.download_button("Download JSON", file, file_name=os.path.basename(json_path), mime="application/json")

                        # Visualize the extracted invoice data below the download button
                        st.write("### Extracted Invoice Data:")
                        st.json(json_data)

                        # Cleanup: remove temp files
                        os.remove(pdf_path)  # Delete temp PDF
                        os.remove(json_path)  # Delete temp JSON after download

                    except json.JSONDecodeError as e:
                        st.error(f"Error decoding JSON: {e}")
                        st.text("Response received:")
                        st.code(invoice_data, language="json")
                else:
                    st.error("Failed to extract valid invoice data.")
