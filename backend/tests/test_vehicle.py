from src.entities.vehicle import Vehicle
from src.entities.intersection import Intersection
from src.entities.road import Road

def test_vehicle_movement():
    i1 = Intersection("A", 0, 0)
    i2 = Intersection("B", 100, 0)
    road = Road("R1", i1, i2, speed_limit=10.0)
    
    v = Vehicle(["A", "B"], desired_speed=10.0)
    road.add_vehicle(v)
    
    assert v.distance_on_road == 0.0
    v.update_position(1.0)
    assert v.distance_on_road == 10.0
    
def test_collision_avoidance():
    i1 = Intersection("A", 0, 0)
    i2 = Intersection("B", 100, 0)
    road = Road("R1", i1, i2, speed_limit=10.0)
    
    v1 = Vehicle(["A", "B"], desired_speed=10.0)
    v2 = Vehicle(["A", "B"], desired_speed=10.0)
    
    road.add_vehicle(v1)
    road.add_vehicle(v2)
    
    v1.distance_on_road = 20.0
    v2.distance_on_road = 18.0
    
    # v2 is behind v1, distance is 2.0 (less than safe_distance 5.0)
    v2.update_position(1.0, next_vehicle_distance=20.0)
    
    # speed should drop to 0
    assert v2.current_speed == 0.0
    assert v2.distance_on_road == 18.0
