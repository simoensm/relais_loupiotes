from pythonosc import udp_client
import time

# Configuration based on your setup
PI_IP = "127.0.0.1" 
INPUT_PORT = 7701  # Port QLC+ is listening on
OSC_PATH = "/255"  # The path you mentioned

client = udp_client.SimpleUDPClient(PI_IP, INPUT_PORT)

def launch_stairville_function():
    print(f"Triggering OSC Path {OSC_PATH} on Port {INPUT_PORT}...")
    
    # Send '255' (Full intensity/Press)
    # QLC+ sees this and maps it to your Channel 23534
    client.send_message(OSC_PATH, 255) 
    
    # Optional: Send '0' after a short delay if it's a toggle button
    time.sleep(0.1)
    client.send_message(OSC_PATH, 0)
    print("Trigger Sent.")

if __name__ == "__main__":
    launch_stairville_function()