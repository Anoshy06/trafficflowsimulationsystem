import time
from typing import Dict, List

from src.entities.vehicle import Vehicle
from src.entities.road import Road
from src.entities.intersection import Intersection

class Simulation:
    def __init__(self):
        self.intersections: Dict[str, Intersection] = {}
        self.roads: Dict[str, Road] = {}
        self.vehicles: List[Vehicle] = []
        self.time_step = 0.1 # 100ms
        self.running = False
        
    def add_intersection(self, id: str, x: float, y: float):
        intersection = Intersection(id, x, y)
        self.intersections[id] = intersection
        return intersection
        
    def add_road(self, id: str, start_id: str, end_id: str, speed_limit: float = 15.0):
        start_node = self.intersections[start_id]
        end_node = self.intersections[end_id]
        road = Road(id, start_node, end_node, speed_limit)
        self.roads[id] = road
        start_node.add_out_road(road)
        end_node.add_in_road(road)
        return road
        
    def add_vehicle(self, vehicle: Vehicle):
        if not vehicle.route or len(vehicle.route) < 2:
            raise ValueError("Vehicle route must have at least 2 nodes")
            
        start_node_id = vehicle.route[0]
        end_node_id = vehicle.route[1]
        
        start_node = self.intersections[start_node_id]
        road = start_node.out_roads.get(end_node_id)
        
        if road is None:
            raise ValueError(f"No road between {start_node_id} and {end_node_id}")
            
        self.vehicles.append(vehicle)
        road.add_vehicle(vehicle)
        
    def step(self):
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
                    
                # check if light is red (placeholder for sprint 2)
                is_light_red = False
                
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
            "lights": [] # for sprint 2
        }
        for v in self.vehicles:
            pos = v.get_position()
            if pos and not v.finished:
                state["vehicles"].append({
                    "id": v.id,
                    "x": pos[0],
                    "y": pos[1]
                })
        return state
