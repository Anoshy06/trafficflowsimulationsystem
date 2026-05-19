from src.entities.traffic_light import TrafficLight

def test_traffic_light_state_transitions():
    light = TrafficLight("TL1", initial_state="RED")
    light.red_duration = 5.0
    light.green_duration = 5.0
    light.yellow_duration = 2.0

    # 1. Start state is RED
    assert light.state == "RED"

    # 2. Update by 4 seconds (should remain RED)
    light.step(4.0)
    assert light.state == "RED"

    # 3. Update by 1.1 seconds (timer=5.1, exceeds red_duration 5.0).
    # Transition to GREEN, timer resets to 0.0 (or is updated relative to cycle, here we reset)
    light.step(1.1)
    assert light.state == "GREEN"
    assert light.timer == 0.0

    # 4. Update by 5.1 seconds (exceeds green_duration 5.0).
    # Transition to YELLOW
    light.step(5.1)
    assert light.state == "YELLOW"
    assert light.timer == 0.0

    # 5. Update by 2.1 seconds (exceeds yellow_duration 2.0).
    # Transition back to RED
    light.step(2.1)
    assert light.state == "RED"
    assert light.timer == 0.0
