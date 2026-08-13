import mesa
import random

class VehicleAgent(mesa.Agent):
    def __init__(self, model, vehicle_type="sedan"):
        super().__init__(model)
        self.vehicle_type = vehicle_type
        self.emission_rate = 5 if vehicle_type == "truck" else 2

    def move(self):
        # 1. Define current position
        cur_x, cur_y = self.pos
        
        # 2. Create a list of 8 potential directions (N, S, E, W, and diagonals)
        # We 'probe' the environment at these points
        probe_distance = 2
        potential_moves = [
            (cur_x + probe_distance, cur_y), (cur_x - probe_distance, cur_y),
            (cur_x, cur_y + probe_distance), (cur_x, cur_y - probe_distance),
            (cur_x + probe_distance, cur_y + probe_distance), (cur_x - probe_distance, cur_y - probe_distance)
        ]

        # 3. Find the cleanest point among the probes
        best_move = self.pos
        # We use the custom method we added to environment.py
        min_pollution = self.model.space.get_pollution_level(cur_x, cur_y)

        for move in potential_moves:
            # Stay within 0-100 bounds
            check_x = max(0, min(move[0], 99))
            check_y = max(0, min(move[1], 99))
            
            p_level = self.model.space.get_pollution_level(check_x, check_y)
            if p_level < min_pollution:
                min_pollution = p_level
                best_move = (check_x, check_y)

        # 4. Move to the best location (with a tiny bit of random noise for realism)
        final_x = max(0, min(best_move[0] + random.uniform(-0.5, 0.5), 99))
        final_y = max(0, min(best_move[1] + random.uniform(-0.5, 0.5), 99))
        
        self.model.space.move_agent(self, (final_x, final_y))

    def emit(self):
        self.model.space.update_pollution(self.pos[0], self.pos[1], self.emission_rate)

    def step(self):
        self.move()
        self.emit()