Code to know exact time of power outage in my Kyiv appartment. 
As all known apps are not precise enough I've built a small Pi code which sends heartbeats to server. 
Raspberry Pi Zero is plugged into a regular socket and can't use my backup battery. 

heartbeat.py - located on Raspberry  
vps_code.py - located on my VPS with Wordpress project. It creates a web-page with basic info about last time when I had electricity and how much time passed since. 
