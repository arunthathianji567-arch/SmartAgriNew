from flask import Flask, request, jsonify
from datetime import datetime
import threading

app = Flask(__name__)

# Latest ESP32 sensor data
latest_data = {
    "temperature": 0.0,
    "humidity": 0.0,
    "soil": 0,
    "soil_status": "DISCONNECTED",
    "water_distance": 0.0,
    "pump_status": False,
    "time": "Waiting for ESP32 data..."
}

data_lock = threading.Lock()


@app.route("/")
def home():
    return jsonify({
        "status": "online",
        "message": "SmartAgri Render backend is running"
    })


@app.route("/health")
def health():
    return jsonify({
        "status": "online",
        "message": "SmartAgri Render backend is running"
    })


@app.route("/sensor", methods=["POST"])
def receive_sensor_data():

    try:
        incoming = request.get_json(silent=True)

        if not incoming:
            return jsonify({
                "status": "error",
                "message": "Invalid JSON"
            }), 400

        temperature = float(
            incoming.get("temperature", 0)
        )

        humidity = float(
            incoming.get("humidity", 0)
        )

        soil = int(
            incoming.get(
                "soil_moisture",
                incoming.get("soil", 0)
            )
        )

        water_distance = float(
            incoming.get("water_distance", 0)
        )

        pump_status = bool(
            incoming.get("pump_status", False)
        )

        # Soil status
        if soil < 1200:
            soil_status = "DRY"
        elif soil < 2800:
            soil_status = "NORMAL"
        else:
            soil_status = "WET"

        # Update latest data
        with data_lock:

            latest_data.update({
                "temperature": temperature,
                "humidity": humidity,
                "soil": soil,
                "soil_status": soil_status,
                "water_distance": water_distance,
                "pump_status": pump_status,
                "time": datetime.now().strftime(
                    "%d-%m-%Y %I:%M:%S %p"
                )
            })

        print()
        print("========== ESP32 DATA ==========")
        print(latest_data)
        print("================================")
        print()

        return jsonify({
            "status": "success",
            "message": "Sensor data received"
        }), 200

    except Exception as error:

        print()
        print("========== SENSOR ERROR ==========")
        print(error)
        print("==================================")
        print()

        return jsonify({
            "status": "error",
            "message": str(error)
        }), 500


@app.route("/data", methods=["GET"])
def get_data():

    with data_lock:
        return jsonify(latest_data)


if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False
    )