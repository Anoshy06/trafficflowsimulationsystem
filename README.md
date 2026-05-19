# Traffic Flow Simulation System (Full-Stack Software Construction Project)

A highly modular, full-stack real-time **Traffic Flow Simulation Engine & Visualization Dashboard** built as an advanced software construction demonstration project. The system models vehicle agents traversing a grid road network dynamically controlled by a synchronized traffic light state machine with live performance analytics.

---

## 🏗️ Architecture & Folder Structure

The project strictly follows decoupled architectural patterns (**Entity-Engine-Controller**) to isolate business logic, system physics, metrics reporting, and presentation.

```
trafficflowsimulationsystem/
├── backend/
│   ├── src/
│   │   ├── entities/       # Vehicle, Road, Intersection, TrafficLight state
│   │   ├── engine/         # Timestep-based physics simulation loop
│   │   ├── analytics/      # Waiting time, throughput, congestion metrics
│   │   └── controller/     # FastAPI app + WebSocket event streaming
│   ├── tests/              # Pytest unit tests (routing, lights, overflow)
│   └── requirements.txt    # Python dependencies
├── frontend/
│   ├── index.html          # Dashboard visualization HTML layout
│   ├── style.css           # Premium Dark Mode Glassmorphism stylesheet
│   └── app.js              # Canvas Rendering + WebSocket Event Handler
├── docs/
│   └── software_engineering_report.md # Agile Sprints, Refactoring & SPI Report
├── README.md               # Setup & System Instructions
└── .gitignore              # Git ignore rules
```

### Decoupled Data Flow & Architecture Diagram

```
+------------------+                   +--------------------+
|  HTML5 Canvas    |  <-- Websockets --| FastAPI Controller |
|  & JS UI         |   (State Updates) | (main.py Router)   |
| (frontend/app.js)|  --- HTTP Post -->|                    |
+------------------+   (Control Actions) +--------------------+
                                                |
                                        +--------------------+
                                        | Simulation Engine  |
                                        | (simulation.py)    |
                                        +--------------------+
                                          /         \
                             +-------------------+  +-------------------+
                             |  Entities Module  |  |  Analytics Module |
                             | (vehicle, road,   |  | (MetricsAnalyzer) |
                             |  traffic_light)   |  +-------------------+
                             +-------------------+
```

---

## ⚙️ Functional Features
- **Dynamic Vehicle Spawning**: Add vehicle agents dynamically onto randomized, valid routes spanning multiple intersections.
- **Synchronized State-Machine Traffic Lights**: Intersections utilize independent, time-cycling green/yellow/red light rules to regulate traffic flow.
- **High-Performance Collision Prevention**: Vehicle agents continuously evaluate their local road segment, slowing down or stopping dynamically when approaching red lights or leading vehicles.
- **Robust Exception Handling & Capacity Guards**: Explicitly guards against invalid route paths, missing road segments, and simulation overflow (too many active vehicle agents).
- **Real-Time Analytics Dashboard**: Continuously tracks and updates overall wait times, total vehicle throughput, and specific road congestion density metrics.

---

## 🚀 Quick Setup & Execution

### Prerequisites
- **Python 3.8+**
- **Modern Web Browser** (Chrome, Edge, Firefox, or Safari)

### 1. Backend Server Setup
From the repository root, create a virtual environment, install the backend dependencies, and boot the server:

```bash
# Create a Python virtual environment
python -m venv venv

# Activate the virtual environment
# Windows:
.\venv\Scripts\activate
# MacOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r backend/requirements.txt

# Start the FastAPI server using Uvicorn
uvicorn backend.src.controller.main:app --reload
```

The server will start at `http://localhost:8000`. You can view the automated interactive API documentation at `http://localhost:8000/docs`.

### 2. Launching the Visualization Dashboard
Simply open the `frontend/index.html` file directly in any browser (e.g. by double-clicking it, or running a local server like Live Server). 

The dashboard will automatically connect to the FastAPI WebSocket server, initialize the coordinate grid (Intersections **A, B, C, D**), and begin streaming metrics.
- Click **Start** to run the simulation loop.
- Click **Add Vehicle** to dynamically spawn a new car agent.
- Click **Pause** to freeze the simulation at any time-step.
- Click **Reset** to wipe the system state and initialize clean coordinate grids.

---

## 🧪 Running Unit Tests
All business rules, state machines, movement physics, and edge-case exceptions are verified via unit testing:

```bash
# From the backend/ folder
pytest tests
```

---

## 📝 Process Documentation
For an in-depth software engineering breakdown of Agile iterations, Lehman's laws, before-and-after refactoring diffs, code-review checklists, and process improvement benchmarks, please review:
👉 **[docs/software_engineering_report.md](docs/software_engineering_report.md)**