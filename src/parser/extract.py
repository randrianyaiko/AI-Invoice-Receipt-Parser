from langchain_google_genai import ChatGoogleGenerativeAI
from src.parser.format_instructions import InvoiceReceipt as ResponseFormatter
from dotenv import load_dotenv
import os
load_dotenv()

def extract_invoice_receipt_data(text: str, api_key: str=os.getenv("GOOGLE_GEMINI_APIKEY")) -> dict:
    """
    Extracts structured data from the provided text using a language model.

    Args:
        text (str): The input text containing invoice or receipt information.

    Returns:
        dict: A dictionary containing the extracted structured data.
    """

    model = ChatGoogleGenerativeAI(
        model='gemini-2.0-flash',
        api_key=api_key
        )
    
    model_with_structure = model.with_structured_output(ResponseFormatter)    
    text = f""" Convert the text here into a structured format\n {text} \n"""
    print("Text to be processed:", text)
    structured_data =model_with_structure.invoke(text)
    print("Structured Data:", structured_data)
    return structured_data.model_dump_json()

