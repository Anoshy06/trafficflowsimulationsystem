import math

class Road:
    def __init__(self, id: str, start_node, end_node, speed_limit: float = 15.0):
        self.id = id
        self.start_node = start_node
        self.end_node = end_node
        self.speed_limit = speed_limit
        self.vehicles = [] # Ordered list of vehicles on this road, from start to end (index 0 is furthest along)
        
        # Calculate length
        dx = end_node.x - start_node.x
        dy = end_node.y - start_node.y
        self.length = math.sqrt(dx**2 + dy**2)
        
    def add_vehicle(self, vehicle):
        self.vehicles.append(vehicle)
        vehicle.current_road = self
        vehicle.distance_on_road = 0.0
        
    def remove_vehicle(self, vehicle):
        if vehicle in self.vehicles:
            self.vehicles.remove(vehicle)
            vehicle.current_road = None
