import asyncio
import json
import random
import os
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from src.engine.simulation import Simulation
from src.entities.vehicle import Vehicle
from src.analytics.metrics import MetricsAnalyzer

app = FastAPI(title="Traffic Flow Simulation API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

simulation = Simulation()

def init_simulation():
    # Create a 2x2 grid
    # Intersections
    simulation.add_intersection("A", 100, 100)
    simulation.add_intersection("B", 500, 100)
    simulation.add_intersection("C", 100, 500)
    simulation.add_intersection("D", 500, 500)
    
    # Roads
    simulation.add_road("R_AB", "A", "B", speed_limit=40.0)
    simulation.add_road("R_BA", "B", "A", speed_limit=40.0)
    simulation.add_road("R_AC", "A", "C", speed_limit=40.0)
    simulation.add_road("R_CA", "C", "A", speed_limit=40.0)
    simulation.add_road("R_BD", "B", "D", speed_limit=40.0)
    simulation.add_road("R_DB", "D", "B", speed_limit=40.0)
    simulation.add_road("R_CD", "C", "D", speed_limit=40.0)
    simulation.add_road("R_DC", "D", "C", speed_limit=40.0)
    
    # Traffic Lights at intersections B and D
    simulation.add_traffic_light("TL_AB", "R_AB", initial_state="RED")
    simulation.add_traffic_light("TL_CB", "R_DB", initial_state="GREEN")
    
    simulation.running = True

init_simulation()

@app.post("/api/start")
async def start_sim():
    simulation.running = True
    return {"status": "started"}

@app.post("/api/pause")
async def pause_sim():
    simulation.running = False
    return {"status": "paused"}

@app.post("/api/reset")
async def reset_sim():
    global simulation
    simulation = Simulation()
    init_simulation()
    return {"status": "reset"}

@app.post("/api/add_vehicle")
async def add_vehicle():
    routes = [
        ["A", "B", "D"],
        ["C", "D", "B"],
        ["A", "C", "D"],
        ["D", "B", "A"],
        ["C", "A", "B"]
    ]
    route = random.choice(routes)
    # Speed is slightly randomized
    vehicle = Vehicle(route=route, desired_speed=30.0 + random.uniform(-10, 10))
    simulation.add_vehicle(vehicle)
    return {"status": "added", "vehicle_id": vehicle.id, "route": route}

async def simulation_loop():
    while True:
        if simulation.running:
            try:
                simulation.step()
            except Exception as e:
                print(f"Simulation error: {e}")
        await asyncio.sleep(simulation.time_step)

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(simulation_loop())

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            state = simulation.get_state()
            metrics = {
                "avg_waiting_time": MetricsAnalyzer.calculate_average_waiting_time(simulation.vehicles),
                "throughput": MetricsAnalyzer.calculate_throughput(simulation.vehicles),
                "congestion": MetricsAnalyzer.calculate_congestion(list(simulation.roads.values()))
            }
            
            # include intersection coords for frontend drawing
            static_data = {
                "intersections": [{"id": k, "x": v.x, "y": v.y} for k, v in simulation.intersections.items()],
                "roads": [{"id": k, "start": v.start_node.id, "end": v.end_node.id} for k, v in simulation.roads.items()]
            }
            
            payload = {
                "static": static_data,
                "state": state,
                "metrics": metrics
            }
            await websocket.send_text(json.dumps(payload))
            await asyncio.sleep(simulation.time_step)
    except WebSocketDisconnect:
        print("Client disconnected")

# Mount static frontend files
frontend_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../frontend"))
app.mount("/", StaticFiles(directory=frontend_path, html=True), name="frontend")
