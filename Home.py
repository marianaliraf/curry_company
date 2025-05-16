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
    <p style='color:white;'>
    The Growth Dashboard was built to monitor growth metrics for Delivery Personnel and Restaurants.
    </p>
    <h3 style='color:white;'>How to use this Growth Dashboard?</h3>
    <ul style='color:white;'>
        <li><b>Business View:</b>
            <ul>
                <li>Management View: General behavior metrics.</li>
                <li>Tactical View: Weekly growth indicators.</li>
                <li>Geographic View: Geolocation insights.</li>
            </ul>
        </li>
        <li><b>Delivery View:</b>
            <ul>
                <li>Monitoring weekly growth indicators.</li>
            </ul>
        </li>
        <li><b>Restaurant View:</b>
            <ul>
                <li>Weekly growth indicators for restaurants.</li>
            </ul>
        </li>
    </ul>
    """,
    unsafe_allow_html=True
)
