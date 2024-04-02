#pip install gpiozero pigpio


from gpiozero import MCP3008, Device
from gpiozero.pins.pigpio import PiGPIOFactory
import time

# Use pigpio for hardware SPI
Device.pin_factory = PiGPIOFactory()

# Assuming AO-03 is connected to channel 0 of the MCP3008
ao03_channel = MCP3008(channel=0)

def perform_post():
    """Perform the Power-On Self-Test for AO-03 module"""
    # Directly reading the analog value, no digitalRead equivalent
    # Note: MCP3008 value is normalized (0 to 1), so adjust thresholds accordingly
    analog_value = ao03_channel.value
    if analog_value < 0.1 or analog_value > 0.9:  # Adjust thresholds as needed
        print("POST failed: Unexpected analog output from AO-03 module.")
        return False

    # All tests passed
    print("POST successful. AO-03 module is functioning.")
    return True

def map_value(value, in_min, in_max, out_min, out_max):
    """Map value from one range to another"""
    return (value - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

def measure_o2_concentration():
    """Read analog value from AO-03 module and convert it to O2 concentration"""
    # MCP3008 returns a normalized value (0 to 1), map this back to 0-1023 for Arduino-like behavior
    analog_value = ao03_channel.value * 1023
    oxygen_concentration = map_value(analog_value, 0, 1023, 0, 100)  # Example mapping
    return oxygen_concentration

if __name__ == "__main__":
    print("Initializing...")

    # Perform Power-On Self-Test
    if perform_post():
        # If all tests passed, output O2 concentration
        while True:  # Continuous reading; remove or modify for your application
            oxygen_concentration = measure_o2_concentration()
            print(f"O2 Concentration: {oxygen_concentration:.2f} %")
            time.sleep(1)  # Delay between readings
    else:
        print("POST failed. AO-03 module is not functioning.")


#This script uses gpiozero's MCP3008 class to read from the ADC and pigpio as the backend for better performance, especially necessary for precise timing and SPI communication on the Raspberry Pi. Adjust the thresholds in perform_post according to the specifics of your AO-03 module and the environment in which you're working.
