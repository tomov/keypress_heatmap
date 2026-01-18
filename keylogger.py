import evdev
from evdev import InputDevice, categorize, ecodes
import datetime

# sudo apt install evtest
# sudo evtest
# REPLACE THIS with the path found in step 1
DEVICE_PATH = '/dev/input/event15' 
LOG_FILE = 'physical_keys_log.txt'

def log_keypresses():
    try:
        device = InputDevice(DEVICE_PATH)
        print(f"Monitoring physical input from: {device.name}")
        
        with open(LOG_FILE, "a") as f:
            # Iterate through the device event stream
            for event in device.read_loop():
                if event.type == ecodes.EV_KEY:
                    key_event = categorize(event)
                    
                    # key_down is 1, key_up is 0, key_hold is 2
                    # We only want to log the initial press (1)
                    if key_event.keystate == 1:
                        timestamp = datetime.datetime.now().isoformat()
                        key_name = key_event.keycode
                        
                        log_entry = f"{timestamp} - {key_name}\n"
                        f.write(log_entry)
                        f.flush() # Ensure it writes to disk immediately
                        
    except PermissionError:
        print("Error: You need root privileges to access raw input devices.")
        print("Try: sudo python3 script_name.py")
    except FileNotFoundError:
        print(f"Error: Device {DEVICE_PATH} not found.")

if __name__ == "__main__":
    log_keypresses()