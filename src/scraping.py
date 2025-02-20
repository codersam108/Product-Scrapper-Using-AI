import re
import requests
from bs4 import BeautifulSoup
from googlesearch import search

def search_product_urls(product_name):
    """
    Search for product pages using a Google search query.
    Returns a list of URLs.
    """
    query = f"{product_name} product"
    print("Searching for product URLs with query:", query)
    all_urls = []
    # Call search with only the query argument
    for i, url in enumerate(search(query)):
        if i >= 10:
            break
        all_urls.append(url)
    return all_urls



def scrape_weight_and_dimensions(url):
    """
    Scrapes the given URL for weight and dimensions using regex.
    """
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        response = requests.get(url, headers=headers)
    except Exception as e:
        print("Error fetching the webpage:", e)
        return "Not Found", "Not Found"
    if response.status_code != 200:
        return "Not Found", "Not Found"
    soup = BeautifulSoup(response.text, 'html.parser')
    page_text = soup.get_text(separator=' ', strip=True)
    weight_pattern = re.compile(r'\bweight[:\s]+([\d\.]+)\s*(kg|lbs)\b', re.IGNORECASE)
    dimensions_pattern = re.compile(r'\bdimensions?[:\s]+([\d\.]+\s*[xX×]\s*[\d\.]+\s*[xX×]\s*[\d\.]+)\s*(cm|in)\b', re.IGNORECASE)
    weight_match = weight_pattern.search(page_text)
    dimensions_match = dimensions_pattern.search(page_text)
    weight = f"{weight_match.group(1)} {weight_match.group(2)}" if weight_match else "Not Found"
    dimensions = f"{dimensions_match.group(1)} {dimensions_match.group(2)}" if dimensions_match else "Not Found"
    return weight, dimensions

def scrape_additional_specs(url):
    """
    Scrapes additional product specifications (Cooling Capacity, Key Component, Refrigerant,
    Compressor Type, Energy Efficiency) from the given URL.
    """
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        response = requests.get(url, headers=headers)
    except Exception as e:
        print("Error fetching additional specs:", e)
        return {
            "Cooling Capacity": "Not Found",
            "Key Component": "Not Found",
            "Refrigerant": "Not Found",
            "Compressor Type": "Not Found",
            "Energy Efficiency": "Not Found"
        }
    if response.status_code != 200:
        return {
            "Cooling Capacity": "Not Found",
            "Key Component": "Not Found",
            "Refrigerant": "Not Found",
            "Compressor Type": "Not Found",
            "Energy Efficiency": "Not Found"
        }
    soup = BeautifulSoup(response.text, 'html.parser')
    page_text = soup.get_text(separator=' ', strip=True)
    specs = {}
    spec_list = ["Cooling Capacity", "Key Component", "Refrigerant", "Compressor Type", "Energy Efficiency"]
    for spec in spec_list:
        pattern = re.compile(r'\b' + re.escape(spec) + r'[:\s]+([^\n|<]+)', re.IGNORECASE)
        match = pattern.search(page_text)
        specs[spec] = match.group(1).strip() if match else "Not Found"
    return specs
