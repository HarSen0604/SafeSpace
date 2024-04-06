import serial
import time

# Define HC-05 module serial port
HC05_PORT = '/dev/ttyS0'  # Assuming the HC-05 is connected to the Pi's hardware UART

# Create a serial port object
hc05 = serial.Serial(HC05_PORT, 9600, timeout=1)

def post_hc05():
    # Send AT command to check if HC-05 module is responding
    hc05.write(b'AT\r\n')
    
    # Wait for response from HC-05
    time.sleep(0.5)
    
    # Check if HC-05 responded with "OK"
    response = hc05.read_all().decode('utf-8')
    if "OK" in response:
        return True  # Return true if HC-05 responded correctly
    else:
        return False  # Return false if HC-05 did not respond correctly

if __name__ == "__main__":
    try:
        # Perform Power-On Self-Test (POST)
        if post_hc05():
            print("HC-05 Power-On Self-Test passed.")  # Print success message if POST passed
        else:
            print("HC-05 Power-On Self-Test failed. Check wiring and module.")  # Print error message if POST failed
    except KeyboardInterrupt:
        pass
    finally:
        hc05.close()
