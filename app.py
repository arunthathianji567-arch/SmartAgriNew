from flask import Flask, render_template, request, jsonify
from datetime import datetime

app = Flask(__name__)

sensor_data = {
    "temperature": 0.0,
    "humidity": 0.0,
    "soil": 0,
    "water_distance": 0.0,
    "pump_status": False,
    "soil_status": "WAITING",
    "time": "Waiting for ESP32 data..."
}


def to_bool(value):
    if isinstance(value, bool):
        return value

    if isinstance(value, (int, float)):
        return value != 0

    if isinstance(value, str):
        return value.lower().strip() in ["true", "1", "yes", "on"]

    return False


@app.route("/")
def dashboard():
    return render_template("dashboard.html")


@app.route("/data")
def get_data():
    return jsonify(sensor_data)


@app.route("/sensor", methods=["POST"])
def receive_sensor():
    global sensor_data

    data = request.get_json(silent=True)

    if not data:
        return jsonify({
            "status": "error",
            "message": "No JSON data received"
        }), 400

    temperature = data.get("temperature", 0)
    humidity = data.get("humidity", 0)
    soil = data.get("soil_moisture", data.get("soil", 0))
    water_distance = data.get("water_distance", 0)
    pump_status = to_bool(data.get("pump_status", False))

    try:
        soil_value = float(soil)

        if soil_value < 1200:
            soil_status = "DRY"
        elif soil_value < 2800:
            soil_status = "NORMAL"
        else:
            soil_status = "WET"

    except (ValueError, TypeError):
        soil_status = "UNKNOWN"

    sensor_data = {
        "temperature": temperature,
        "humidity": humidity,
        "soil": soil,
        "water_distance": water_distance,
        "pump_status": pump_status,
        "soil_status": soil_status,
        "time": datetime.now().strftime("%d-%m-%Y %I:%M:%S %p")
    }

    print()
    print("================================")
    print("ESP32 DATA RECEIVED")
    print("================================")
    print("Temperature :", temperature)
    print("Humidity    :", humidity)
    print("Soil        :", soil)
    print("Water       :", water_distance)
    print("Pump        :", pump_status)
    print("Soil Status :", soil_status)
    print("Time        :", sensor_data["time"])
    print("================================")

    return jsonify({
        "status": "success",
        "message": "Sensor data received"
    })


@app.route("/health")
def health():
    return jsonify({
        "status": "online",
        "message": "Flask server is running"
    })


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False
    )