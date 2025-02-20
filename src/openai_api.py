import json
import openai
from dotenv import load_dotenv
load_dotenv()  # This loads the variables from your .env file
import os


openai.api_key = os.getenv("OPENAI_API_KEY")

def fetch_product_details(product_name):
    """
    Calls the OpenAI API to generate a rich, customer-facing HTML template for the product.
    The output must be a JSON object with keys "description" and "short_description".
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
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # Change to gpt-4 if you have access
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        max_tokens=1200
    )
    result_text = response.choices[0].message.content.strip()
    try:
        return json.loads(result_text)
    except json.JSONDecodeError:
        print("Error: The API response is not valid JSON. Raw response:")
        print(result_text)
        return None

def fetch_weight_dimensions_via_api(product_name):
    """
    Fallback: Uses OpenAI API to retrieve weight and dimensions.
    Expects a JSON response with keys "weight" and "dimensions".
    """
    prompt = f"""
Provide the product weight and dimensions for "{product_name}".
If exact values are not available, return "Not Found" for those keys.
Return only a valid JSON object in the format:
{{"weight": "<value>", "dimensions": "<value>"}}
    """
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
        max_tokens=150
    )
    result_text = response.choices[0].message.content.strip()
    try:
        specs = json.loads(result_text)
        return specs.get("weight", "Not Found"), specs.get("dimensions", "Not Found")
    except Exception as e:
        print("Error fetching weight/dimensions from API:", e)
        return "Not Found", "Not Found"

def fetch_additional_specs_via_api(product_name):
    """
    Fallback: Uses OpenAI API to retrieve additional specifications.
    Expects a JSON object with keys: Cooling Capacity, Key Component, Refrigerant, Compressor Type, Energy Efficiency.
    """
    prompt = f"""
Provide the following product specifications for "{product_name}":
Cooling Capacity, Key Component, Refrigerant, Compressor Type, Energy Efficiency.
Return only a valid JSON object in the following format:
{{"Cooling Capacity": "<value>", "Key Component": "<value>", "Refrigerant": "<value>", "Compressor Type": "<value>", "Energy Efficiency": "<value>"}}
If any information is not available, return "Not Found" for that key.
    """
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
        max_tokens=150
    )
    result_text = response.choices[0].message.content.strip()
    try:
        return json.loads(result_text)
    except Exception as e:
        print("Error fetching additional specs from API:", e)
        return {
            "Cooling Capacity": "Not Found",
            "Key Component": "Not Found",
            "Refrigerant": "Not Found",
            "Compressor Type": "Not Found",
            "Energy Efficiency": "Not Found"
        }
