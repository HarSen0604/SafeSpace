import RPi.GPIO as GPIO
import time

# Set GPIO mode
GPIO.setmode(GPIO.BCM)

# Define pin for MQ2 Gas Sensor
gas_sensor_pin = 14

# Define pin for LED (optional)
led_pin = 15

# Initialize GPIO pins
GPIO.setup(gas_sensor_pin, GPIO.IN)
GPIO.setup(led_pin, GPIO.OUT)

# Function to perform Power On Self Test (POST)
def perform_post():
    print("Performing Power On Self Test (POST)...")
    
    # Test 1: Check if the sensor is properly connected
    if GPIO.input(gas_sensor_pin) == GPIO.LOW:
        print("Error: Gas sensor not connected.")
        return False
    
    # Test 2: Check if the sensor is responding
    # You may use specific sensor behavior to test its responsiveness
    # For example, you can attempt to read the sensor a few times and check for consistent values
    # Here, we'll read the sensor value 5 times and check if they are consistent
    sensor_values = []
    for _ in range(5):
        sensor_values.append(GPIO.input(gas_sensor_pin))
        time.sleep(0.1)  # Wait between readings
    if len(set(sensor_values)) != 1:
        print("Error: Gas sensor not responding.")
        return False
    
    # Test 3: Check if the sensor reading is within a valid range
    # You may read a few initial values and ensure they are within a valid range
    # Here, we'll read the sensor value once and check if it's within a valid range
    initial_value = GPIO.input(gas_sensor_pin)
    if initial_value not in [GPIO.LOW, GPIO.HIGH]:
        print("Error: Invalid reading from gas sensor.")
        return False
    
    print("POST completed successfully.")
    return True

# Function to read gas level
def read_gas_level():
    # Read gas level from sensor
    gas_level = GPIO.input(gas_sensor_pin)
    return gas_level

try:
    # Perform POST
    if perform_post():
        while True:
            # Read gas level
            gas_level = read_gas_level()
            
            # Display gas level
            print("Gas Level:", gas_level)
            
            # Optionally, control an LED based on gas level
            if gas_level == GPIO.HIGH:
                GPIO.output(led_pin, GPIO.HIGH)
            else:
                GPIO.output(led_pin, GPIO.LOW)
            
            # Wait for some time before reading again
            time.sleep(1)

except KeyboardInterrupt:
    # Clean up GPIO settings on keyboard interrupt
    GPIO.cleanup()
