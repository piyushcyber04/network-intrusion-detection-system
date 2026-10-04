from flask import Flask, jsonify, render_template, request

app = Flask(__name__)
alerts = []

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/alerts")
def get_alerts():
    return jsonify(alerts)

@app.route("/add_alert", methods=["POST"])
def add_alert_api():
    data = request.json
    alert = data.get("alert")
    if alert and alert not in alerts:
        alerts.append(alert)
    return jsonify({"status": "ok"})

if __name__ == "__main__":
    app.run(debug=True)
