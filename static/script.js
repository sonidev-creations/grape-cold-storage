const firebaseConfig = {
    apiKey: "AIzaSyCI7BaNJD8Got6VqlHOvWoTPhIdGNKAO1U",
    authDomain: "grape-storage.firebaseapp.com",
    databaseURL: "https://grape-storage-default-rtdb.firebaseio.com/",
    storageBucket: "grape-storage.firebasestorage.app"
};

firebase.initializeApp(firebaseConfig);
const db = firebase.database();

function safeValue(value, unit = "") {
    return (value !== undefined && value !== null)
        ? `${value} ${unit}`
        : "--";
}

function updateUI(data) {
    document.getElementById("temperature").textContent =
        `Temperature: ${safeValue(data.temperature, "°C")}`;

    document.getElementById("humidity").textContent =
        `Humidity: ${safeValue(data.humidity, "%")}`;

    document.getElementById("gas").textContent =
        `Gas: ${safeValue(data.gas)}`;

    let tsDiv = document.getElementById("timestamp");
    if (tsDiv && data.timestamp) {
        tsDiv.textContent = `Last Update: ${data.timestamp}`;
    }

    const tempDiv = document.getElementById("temperature");
    const humidDiv = document.getElementById("humidity");

    tempDiv.style.color = "black";
    humidDiv.style.color = "black";

    if (data.temperature !== undefined) {
        if (data.temperature > 8) {
            tempDiv.style.color = "red";
        } else if (data.temperature < 0) {
            tempDiv.style.color = "blue";
        }
    }

    if (data.humidity !== undefined) {
        if (data.humidity > 90 || data.humidity < 30) {
            humidDiv.style.color = "red";
        }
    }
}

db.ref("sensor_readings")
    .limitToLast(1)
    .on("child_added", function(snapshot) {
        const data = snapshot.val();
        console.log("Live Data:", data);
        updateUI(data);
    });

db.ref(".info/connected").on("value", function(snapshot) {
    if (snapshot.val() === true) {
        console.log("✅ Connected to Firebase");
    } else {
        console.log("❌ Not connected to Firebase");
    }
});
async function manualRefresh() {
    try {
        const response = await fetch('/latest');
        const data = await response.json();
        updateUI(data);
    } catch (err) {
        console.error("Manual fetch failed:", err);
    }
}