// -----------------------
// GLOBAL CHART LAYOUT
// -----------------------
const layout = {
    paper_bgcolor: "#0f172a",
    plot_bgcolor: "#0f172a",
    font: { color: "white" },
    margin: { l: 50, r: 20, t: 20, b: 40 },
    xaxis: {
        gridcolor: "#1e293b",
        zeroline: false
    },
    yaxis: {
        gridcolor: "#1e293b",
        zeroline: false
    }
};

const chartStyle = {
    type: "scatter",
    mode: "lines",
    line: {
        width: 3
    }
};

// -----------------------
// HELPERS
// -----------------------
function updateTimestamp() {
    document.getElementById("updated").innerText =
        "Updated: " + new Date().toLocaleTimeString();
}

function setOnlineStatus(isOnline) {
    const badge = document.getElementById("liveBadge");

    if (isOnline) {
        badge.innerHTML = `<span class="dot"></span>LIVE`;
        badge.className = "live";
    } else {
        badge.innerHTML = `<span class="dot offline-dot"></span>OFFLINE`;
        badge.className = "offline";
    }
}

function setSystemStatus(message, type) {
    const status = document.getElementById("status");

    status.innerText = message;
    status.className = "status " + type;
}

function renderChart(id, x, y) {
    Plotly.react(id, [{
        ...chartStyle,
        x: x,
        y: y
    }], layout, { responsive: true });
}

// -----------------------
// FETCH LATEST VALUES
// -----------------------
async function fetchLatest() {
    try {
        const res = await fetch("/api/latest");

        if (!res.ok) throw new Error("API error");

        const data = await res.json();

        document.getElementById("soil").innerText =
            Math.round(data.soil) + "%";

        document.getElementById("temp").innerText =
            Math.round(data.temp) + "°C";

        document.getElementById("humidity").innerText =
            Math.round(data.humidity) + "%";

        if (data.soil < 30) {
            setSystemStatus("⚠️ Water needed", "danger");
        } else if (data.temp > 30) {
            setSystemStatus("🔥 Too hot", "warning");
        } else {
            setSystemStatus("✅ All good", "success");
        }

        updateTimestamp();
        setOnlineStatus(true);

    } catch (error) {
        setOnlineStatus(false);
        setSystemStatus("⚠️ Connection lost", "danger");
    }
}

// -----------------------
// LOAD HISTORY GRAPHS
// -----------------------
async function loadGraphs() {
    try {
        const res = await fetch("/api/history");

        if (!res.ok) throw new Error("API error");

        const data = await res.json();

        const x = Array.from(
            { length: data.soil.length },
            (_, i) => i + 1
        );

        renderChart("soilGraph", x, data.soil);
        renderChart("tempGraph", x, data.temperature);
        renderChart("humidityGraph", x, data.humidity);

    } catch (error) {
        console.error("Graph load failed:", error);
    }
}

// -----------------------
// STARTUP
// -----------------------
fetchLatest();
loadGraphs();

setInterval(fetchLatest, 2000);
setInterval(loadGraphs, 10000);