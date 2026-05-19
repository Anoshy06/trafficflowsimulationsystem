import time
from typing import Dict, List

from src.entities.vehicle import Vehicle
from src.entities.road import Road
from src.entities.intersection import Intersection
from src.entities.traffic_light import TrafficLight

class Simulation:
    def __init__(self):
        self.intersections: Dict[str, Intersection] = {}
        self.roads: Dict[str, Road] = {}
        self.vehicles: List[Vehicle] = []
        self.traffic_lights: Dict[str, TrafficLight] = {}
        self.time_step = 0.1 # 100ms
        self.running = False
        self.max_vehicles = 100 # Maximum allowed vehicles to prevent simulation overflow
        
    def add_intersection(self, id: str, x: float, y: float):
        intersection = Intersection(id, x, y)
        self.intersections[id] = intersection
        return intersection
        
    def add_road(self, id: str, start_id: str, end_id: str, speed_limit: float = 15.0):
        if start_id not in self.intersections or end_id not in self.intersections:
            raise KeyError("Start or End intersection not found")
        start_node = self.intersections[start_id]
        end_node = self.intersections[end_id]
        road = Road(id, start_node, end_node, speed_limit)
        self.roads[id] = road
        start_node.add_out_road(road)
        end_node.add_in_road(road)
        return road
        
    def add_traffic_light(self, id: str, road_id: str, initial_state: str = "RED"):
        if road_id not in self.roads:
            raise KeyError("Road not found")
        road = self.roads[road_id]
        light = TrafficLight(id, initial_state)
        self.traffic_lights[id] = light
        road.traffic_light = light
        return light
        
    def add_vehicle(self, vehicle: Vehicle):
        # 1. Prevent Simulation Overflow
        active_vehicles = [v for v in self.vehicles if not v.finished]
        if len(active_vehicles) >= self.max_vehicles:
            raise OverflowError("Simulation overflow: Maximum vehicle capacity reached!")

        # 2. Validate route
        if not vehicle.route or len(vehicle.route) < 2:
            raise ValueError("Vehicle route must have at least 2 nodes")
            
        # 3. Check for missing nodes/intersections in route
        for node_id in vehicle.route:
            if node_id not in self.intersections:
                raise ValueError(f"Intersection {node_id} in vehicle route does not exist")
            
        start_node_id = vehicle.route[0]
        end_node_id = vehicle.route[1]
        
        start_node = self.intersections[start_node_id]
        road = start_node.out_roads.get(end_node_id)
        
        if road is None:
            raise ValueError(f"No road between {start_node_id} and {end_node_id}")
            
        self.vehicles.append(vehicle)
        road.add_vehicle(vehicle)
        
    def step(self):
        # Update traffic lights
        for light in self.traffic_lights.values():
            light.step(self.time_step)
            
        # Update vehicles
        for road in self.roads.values():
            # sort vehicles on this road by distance (furthest first)
            road.vehicles.sort(key=lambda v: v.distance_on_road, reverse=True)
            
            for i, vehicle in enumerate(road.vehicles):
                # find distance to next vehicle
                next_vehicle_distance = None
                if i > 0:
                    next_vehicle = road.vehicles[i-1]
                    next_vehicle_distance = next_vehicle.distance_on_road
                    
                # check if light is red
                is_light_red = False
                if road.traffic_light and road.traffic_light.state == "RED":
                    is_light_red = True
                elif road.traffic_light and road.traffic_light.state == "YELLOW":
                    # For simplicity, treat yellow as red if too far from intersection (wait, just yellow=red)
                    is_light_red = True
                
                vehicle.update_position(self.time_step, next_vehicle_distance, is_light_red)
                
                # Check if vehicle reached end of road
                if vehicle.distance_on_road >= road.length:
                    self._transfer_vehicle_to_next_road(vehicle, road)
                    
    def _transfer_vehicle_to_next_road(self, vehicle: Vehicle, current_road: Road):
        vehicle.current_route_index += 1
        current_road.remove_vehicle(vehicle)
        
        if vehicle.current_route_index >= len(vehicle.route) - 1:
            # vehicle reached destination
            vehicle.finished = True
        else:
            # move to next road
            next_start_id = vehicle.route[vehicle.current_route_index]
            next_end_id = vehicle.route[vehicle.current_route_index + 1]
            
            node = self.intersections[next_start_id]
            next_road = node.out_roads.get(next_end_id)
            
            if next_road:
                next_road.add_vehicle(vehicle)
            else:
                vehicle.finished = True # invalid route, terminate
                
    def get_state(self):
        state = {
            "vehicles": [],
            "lights": []
        }
        for v in self.vehicles:
            pos = v.get_position()
            if pos and not v.finished:
                state["vehicles"].append({
                    "id": v.id,
                    "x": pos[0],
                    "y": pos[1]
                })
        for light in self.traffic_lights.values():
            state["lights"].append({
                "id": light.id,
                "state": light.state,
                "road_id": [r_id for r_id, r in self.roads.items() if r.traffic_light == light][0]
            })
        return state
