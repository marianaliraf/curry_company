import streamlit as st
from PIL import Image
import os
from styles.custom_css import inject_custom_css

st.set_page_config(
    page_title="Home",
    #page_icon=""
)

# Aplica o estilo personalizado
inject_custom_css()

image_path = os.path.join('images', 'logo_cury_company.png')
image = Image.open(image_path)
st.sidebar.image(image, width=120)

st.sidebar.markdown('# Curry Company')
st.sidebar.markdown('## Fastest Delivery in Town')
st.sidebar.markdown("""---""")

st.write("# Curry Company Growth Dashboard")

st.markdown(
    """
    The Growth Dashboard was built to monitor growth metrics for Delivery Personnel and Restaurants.
    
    ### How to use this Growth Dashboard?
    
    - Business View:
        - Management View: General behavior metrics.
        - Tactical View: Weekly growth indicators.
        - Geographic View: Geolocation insights.
    
    - Delivery View:
        - Monitoring weekly growth indicators.
    
    - Restaurant View:
        - Weekly growth indicators for restaurants.
"""
)