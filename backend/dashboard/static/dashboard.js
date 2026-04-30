// -----------------------
// CHART STYLE
// -----------------------
const layout = {
    paper_bgcolor:"#0f172a",
    plot_bgcolor:"#0f172a",
    font:{color:"white"}
};

// -----------------------
// FETCH LIVE DATA
// -----------------------
async function fetchLatest(){
    const res = await fetch("/api/latest");
    const data = await res.json();

    document.getElementById("soil").innerText = Math.round(data.soil) + "%";
    document.getElementById("temp").innerText = Math.round(data.temp) + "°C";
    document.getElementById("humidity").innerText = Math.round(data.humidity) + "%";

    const status = document.getElementById("status");

    if(data.soil < 30){
        status.innerText = "⚠️ Water needed";
        status.style.background = "red";
    }
    else if(data.temp > 30){
        status.innerText = "🔥 Too hot";
        status.style.background = "orange";
    }
    else{
        status.innerText = "✅ All good";
        status.style.background = "green";
    }
}


// -----------------------
// LOAD GRAPHS
// -----------------------
async function loadGraphs(){
    const res = await fetch("/api/history");
    const data = await res.json();

    const x = Array.from({length:data.soil.length}, (_,i)=>i);

    Plotly.newPlot("soilGraph", [{
        x:x,
        y:data.soil,
        type:"scatter"
    }], layout);

    Plotly.newPlot("tempGraph", [{
        x:x,
        y:data.temperature,
        type:"scatter"
    }], layout);

    Plotly.newPlot("humidityGraph", [{
        x:x,
        y:data.humidity,
        type:"scatter"
    }], layout);
}


// -----------------------
// LOOP
// -----------------------
fetchLatest();
loadGraphs();

setInterval(fetchLatest, 2000);
setInterval(loadGraphs, 10000);