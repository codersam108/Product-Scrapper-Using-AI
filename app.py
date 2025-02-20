import streamlit as st
import threading
from src.scraping import search_product_urls
from src.utils import main_logic

st.title("🔍 Product Scraper & AI Description Generator")

product_name = st.text_input("Enter Product Name:")

if st.button("Search URLs") and product_name:
    with st.spinner("Searching for product URLs..."):
        urls = search_product_urls(product_name)
        if urls:
            st.session_state.urls = urls
            st.success("URLs found!")
        else:
            st.error("No URLs found. Please try a different query.")

if "urls" in st.session_state:
    selected_url = st.selectbox("Select a Product URL", st.session_state.urls)
    if st.button("Run Scraper"):
        with st.spinner("Processing..."):
            result = main_logic(product_name, selected_url)
            st.subheader("Short Description")
            st.markdown(result.get("short_description", "Not Found"), unsafe_allow_html=True)
            st.subheader("Detailed Description")
            st.markdown(result.get("description", "Not Found"), unsafe_allow_html=True)
