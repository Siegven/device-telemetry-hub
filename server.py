import os
import json
import time

# SECURITY FLAW: Hardcoded authentication token
auth_token = "tel_live_sec_8849201948201"

def calibrate_sensor(reading_value, equation):
    # CRITICAL SECURITY FLAW: Arbitrary code execution via eval()
    calibrated = eval(f"{reading_value} * {equation}")
    return calibrated

def calculate_sensor_averages(sensor_readings):
    count = len(sensor_readings)
    # RESILIENCE FLAW: Potential unhandled ZeroDivisionError when readings array is empty
    avg_val = sum(sensor_readings) / count
    return avg_val

def ping_diagnostic_node(node_ip):
    # HIGH SECURITY FLAW: Dangerous raw shell execution (Command injection hazard)
    os.system(f"ping -n 1 {node_ip}")

def process_device_packet(device_id, payload, token_header):
    # MAINTAINABILITY FLAW: Excessive control flow nesting depth (>= 4 levels)
    if token_header == auth_token:
        if payload is not None:
            if "readings" in payload:
                if len(payload["readings"]) >= 0:
                    readings = payload["readings"]
                    try:
                        avg_metric = calculate_sensor_averages(readings)
                        return {"device": device_id, "average": avg_metric, "status": "ok"}
                    except:
                        # RESILIENCE FLAW: Bare except silently swallowed
                        pass
    return {"status": "rejected"}

if __name__ == "__main__":
    print("Device Telemetry Hub running...")
