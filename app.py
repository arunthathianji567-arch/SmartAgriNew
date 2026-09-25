from flask import Flask, render_template, jsonify
import urllib.request
import json
import os

app = Flask(__name__)

RENDER_DATA_URL = "https://smartagrinew.onrender.com/data"


@app.route("/")
def dashboard():
    return render_template("dashboard.html")


@app.route("/data")
def get_data():

    try:

        request = urllib.request.Request(
            RENDER_DATA_URL,
            headers={
                "User-Agent": "Mozilla/5.0"
            }
        )

        with urllib.request.urlopen(
            request,
            timeout=30
        ) as response:

            raw = response.read().decode("utf-8")

            print()
            print("========== RENDER DATA ==========")
            print(raw)
            print("=================================")
            print()

            data = json.loads(raw)

            return jsonify(data)

    except Exception as error:

        print()
        print("========== DATA ERROR ==========")
        print(error)
        print("================================")
        print()

        return jsonify({
            "temperature": 0.0,
            "humidity": 0.0,
            "soil": 0,
            "water_distance": 0.0,
            "pump_status": False,
            "soil_status": "DISCONNECTED",
            "time": "Waiting for ESP32 data..."
        }), 503


@app.route("/health")
def health():

    return jsonify({
        "status": "online",
        "message": "Local Flask server is running"
    })


if __name__ == "__main__":

    port = int(
        os.environ.get(
            "PORT",
            5000
        )
    )

    app.run(
        host="127.0.0.1",
        port=port,
        debug=False
    )