from typing import List
from src.entities.vehicle import Vehicle
from src.entities.road import Road

class MetricsAnalyzer:
    @staticmethod
    def calculate_average_waiting_time(vehicles: List[Vehicle]) -> float:
        if not vehicles:
            return 0.0
        total_waiting_time = sum(v.waiting_time for v in vehicles)
        return total_waiting_time / len(vehicles)

    @staticmethod
    def calculate_throughput(vehicles: List[Vehicle]) -> int:
        return sum(1 for v in vehicles if v.finished)

    @staticmethod
    def calculate_congestion(roads: List[Road]) -> dict:
        congestion_data = {}
        for road in roads:
            # simple congestion: vehicles per 100 units of length
            if road.length > 0:
                density = (len(road.vehicles) / road.length) * 100
            else:
                density = 0
            congestion_data[road.id] = density
        return congestion_data
