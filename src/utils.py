from src.openai_api import fetch_product_details, fetch_weight_dimensions_via_api, fetch_additional_specs_via_api
from src.scraping import scrape_weight_and_dimensions, scrape_additional_specs

def update_templates_with_specs(product_templates, weight, dimensions, additional_specs):
    """
    Replaces placeholders in the product templates with the provided specifications.
    """
    updated_description = product_templates.get("description", "")
    updated_description = updated_description.replace("[Insert Weight]", weight)
    updated_description = updated_description.replace("[Insert Dimensions]", dimensions)
    for key, placeholder in [("Cooling Capacity", "[Insert Cooling Capacity]"),
                             ("Key Component", "[Insert Key Component]"),
                             ("Refrigerant", "[Insert Refrigerant]"),
                             ("Compressor Type", "[Insert Compressor Type]"),
                             ("Energy Efficiency", "[Insert Energy Efficiency]")]:
        value = additional_specs.get(key, "Not Found")
        updated_description = updated_description.replace(placeholder, value)
    updated_short_description = product_templates.get("short_description", "")
    return {
        "description": updated_description,
        "short_description": updated_short_description
    }

def main_logic(product_name, selected_url):
    # Scrape weight and dimensions
    weight, dimensions = scrape_weight_and_dimensions(selected_url)
    if weight == "Not Found" or dimensions == "Not Found":
        api_weight, api_dimensions = fetch_weight_dimensions_via_api(product_name)
        if weight == "Not Found":
            weight = api_weight
        if dimensions == "Not Found":
            dimensions = api_dimensions

    # Scrape additional specifications
    additional_specs = scrape_additional_specs(selected_url)
    if any(val == "Not Found" for val in additional_specs.values()):
        api_specs = fetch_additional_specs_via_api(product_name)
        for key in additional_specs:
            if additional_specs[key] == "Not Found":
                additional_specs[key] = api_specs.get(key, "Not Found")

    product_templates = fetch_product_details(product_name)
    if not product_templates:
        return {"description": "Failed to retrieve product details from API.", "short_description": ""}
    return update_templates_with_specs(product_templates, weight, dimensions, additional_specs)
