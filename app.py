@app.route("/data")
def get_data():

    try:
        import urllib.request
        import json

        url = "https://smartagrinew.onrender.com/data"

        req = urllib.request.Request(
            url,
            headers={
                "User-Agent": "Mozilla/5.0"
            }
        )

        with urllib.request.urlopen(req, timeout=30) as response:

            raw = response.read().decode("utf-8")

            print()
            print("========== RENDER DATA ==========")
            print(raw)
            print("=================================")
            print()

            data = json.loads(raw)

            return jsonify(data)

    except Exception as e:

        print()
        print("========== DATA ERROR ==========")
        print(str(e))
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