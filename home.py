import streamlit as st

st.title("🏙️ Sustainable Urban Mobility Simulation")

# Introduction Image
st.image("https://images.unsplash.com/photo-1449824913935-59a10b8d2000?auto=format&fit=crop&w=1200&q=80", 
         caption="The Challenge of Modern Urban Infrastructure")

st.markdown("""
### Transforming Cities through Multi-Agent Systems
Rapid urbanization has intensified traffic congestion and air pollution. This project uses 
**Multi-Agent Simulation (MAS)** to model individual vehicle behaviors and their 
environmental impact in real-time.

**Core Features:**
* **Autonomous Agents:** Vehicles that react to pollution levels.
* **Real-World Data:** Integration with OpenStreetMap for accurate city grids.
* **Policy Testing:** Evaluate 'Green Zones' and traffic re-routing strategies.
""")

st.info("👈 Navigate to the **Pollution Detector** to start a live simulation.")