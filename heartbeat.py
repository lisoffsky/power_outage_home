import requests
import time

vps_url = 'enter'

while True:
    try:
        heartbeat_data = {'data': 'heartbeat'}
        response = requests.post(vps_url, json=heartbeat_data)
        
        if response.status_code == 200:
            print('Heartbeat sent successfully')
        else:
            print(f'Failed to send heartbeat. Status code: {response.status_code}')
    
    except requests.exceptions.RequestException as e:
        print(f'Error sending heartbeat: {e}')
    
    time.sleep(60)  # Send heartbeat every 60 seconds (1 minute)
