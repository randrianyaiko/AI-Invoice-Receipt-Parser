import os
import streamlit as st
from PIL import Image
import tempfile
from src.ocr.extraction import extract_text_from_image
from src.parser.extract import extract_invoice_receipt_data

LANGUAGES = {
                "English": "eng",
                "Spanish": "spa",
                "French": "fra",
                "German": "deu",
                "Italian": "ita"
            }


# ------------------------
# Configuration
# ------------------------
def configure_page():
    st.set_page_config(
        page_title="Invoice and Receipt Parser",
        layout="wide",
        initial_sidebar_state="expanded",
    )


# ------------------------
# Sidebar Content
# ------------------------
def display_sidebar():
    with st.sidebar:
        st.title("📄Receipt and Invoice parser")
        st.write(
            "Upload an image of the invoice or receipt to extract text and structure it into JSON."
        )
        st.markdown("---")

        st.subheader(" Configurations ")
        with st.form("api_key_form"):            
            # Language mapping for display and Tesseract codes
            selected_language = st.selectbox(
                "Select Language",
                options=list(LANGUAGES.keys()),
                index=0,
                help="Select the language for OCR extraction."
            )
            
            selected_language_code = LANGUAGES[selected_language]
            api_key_input = st.text_input(
                "Enter your Gemini API Key 🔐", 
                type="password",
                value=os.getenv("GOOGLE_GEMINI_APIKEY", "")
                )
            
            submitted = st.form_submit_button("Submit")
            if submitted:
                os.environ["GOOGLE_GEMINI_APIKEY"] = api_key_input
                os.environ["LANGUAGE"] = selected_language_code
                st.success("API key saved to environment for this session.")


# ------------------------
# Image Upload Widget
# ------------------------
def upload_image():
    return st.file_uploader(
        "📥 Upload an image (PNG, JPG, JPEG)",
        type=["png", "jpg", "jpeg"],
        help="Select an image file for OCR extraction.",
    )


# ------------------------
# Display Uploaded Image
# ------------------------
def show_uploaded_image(image_file, col):
    with col:
        st.subheader("Uploaded Image")
        image = Image.open(image_file)
        st.image(image, use_column_width=True)
    return image


# ------------------------
# Extract and Display Text
# ------------------------
def process_and_display_text(image, col):
    with col:
        st.subheader("Extracted Data")

        with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp_file:
            image.save(tmp_file.name)
            image_path = tmp_file.name

        try:
            text = extract_text_from_image(image_path,language=os.getenv("LANGUAGE"))
            json_data = extract_invoice_receipt_data(text)
            st.json(json_data)
        except Exception as e:
            text = f"❌ Error extracting text: {e}"
            st.error(text)
            return

        st.download_button(
            label="💾 Download Data",
            data=json_data,
            file_name="data_.json"
        )


# ------------------------
# Main App
# ------------------------
def main():
    configure_page()
    display_sidebar()

    st.title("Invoice and Receipt Parser")
    uploaded_file = upload_image()

    if uploaded_file:
        col1, col2 = st.columns(2)
        image = show_uploaded_image(uploaded_file, col1)
        process_and_display_text(image, col2)
    else:
        st.info("Please upload an image of the invoice or receipt to preview it, extract the text and struture it into JSON.")


if __name__ == "__main__":
    main()
