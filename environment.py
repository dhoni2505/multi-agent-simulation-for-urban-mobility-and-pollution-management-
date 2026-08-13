import requests
import numpy as np
import osmnx as ox
import mesa
import os
from dotenv import load_dotenv

load_dotenv()

class UrbanGrid(mesa.space.ContinuousSpace):
    def __init__(self, location_name, x_max, y_max, grid_resolution=40):
        super().__init__(x_max, y_max, torus=False)
        self.resolution = grid_resolution
        self.x_max, self.y_max = x_max, y_max
        
        # 1. Fetch Real-Time Baseline AQI
        self.baseline_aqi = self.fetch_realtime_aqi(location_name)
        self.pollution_grid = np.full((grid_resolution, grid_resolution), self.baseline_aqi / 20.0)
        
        # 2. Load Map
        try:
            ox.settings.use_cache = True
            self.graph = ox.graph_from_address(location_name, dist=800, network_type="drive")
        except Exception as e:
            self.graph = None

    def fetch_realtime_aqi(self, city):
        token = os.getenv("WAQI_TOKEN")
        url = f"https://api.waqi.info/feed/{city}/?token={token}"
        try:
            response = requests.get(url, timeout=5).json()
            if response['status'] == 'ok':
                return float(response['data']['aqi'])
        except:
            pass
        return 0.0

    def update_pollution(self, x, y, amount):
        """Translates continuous agent coords to grid cells and adds pollution."""
        grid_x = int(min(max(x / self.x_max * (self.resolution - 1), 0), self.resolution - 1))
        grid_y = int(min(max(y / self.y_max * (self.resolution - 1), 0), self.resolution - 1))
        self.pollution_grid[grid_x, grid_y] += amount

    # --- THE MISSING METHOD ---
    def get_pollution_level(self, x, y):
        """Allows 'Smart Agents' to probe the environment for pollution levels."""
        grid_x = int(min(max(x / self.x_max * (self.resolution - 1), 0), self.resolution - 1))
        grid_y = int(min(max(y / self.y_max * (self.resolution - 1), 0), self.resolution - 1))
        return self.pollution_grid[grid_x, grid_y]