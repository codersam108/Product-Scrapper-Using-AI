import json
import openai
import streamlit as st
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Set the API key from Streamlit secrets (or .env if not deployed on Streamlit Cloud)
openai.api_key = st.secrets["OPENAI_API_KEY"] if "OPENAI_API_KEY" in st.secrets else os.getenv("OPENAI_API_KEY")
if not openai.api_key:
    st.error("OPENAI_API_KEY is not set in environment or secrets!")
    st.stop()

def fetch_product_details(product_name):
    """
    Uses the OpenAI API to generate a rich, customer-facing HTML product description.
    Expects a JSON object with keys "description" and "short_description".
    """
    prompt = f"""
You are to generate a detailed product description in HTML for the product "{product_name}".
Your output must be a valid JSON object with two keys:
  "description" and "short_description".

Generate a rich, customer-friendly HTML template that includes:
1. A header section with the product title and model information.
2. A "Description" section as an unordered list of 4 key features in the format:
   <li><b>Feature Name:</b> Explanation.</li>
3. A "Specifications" section as a table with rows for:
   - Cooling Capacity: [Insert Cooling Capacity]
   - Key Component: [Insert Key Component]
   - Energy Efficiency: [Insert Energy Efficiency]
   - Refrigerant: [Insert Refrigerant]
   - Compressor Type: [Insert Compressor Type]
4. A "General Information" section as a table with rows for details such as In The Box, Model Name, Star Rating, Operating Mode, and Product Category.
5. A "Product Dimensions" section as a table with rows for:
   - Indoor Unit Dimensions (W x H x D): [Insert Dimensions]
   - Indoor Unit Weight: [Insert Weight]

Also generate a "short_description" as a concise HTML summary (using an unordered list with 4 items).

Output only a valid JSON object with no extra text.
Example:
{{
  "description": "<div>... rich HTML ...</div>",
  "short_description": "<div>... concise HTML ...</div>"
}}
    """
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",  # Change to "gpt-3.5-turbo" if needed
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=1200
        )
        result_text = response["choices"][0]["message"]["content"].strip()
        return json.loads(result_text)
    except Exception as e:
        st.error(f"Error fetching product details: {e}")
        return None

def fetch_weight_dimensions_via_api(product_name):
    """
    Uses the OpenAI API as a fallback to retrieve the product's weight and dimensions.
    Expects a JSON response with keys "weight" and "dimensions".
    """
    prompt = f"""
Provide the product weight and dimensions for "{product_name}".
If exact values are not available, return "Not Found" for those keys.
Return only a valid JSON object in the format:
{{"weight": "<value>", "dimensions": "<value>"}}
    """
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # Change to "gpt-4" if needed
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
            max_tokens=150
        )
        result_text = response["choices"][0]["message"]["content"].strip()
        specs = json.loads(result_text)
        return specs.get("weight", "Not Found"), specs.get("dimensions", "Not Found")
    except Exception as e:
        st.error(f"Error fetching weight/dimensions: {e}")
        return "Not Found", "Not Found"

def fetch_additional_specs_via_api(product_name):
    """
    Uses the OpenAI API as a fallback to retrieve additional product specifications.
    Expects a JSON object with the following keys:
      Cooling Capacity, Key Component, Refrigerant, Compressor Type, Energy Efficiency.
    """
    prompt = f"""
Provide the following product specifications for "{product_name}":
Cooling Capacity, Key Component, Refrigerant, Compressor Type, Energy Efficiency.
Return only a valid JSON object in the following format:
{{"Cooling Capacity": "<value>", "Key Component": "<value>", "Refrigerant": "<value>", "Compressor Type": "<value>", "Energy Efficiency": "<value>"}}
If any information is not available, return "Not Found" for that key.
    """
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # Change to "gpt-4" if needed
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
            max_tokens=150
        )
        result_text = response["choices"][0]["message"]["content"].strip()
        return json.loads(result_text)
    except Exception as e:
        st.error(f"Error fetching additional specs: {e}")
        return {
            "Cooling Capacity": "Not Found",
            "Key Component": "Not Found",
            "Refrigerant": "Not Found",
            "Compressor Type": "Not Found",
            "Energy Efficiency": "Not Found"
        }
