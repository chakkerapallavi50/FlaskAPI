import fitz  # PyMuPDF
import google.generativeai as genai
import json
import re
 
# Function to extract text from the PDF
def extract_text_from_pdf(pdf_path):
    document = fitz.open(pdf_path)
    full_text = ""
    for page_num in range(document.page_count):
        page = document.load_page(page_num)
        full_text += page.get_text("text")  # Extract text from each page
    return full_text
 
# Function to extract invoice details using Gemini AI
def extract_invoice_with_gemini(text, api_key):
    genai.configure(api_key=api_key)  # Set API key
    
    prompt = f"""
    Extract the following details from this invoice text:
 
    {text}
 
    Return the result in JSON format with these fields:
 
    - Invoice details (number, order number, invoice date, due date, total due)  
    - Sender details (name, address, email)  
    - Recipient details (name, address, email)  
    - Items (quantity, service, rate, adjustment, sub-total)  
    - Tax details (tax amount)  
    - Bank details (bank name, account number, BSB number)  
 
    Ensure the output is valid JSON.
    """
 
    model = genai.GenerativeModel("gemini-1.5-flash")
 
    try:
        response = model.generate_content(prompt)
 
        # Log the raw response
        print("Raw Response from Gemini AI:", response.text)
 
        if not response.text.strip():
            raise ValueError("Empty response from Gemini AI.")
 
        # Clean up the response by removing ```json and ```
        clean_response = re.sub(r"^```json\s*|\s*```$", "", response.text.strip(), flags=re.MULTILINE)
 
        print("Cleaned Response from Gemini AI:", clean_response)
 
        return clean_response
 
    except Exception as e:
        print(f"Error during AI request: {e}")
        return None
 
# Function to save extracted data as JSON
def save_data_as_json(data, output_path):
    with open(output_path, 'w') as json_file:
        json.dump(data, json_file, indent=4) 
    print(f"Data saved to {output_path}")
 
# Main function
def main():
    pdf_path = "Invoice_3.pdf"  # Update with your PDF file path
    output_json_path = pdf_path.rsplit(".", 1)[0] + ".json"
 # Output JSON file
    api_key = "AIzaSyB0jEXbWexwC4VH5aNL3GuSjffxyxWk3QI"  # Replace with your valid API key
 
    # Extract text from the PDF
    text = extract_text_from_pdf(pdf_path)
 
    # Use Gemini AI to process the invoice and eximport fitz  # PyMuPDF import google.generativeai as genai import json import re   # Function to extract text from the PDF def extract_text_from_pdf(pdf_path):     document = fitz.open(pdf_path)     full_text = ""     for page_num in range(document.page_count):         page = document.load_page(page_num)         full_text += page.get_text("text")  # Extract text from each page     return full_text   # Function to extract invoice details using Gemini AI def extract_invoice_with_gemini(text, api_key):     genai.configure(api_key=api_key)  # Set API key          prompt = f"""     Extract the following details from this invoice text:       {text}       Return the result in JSON format with these fields:       - Invoice details (number, order number, invoice date, due date, total due)       - Sender details (name, address, email)       - Recipient details (name, address, email)       - Items (quantity, service, rate, adjustment, sub-total)       - Tax details (tax amount)       - Bank details (bank name, account number, BSB number)         Ensure the output is valid JSON.     """       model = genai.GenerativeModel("gemini-1.5-flash")       try:         response = model.generate_content(prompt)           # Log the raw response         print("Raw Response from Gemini AI:", response.text)           if not response.text.strip():             raise ValueError("Empty response from Gemini AI.")           # Clean up the response by removing ```json and ```         clean_response = re.sub(r"^```json\s*|\s*```$", "", response.text.strip(), flags=re.MULTILINE)           print("Cleaned Response from Gemini AI:", clean_response)           return clean_response       except Exception as e:         print(f"Error during AI request: {e}")         return None   # Function to save extracted data as JSON def save_data_as_json(data, output_path):     with open(output_path, 'w') as json_file:         json.dump(data, json_file, indent=4)     print(f"Data saved to {output_path}")   # Main function def main():     pdf_path = "Invoice_6.pdf"  # Update with your PDF file path     output_json_path = pdf_path.split('.'[0]+".json")  # Output JSON file     api_key = "AIzaSyB0jEXbWexwC4VH5aNL3GuSjffxyxWk3QI"  # Replace with your valid API key       # Extract text from the PDF     text = extract_text_from_pdf(pdf_path)       # Use Gemini AI to process the invoice and extract structured data     invoice_data = extract_invoice_with_gemini(text, api_key)       if invoice_data:         try:             json_data = json.loads(invoice_data)  # Parse JSON after cleaning             save_data_as_json(json_data, output_json_path)         except json.JSONDecodeError as e:             print(f"Error decoding JSON: {e}")             print("Response received:", invoice_data)     else:         print("No valid response to parse.")   # Run the main function if __name__ == "__main__":     main()    tract structured data
    invoice_data = extract_invoice_with_gemini(text, api_key)
 
    if invoice_data:
        try:
            json_data = json.loads(invoice_data)  # Parse JSON after cleaning
            save_data_as_json(json_data, output_json_path)
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
            print("Response received:", invoice_data)
    else:
        print("No valid response to parse.")
 
# Run the main function
if __name__ == "__main__":
    main()
 
 