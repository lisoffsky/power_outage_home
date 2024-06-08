from flask import Flask, jsonify, request
import time
import requests
import datetime
import pytz

app = Flask(__name__)

# WordPress site details
wordpress_url = 'enter'
wordpress_username = 'enter'
wordpress_password = 'enter'

last_heartbeat = 0
power_outage_detected = False
power_outage_timestamp = None

# Set the desired timezone (GMT+3)
timezone = pytz.timezone('Europe/Moscow')

@app.route('/heartbeat', methods=['GET', 'POST'])
def receive_heartbeat():
    global last_heartbeat, power_outage_detected, power_outage_timestamp
    if request.method == 'POST':
        heartbeat_data = request.json
        print(f"Received heartbeat from Raspberry Pi: {heartbeat_data}")
        last_heartbeat = time.time()
        power_outage_detected = False
        power_outage_timestamp = None
        status = 'OK'
    else:
        current_time = time.time()
        elapsed_time = current_time - last_heartbeat
        minutes, _ = divmod(elapsed_time, 60)
        if minutes > 2:
            power_outage_detected = True
            power_outage_timestamp = datetime.datetime.now(timezone).strftime("%Y-%m-%d %H:%M:%S")
            status = 'Power Outage'
        else:
            status = 'OK'
    formatted_time = datetime.datetime.fromtimestamp(last_heartbeat, timezone).strftime("%Y-%m-%d %H:%M:%S")
    return jsonify(status=status, last_heartbeat=formatted_time)

@app.route('/status')
def get_status():
    global power_outage_detected, power_outage_timestamp, last_heartbeat
    current_time = time.time()
    elapsed_time = current_time - last_heartbeat
    minutes, seconds = divmod(elapsed_time, 60)
    hours, minutes = divmod(minutes, 60)
    out_of_power = f"{int(hours):02d}:{int(minutes):02d}:{int(seconds):02d}"
    if minutes > 2:
        power_outage_detected = True
        power_outage_timestamp = datetime.datetime.now(timezone).strftime("%Y-%m-%d %H:%M:%S")
        send_notification()
        return jsonify(status='Power Outage', last_heartbeat=datetime.datetime.fromtimestamp(last_heartbeat, timezone).strftime("%Y-%m-%d %H:%M:%S"), power_outage_timestamp=power_outage_timestamp, out_of_power=out_of_power)
    else:
        power_outage_detected = False
        power_outage_timestamp = None
        return jsonify(status='OK', last_heartbeat=datetime.datetime.fromtimestamp(last_heartbeat, timezone).strftime("%Y-%m-%d %H:%M:%S"), out_of_power=out_of_power)

def send_notification():
    global power_outage_timestamp
    data = {
        'title': 'Power Outage Notification',
        'content': f'A power outage has been detected at the Raspberry Pi Zero location. Power outage timestamp: {power_outage_timestamp}',
        'status': 'publish'
    }
    response = requests.post(f'{wordpress_url}/posts', json=data, auth=(wordpress_username, wordpress_password))
    if response.status_code == 201:
        print('Notification sent successfully')
    else:
        print(f'Failed to send notification. Status code: {response.status_code}')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
