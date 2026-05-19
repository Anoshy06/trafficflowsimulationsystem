import uuid

class Vehicle:
    def __init__(self, route: list, desired_speed: float, id: str = None):
        """
        route: list of intersection IDs representing the path.
        """
        self.id = id or str(uuid.uuid4())
        self.route = route
        self.current_route_index = 0
        self.current_road = None
        self.distance_on_road = 0.0
        self.desired_speed = desired_speed
        self.current_speed = 0.0
        self.waiting_time = 0.0
        self.total_time = 0.0
        self.finished = False

    def update_position(self, delta_time: float, next_vehicle_distance: float = None, is_light_red: bool = False):
        if self.finished or self.current_road is None:
            return

        self.total_time += delta_time

        # Calculate target speed
        target_speed = self.desired_speed

        # Stop at red light if near the end of the road
        distance_to_end = self.current_road.length - self.distance_on_road
        stopping_distance = 10.0 # meters

        if is_light_red and distance_to_end < stopping_distance:
            target_speed = 0.0

        # Collision avoidance
        if next_vehicle_distance is not None:
            safe_distance = 5.0 # meters
            if next_vehicle_distance - self.distance_on_road < safe_distance:
                target_speed = 0.0

        # Update speed (simple instant acceleration for now)
        self.current_speed = target_speed

        if self.current_speed == 0:
            self.waiting_time += delta_time

        self.distance_on_road += self.current_speed * delta_time

    def get_position(self):
        if self.finished or self.current_road is None:
            return None
            
        start = self.current_road.start_node
        end = self.current_road.end_node
        
        if self.current_road.length == 0:
            return start.x, start.y
            
        progress = self.distance_on_road / self.current_road.length
        progress = max(0.0, min(1.0, progress)) # clamp between 0 and 1
        
        x = start.x + (end.x - start.x) * progress
        y = start.y + (end.y - start.y) * progress
        return x, y
