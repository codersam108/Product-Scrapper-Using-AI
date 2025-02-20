import json
import openai
import streamlit as st

# Load API key from Streamlit secrets
openai.api_key = st.secrets["OPENAI_API_KEY"]

def fetch_product_details(product_name):
    """
    Calls the OpenAI API to generate a rich, customer-facing HTML template for the product.
    The output must be a JSON object with keys "description" and "short_description".
    """
    prompt = f"""
    You are to generate a detailed product description in HTML for the product '{product_name}'.
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
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=1200
        )
        result_text = response["choices"][0]["message"]["content"].strip()
        return json.loads(result_text)
    except Exception as e:
        st.error(f"Error: Failed to fetch product details. {e}")
        return None

def fetch_weight_dimensions_via_api(product_name):
    """
    Uses OpenAI API to retrieve product weight and dimensions.
    """
    prompt = f"""
    Provide the product weight and dimensions for "{product_name}".
    If exact values are not available, return "Not Found" for those keys.
    Return only a valid JSON object in the format:
    {{"weight": "<value>", "dimensions": "<value>"}}
    """
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
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
    Uses OpenAI API to retrieve additional product specifications.
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
            model="gpt-4",
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

# Streamlit UI
st.title("🔍 Product Scraper & AI Description Generator")

product_name = st.text_input("Enter Product Name:", "")

if st.button("Generate Description"):
    if not product_name:
        st.warning("Please enter a product name.")
    else:
        st.info("Fetching product details...")
        details = fetch_product_details(product_name)

        if details:
            st.subheader("Short Description")
            st.markdown(details["short_description"], unsafe_allow_html=True)

            st.subheader("Detailed Description")
            st.markdown(details["description"], unsafe_allow_html=True)

        st.info("Fetching weight and dimensions...")
        weight, dimensions = fetch_weight_dimensions_via_api(product_name)
        st.write(f"**Weight:** {weight}")
        st.write(f"**Dimensions:** {dimensions}")

        st.info("Fetching additional specifications...")
        specs = fetch_additional_specs_via_api(product_name)
        st.write("**Cooling Capacity:**", specs["Cooling Capacity"])
        st.write("**Key Component:**", specs["Key Component"])
        st.write("**Refrigerant:**", specs["Refrigerant"])
        st.write("**Compressor Type:**", specs["Compressor Type"])
        st.write("**Energy Efficiency:**", specs["Energy Efficiency"])
