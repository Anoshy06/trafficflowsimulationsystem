const API_URL = "http://localhost:8000/api";
const WS_URL = "ws://localhost:8000/ws";

const canvas = document.getElementById("sim-canvas");
const ctx = canvas.getContext("2d");

let simState = {
    static: { intersections: [], roads: [] },
    state: { vehicles: [], lights: [] },
    metrics: {}
};

let ws;

function connectWebSocket() {
    ws = new WebSocket(WS_URL);
    ws.onmessage = (event) => {
        const data = JSON.parse(event.data);
        if (data.static) simState.static = data.static;
        if (data.state) simState.state = data.state;
        if (data.metrics) simState.metrics = data.metrics;
        
        render();
        updateDashboard();
    };
    ws.onclose = () => {
        console.log("WebSocket disconnected. Retrying...");
        setTimeout(connectWebSocket, 1000);
    };
}

function render() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    
    // Draw roads
    ctx.strokeStyle = "#475569";
    ctx.lineWidth = 20;
    simState.static.roads.forEach(road => {
        const start = simState.static.intersections.find(i => i.id === road.start);
        const end = simState.static.intersections.find(i => i.id === road.end);
        if (start && end) {
            ctx.beginPath();
            ctx.moveTo(start.x, start.y);
            ctx.lineTo(end.x, end.y);
            ctx.stroke();
            
            // Draw center line
            ctx.strokeStyle = "#94a3b8";
            ctx.lineWidth = 2;
            ctx.setLineDash([10, 10]);
            ctx.beginPath();
            ctx.moveTo(start.x, start.y);
            ctx.lineTo(end.x, end.y);
            ctx.stroke();
            ctx.setLineDash([]);
            ctx.strokeStyle = "#475569";
            ctx.lineWidth = 20;
        }
    });

    // Draw Intersections
    ctx.fillStyle = "#334155";
    simState.static.intersections.forEach(node => {
        ctx.beginPath();
        ctx.arc(node.x, node.y, 15, 0, Math.PI * 2);
        ctx.fill();
        
        // Node labels
        ctx.fillStyle = "#fff";
        ctx.font = "12px Inter";
        ctx.textAlign = "center";
        ctx.textBaseline = "middle";
        ctx.fillText(node.id, node.x, node.y);
        ctx.fillStyle = "#334155";
    });

    // Draw Traffic Lights
    simState.state.lights.forEach(light => {
        const road = simState.static.roads.find(r => r.id === light.road_id);
        if (road) {
            const end = simState.static.intersections.find(i => i.id === road.end);
            const start = simState.static.intersections.find(i => i.id === road.start);
            if (start && end) {
                // place light slightly before the intersection
                const dx = end.x - start.x;
                const dy = end.y - start.y;
                const len = Math.sqrt(dx*dx + dy*dy);
                const offset = 25;
                const lx = end.x - (dx/len) * offset;
                const ly = end.y - (dy/len) * offset;
                
                ctx.fillStyle = light.state === "RED" ? "#ef4444" : 
                               light.state === "YELLOW" ? "#eab308" : "#22c55e";
                ctx.beginPath();
                ctx.arc(lx, ly, 8, 0, Math.PI * 2);
                ctx.fill();
                ctx.strokeStyle = "#ffffff";
                ctx.lineWidth = 2;
                ctx.stroke();
            }
        }
    });

    // Draw Vehicles
    ctx.fillStyle = "#60a5fa";
    simState.state.vehicles.forEach(v => {
        ctx.beginPath();
        ctx.arc(v.x, v.y, 6, 0, Math.PI * 2);
        ctx.fill();
        ctx.strokeStyle = "#ffffff";
        ctx.lineWidth = 1.5;
        ctx.stroke();
    });
}

function updateDashboard() {
    if(!simState.metrics) return;
    
    document.getElementById("val-wait").textContent = (simState.metrics.avg_waiting_time || 0).toFixed(1) + "s";
    document.getElementById("val-throughput").textContent = simState.metrics.throughput || 0;
    
    const congestionContainer = document.getElementById("val-congestion");
    congestionContainer.innerHTML = "";
    if (simState.metrics.congestion) {
        for (const [roadId, density] of Object.entries(simState.metrics.congestion)) {
            const div = document.createElement("div");
            div.className = "road-item";
            div.innerHTML = `<span>${roadId}</span><span>${density.toFixed(1)}</span>`;
            congestionContainer.appendChild(div);
        }
    }
}

// API Calls
async function postAction(action) {
    try {
        await fetch(`${API_URL}/${action}`, { method: 'POST' });
    } catch (e) {
        console.error("API Error", e);
    }
}

document.getElementById("start-btn").addEventListener("click", () => postAction("start"));
document.getElementById("pause-btn").addEventListener("click", () => postAction("pause"));
document.getElementById("reset-btn").addEventListener("click", () => postAction("reset"));
document.getElementById("add-vehicle-btn").addEventListener("click", () => postAction("add_vehicle"));

connectWebSocket();
