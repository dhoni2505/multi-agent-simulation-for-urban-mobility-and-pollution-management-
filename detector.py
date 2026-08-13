import streamlit as st
import osmnx as ox
import folium
from streamlit_folium import st_folium
from folium.plugins import HeatMap
import branca.colormap as cm
from scripts.run_simulation import UrbanPollutionModel
import pandas as pd
import numpy as np

# --- 1. Persistent Data Handling ---
if "model_results" not in st.session_state:
    st.session_state.model_results = None

st.set_page_config(layout="wide")
st.title("🚗 Urban Mobility & Real-Time Pollution Detector")

# --- 2. Input Sidebar ---
st.sidebar.header("Simulation Settings")
location = st.sidebar.text_input("Enter City/Area:", "New York, USA")
v_count = st.sidebar.slider("Vehicles:", 20, 150, 50)
steps = st.sidebar.slider("Duration (Steps):", 50, 200, 100)

if st.sidebar.button("🚀 Start Simulation"):
    with st.spinner(f"Downloading Map and Live Data for {location}..."):
        try:
            model = UrbanPollutionModel(n_vehicles=v_count, location=location)
            
            # Optimized UI Progress
            pb = st.progress(0)
            for i in range(steps):
                model.step()
                if i % 10 == 0: pb.progress((i + 1) / steps)
            
            st.session_state.model_results = {
                "pollution_grid": model.space.pollution_grid,
                "baseline_aqi": model.space.baseline_aqi,
                "graph": model.space.graph,
                "location": location
            }
            st.success("Analysis Ready!")
        except Exception as e:
            st.error(f"Error: {e}")

# --- 3. Visualization Block ---
if st.session_state.model_results:
    res = st.session_state.model_results
    grid = res["pollution_grid"]
    
    if res["graph"]:
        # Extract Road GeoData
        nodes, edges = ox.graph_to_gdfs(res["graph"])
        
        # Dashboard Layout
        col1, col2 = st.columns([3, 1])
        
        with col1:
            st.subheader(f"Interactive Live Map: {res['location']}")
            
            # Create Map
            m = folium.Map(location=[nodes.y.mean(), nodes.x.mean()], zoom_start=15, tiles="CartoDB positron")

            # A. EXPLICIT ROAD LAYER (Fixes visibility)
            folium.GeoJson(
                edges, 
                name="Road Network",
                style_function=lambda x: {'color': '#2c3e50', 'weight': 2, 'opacity': 0.6}
            ).add_to(m)

            # B. COLOR LEGEND
            max_p = float(grid.max()) + 0.1
            colormap = cm.LinearColormap(['yellow', 'orange', 'red', 'darkred'], 
                                         vmin=float(grid.min()), vmax=max_p, 
                                         caption="Pollution Level")
            m.add_child(colormap)

            # C. HAZARD MARKERS (Top 5)
            r = grid.shape[0]
            top_5 = np.argsort(grid.flatten())[-5:]
            for idx in top_5:
                x, y = np.unravel_index(idx, grid.shape)
                lat = float(nodes.y.min() + (y / r) * (nodes.y.max() - nodes.y.min()))
                lng = float(nodes.x.min() + (x / r) * (nodes.x.max() - nodes.x.min()))
                folium.Marker([lat, lng], icon=folium.Icon(color='red', icon='warning', prefix='fa')).add_to(m)

            # D. HEATMAP LAYER
            heat_data = [[float(nodes.y.min() + (y/r)*(nodes.y.max()-nodes.y.min())), 
                          float(nodes.x.min() + (x/r)*(nodes.x.max()-nodes.x.min())), 
                          float(grid[x,y])] 
                         for x in range(r) for y in range(r) if grid[x,y] > 0]
            
            HeatMap(heat_data, radius=15, blur=10, min_opacity=0.3).add_to(m)

            # Final Render with Unique Key
            st_folium(m, width=900, height=600, key="simulation_map")

        with col2:
            st.subheader("Metrics")
            st.metric("Live City AQI", f"{int(res['baseline_aqi'])}")
            st.write(f"**Total Grid Coverage:** {r}x{r}")
            
            # Export
            df = pd.DataFrame(grid)
            st.download_button("📥 Export CSV", df.to_csv().encode('utf-8'), f"{location}.csv")