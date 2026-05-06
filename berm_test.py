import RPi.GPIO as GPIO
import time
from pythonosc.udp_client import SimpleUDPClient

# --- CONFIGURATION ---
PIN = 27                # GPIO sensor pin
OSC_IP = "127.0.0.1"    # Localhost (same Pi)
OSC_PORT = 7701         # Your working QLC+ port
OSC_PATH = "/255"       # Your working OSC path
OSC_VALUE_ON = 255      # "Press" value
OSC_VALUE_OFF = 0       # "Release" value

# --- INITIALIZATION ---
client = SimpleUDPClient(OSC_IP, OSC_PORT)

GPIO.setmode(GPIO.BCM)
# Using PUD_UP assumes your sensor pulls to Ground (0) when triggered
GPIO.setup(PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

last_state = 1

print(f"--- System Ready ---")
print(f"Monitoring PIN {PIN}...")
print(f"Sending OSC to {OSC_IP}:{OSC_PORT} via {OSC_PATH}")

# --- MAIN LOOP ---
try:
    while True:
        current_state = GPIO.input(PIN)

        # Trigger logic: when state changes from 1 (High) to 0 (Low)
        if current_state == 0 and last_state == 1:
            print("SENSOR DETECTED! Triggering QLC+ Function...")
            
            # 1. Send "Press"
            client.send_message(OSC_PATH, OSC_VALUE_ON)
            
            # 2. Brief pause then send "Release" (to reset the QLC+ button)
            time.sleep(0.1)
            client.send_message(OSC_PATH, OSC_VALUE_OFF)
            
            # 3. Debounce: ignore sensor for 0.5s to avoid double-triggers
            time.sleep(0.5) 
            print("Ready for next trigger.")

        last_state = current_state
        time.sleep(0.05) # CPU-friendly polling rate

except KeyboardInterrupt:
    print("\nShutting down safely...")
    GPIO.cleanup()