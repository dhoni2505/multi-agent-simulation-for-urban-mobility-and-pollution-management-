import streamlit as st

# Define the pages
home_page = st.Page("pages/home.py", title="Home", icon="🏠", default=True)
detector_page = st.Page("pages/detector.py", title="Pollution Detector", icon="🚗")
about_page = st.Page("pages/about.py", title="About the Project", icon="ℹ️")

# Initialize Navigation
pg = st.navigation([home_page, detector_page, about_page])
st.set_page_config(page_title="Urban Mobility MAS", layout="wide")

# Run Navigation
pg.run()