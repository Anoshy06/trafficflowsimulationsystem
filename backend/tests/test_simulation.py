import pytest
from src.engine.simulation import Simulation
from src.entities.vehicle import Vehicle

def test_simulation_routing_and_completion():
    sim = Simulation()
    sim.add_intersection("A", 0, 0)
    sim.add_intersection("B", 100, 0)
    sim.add_road("R1", "A", "B")

    v = Vehicle(["A", "B"], desired_speed=10.0)
    sim.add_vehicle(v)

    assert len(sim.vehicles) == 1
    assert v.current_road.id == "R1"
    assert v.finished is False

    # Perform steps to let the vehicle complete the route
    # R1 length is 100. At speed 10, it needs 10 seconds.
    # At time_step 0.1, we need 100 steps.
    for _ in range(101):
        sim.step()

    assert v.finished is True

def test_invalid_route_raises_exception():
    sim = Simulation()
    sim.add_intersection("A", 0, 0)
    sim.add_intersection("B", 100, 0)
    
    # Vehicle tries to go from A to C (C doesn't exist)
    v1 = Vehicle(["A", "C"], desired_speed=10.0)
    with pytest.raises(ValueError):
        sim.add_vehicle(v1)

    # Intersection C exists but no road A -> C
    sim.add_intersection("C", 0, 100)
    v2 = Vehicle(["A", "C"], desired_speed=10.0)
    with pytest.raises(ValueError):
        sim.add_vehicle(v2)

def test_simulation_overflow():
    sim = Simulation()
    sim.add_intersection("A", 0, 0)
    sim.add_intersection("B", 100, 0)
    sim.add_road("R1", "A", "B")
    
    # Let's set a low MAX_VEHICLES limit for testing if we implement it,
    # or let's test it raising an exception.
    # We will modify Simulation to have a max limit of 100 vehicles.
    sim.max_vehicles = 3
    
    sim.add_vehicle(Vehicle(["A", "B"], desired_speed=10.0, id="v1"))
    sim.add_vehicle(Vehicle(["A", "B"], desired_speed=10.0, id="v2"))
    sim.add_vehicle(Vehicle(["A", "B"], desired_speed=10.0, id="v3"))
    
    with pytest.raises(OverflowError):
        sim.add_vehicle(Vehicle(["A", "B"], desired_speed=10.0, id="v4"))
