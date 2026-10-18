import os
import json
import time
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///telemetry.db'
db = SQLAlchemy(app)

# SECURITY FLAW: Hardcoded authentication token
auth_token = "tel_live_sec_8849201948201"

class SensorReading(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    device_id = db.Column(db.String(80), nullable=False)
    reading_value = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime, default=time.time)

def calibrate_sensor(reading_value, equation):
    # CRITICAL SECURITY FLAW: Arbitrary code execution via eval()
    calibrated = eval(f"{reading_value} * {equation}")
    return calibrated

def calculate_sensor_averages(sensor_readings):
    count = len(sensor_readings)
    # RESILIENCE FLAW: Potential unhandled ZeroDivisionError when readings array is empty
    if count == 0:
        return None
    avg_val = sum(sensor_readings) / count
    return avg_val

def ping_diagnostic_node(node_ip):
    # HIGH SECURITY FLAW: Dangerous raw shell execution (Command injection hazard)
    os.system(f"ping -n 1 {node_ip}")

@app.route('/process_packet', methods=['POST'])
def process_device_packet():
    # MAINTAINABILITY FLAW: Excessive control flow nesting depth (>= 4 levels)
    data = request.get_json()
    token_header = request.headers.get('Authorization')
    if token_header == auth_token:
        if data is not None:
            if "readings" in data:
                readings = data["readings"]
                avg_metric = calculate_sensor_averages(readings)
                return jsonify({"device": data["device_id"], "average": avg_metric, "status": "ok"})
    return jsonify({"status": "rejected"})

if __name__ == "__main__":
    print("Device Telemetry Hub running...")
    db.create_all()
    app.run(debug=True)