import streamlit as st

st.title("ℹ️ About This Project")

# Technical Architecture Image


st.markdown("""
### Technical Methodology
Unlike traditional static models, this system uses a **decentralized approach**:
1. **The Environment:** A continuous space mapped via `OSMnx`.
2. **The Agents:** Each vehicle calculates its own path and emission footprint.
3. **The Feedback Loop:** Agents sense high pollution levels and adapt their routes 
   to simulate eco-conscious driving.

### The Team & Goal
Our goal is to provide urban planners with a **digital twin** of their city to test 
policies before they are implemented in the real world.
""")

st.image("https://images.unsplash.com/photo-1518005020453-eb5e638bc21c?auto=format&fit=crop&w=800&q=80", 
         caption="Data-Driven Urban Planning")