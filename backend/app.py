from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from firebase_config import db
from datetime import datetime
from alert_service import check_and_alert

app = Flask(__name__)
CORS(app)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/send_data", methods=["POST"])
def send_data():
    data = request.get_json()

    if not data:
        return jsonify({"status": "error", "message": "No data received"}), 400

    data["timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    db.child("grape-data").set(data)

    print("🔥 New sensor data:", data)

    alerts = check_and_alert(data)

    return jsonify({
        "status": "success",
        "data": data,
        "alerts": alerts
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)