# Software Engineering & Construction Report: Traffic Flow Simulation System

This report documents the architectural, methodological, and process-related aspects of the Traffic Flow Simulation System. The system was designed following strict software construction principles, including modular design, refactoring, performance optimization, and rigorous testing.

---

## 1. Process Model (Agile Iterations)

The development followed an **Agile Scrum framework** divided into four logical sprints. Each sprint delivered a set of verified, independent features simulated through Git branch isolation.

```mermaid
gantt
    title Agile Sprint Timeline
    dateFormat  YYYY-MM-DD
    section Sprints
    Sprint 1: Core Engine             :active, s1, 2026-05-19, 1d
    Sprint 2: Traffic Lights & Safety :active, s2, after s1, 1d
    Sprint 3: Analytics & Controller  :active, s3, after s2, 1d
    Sprint 4: UI, Testing & SPI       :active, s4, after s3, 1d
```

- **Sprint 1: Core Simulation Engine (`feature/simulation-engine`)**
  - **Goal**: Build the basic physics model and coordinates grid.
  - **Deliverable**: Road network representation (intersections, roads) and timestep vehicle position interpolation.
- **Sprint 2: Traffic Lights & Safety (`feature/traffic-lights`)**
  - **Goal**: Integrate control components and collision-prevention rules.
  - **Deliverable**: Traffic light state machine and vehicle-to-vehicle collision avoidance logic.
- **Sprint 3: Controller Layer & Analytics (`feature/analytics`)**
  - **Goal**: Build APIs for interactive control and data aggregation.
  - **Deliverable**: Metrics calculations (waiting time, throughput, congestion) and a WebSocket controller in FastAPI.
- **Sprint 4: UI & Process Improvement (`feature/ui`, `feature/testing`)**
  - **Goal**: Create the visual front-end dashboard and complete validation.
  - **Deliverable**: Real-time Glassmorphism HTML5 Canvas visualization, robust unit tests, and performance improvements.

---

## 2. Refactoring Requirement

### Before Refactoring: Monolithic Simulation Loop
In initial exploratory prototyping, the simulation loop was structured as a single massive monolithic loop doing entity updates, drawing, and statistics calculation all in one place:

```python
# BEFORE (Monolithic Conceptual Prototype)
def simulation_tick(vehicles, roads, lights, canvas):
    for vehicle in vehicles:
        # Move vehicle
        vehicle.distance += vehicle.speed * 0.1
        # Stop at lights
        for light in lights:
            if light.is_red() and vehicle.is_near(light):
                vehicle.speed = 0
        # Collision prevention
        for other in vehicles:
            if other != vehicle and vehicle.is_too_close(other):
                vehicle.speed = 0
        # Draw directly
        canvas.draw_circle(vehicle.x, vehicle.y, 5)
    # Calculate stats directly
    avg_wait = sum(v.wait_time for v in vehicles) / len(vehicles)
```

### After Refactoring: Entity-Engine-Controller Separation
The prototype was refactored into a highly modular, decoupled architecture:
1. **Entities Module (`src/entities/`)**: Focuses entirely on state and behavior of individual objects (`Vehicle`, `Road`, `TrafficLight`, `Intersection`). They contain no visualization logic and no global simulation rules.
2. **Simulation Engine (`src/engine/`)**: Handles the time-step progression, coordinate tracking, and coordination between different roads and intersections.
3. **Controller Layer (`src/controller/`)**: Provides communication endpoints (REST API/WebSockets) to decouple the visual rendering engine (Frontend Canvas) from the computational backend.
4. **Analytics Module (`src/analytics/`)**: Encapsulates all reporting calculations (`MetricsAnalyzer`), allowing independent modification of analytics algorithms without altering core movement physics.

---

## 3. Software Process Improvement (SPI)

### Optimization of Simulation Performance & Safety
During sprint testing, the collision avoidance logic was identified as a potential performance bottleneck ($O(N^2)$ cross-comparison between all vehicles globally). 

#### Process Improvement Implemented:
1. **Spatial Hashing/Bucketing by Road**:
   - Instead of comparing each vehicle against every other vehicle in the global array, vehicles are stored and sorted inside their respective `Road` object.
   - For any vehicle, collision checks are reduced to $O(1)$ by only checking the vehicle immediately ahead of it on the exact same road segment (`next_vehicle_distance`).
2. **Simulation Overflow Guard**:
   - Implemented a proactive capacity check (`max_vehicles` guard) to prevent system resource exhaustion (Memory/CPU spikes) under heavy test loads.
   - Raises an explicit `OverflowError` rather than failing silently or causing frame-rate degradation.

---

## 4. Lehman's Laws of Software Evolution Justification

The evolution of the Traffic Flow Simulation System matches several of **Lehman's Laws of Software Evolution**:

1. **Law of Continuing Change**:
   - *Application*: A traffic simulation system must continuously adapt to modern transportation updates (e.g., adding autonomous vehicles, smart vehicle-to-infrastructure communication).
2. **Law of Increasing Complexity**:
   - *Application*: As new roads, complex multi-lane highways, and adaptive roundabouts are introduced, the network graph structure grows exponentially complex. The modularization of `src/entities/` was a direct response to handle this complexity without mutating the simulation loop in `src/engine/`.
3. **Law of Feedback Systems**:
   - *Application*: To optimize city congestion, the system cannot operate purely as a feed-forward simulator; it requires an active feedback loop where analytics (average waiting times) dynamically adjust traffic light timings (adaptive signals).

---

## 5. Peer Review Simulation

### Code Review Checklist
- [x] **Modular Design**: Are entities kept free of presentation logic?
- [x] **Collision Prevention**: Is safe distance enforced robustly?
- [x] **Error Handling**: Are invalid routes and missing intersections handled gracefully?
- [x] **Code Cleanliness**: Are variable names clear and type-hinted where possible?

### Review Comments & Feedback
- **Reviewer**: "The spatial optimization of sorting vehicles on roads works wonderfully. However, if a vehicle is transferring from one road to another at an intersection, does it check for collisions with vehicles at the start of the next road?"
- **Resolution/Action**: Added an explicit route connection check and clamp vehicle speeds at intersections to ensure zero-collision transitions when switching roads in `_transfer_vehicle_to_next_road`.

---
*End of Report.*
