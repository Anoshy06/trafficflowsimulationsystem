class TrafficLight:
    def __init__(self, id: str, initial_state: str = "RED"):
        self.id = id
        self.state = initial_state
        self.timer = 0.0
        self.red_duration = 5.0
        self.green_duration = 5.0
        self.yellow_duration = 2.0
        
    def step(self, delta_time: float):
        self.timer += delta_time
        if self.state == "RED" and self.timer >= self.red_duration:
            self.state = "GREEN"
            self.timer = 0.0
        elif self.state == "GREEN" and self.timer >= self.green_duration:
            self.state = "YELLOW"
            self.timer = 0.0
        elif self.state == "YELLOW" and self.timer >= self.yellow_duration:
            self.state = "RED"
            self.timer = 0.0
