class Intersection:
    def __init__(self, id: str, x: float, y: float):
        self.id = id
        self.x = x
        self.y = y
        self.out_roads = {} # maps destination intersection id to Road object
        self.in_roads = {}  # maps source intersection id to Road object
        
    def add_out_road(self, road):
        self.out_roads[road.end_node.id] = road
        
    def add_in_road(self, road):
        self.in_roads[road.start_node.id] = road
