// HC05_POST_Code.ino
#include <SoftwareSerial.h> // Include the SoftwareSerial library for serial communication with HC-05

// Define HC-05 module pins
#define HC05_TX 10 // HC-05 TX pin
#define HC05_RX 11 // HC-05 RX pin

SoftwareSerial hc05(HC05_TX, HC05_RX); // Create a software serial port for communication with HC-05

/**
 * @brief Function to perform Power-On Self-Test (POST) for HC-05 module
 * @return True if POST passed, False otherwise
 */
bool postHC05() {
  // Send AT command to check if HC-05 module is responding
  hc05.println("AT");
  
  // Wait for response from HC-05
  delay(500);
  
  // Check if HC-05 responded with "OK"
  if (hc05.find("OK")) {
    return true; // Return true if HC-05 responded correctly
  } else {
    return false; // Return false if HC-05 did not respond correctly
  }
}

void setup() {
  Serial.begin(9600); // Initialize serial communication for debugging purposes
  hc05.begin(9600); // Initialize serial communication with HC-05 module

  // Wait for HC-05 module to initialize
  delay(1000);
  
  // Perform Power-On Self-Test (POST)
  if (postHC05()) {
    Serial.println("HC-05 Power-On Self-Test passed."); // Print success message if POST passed
  } else {
    Serial.println("HC-05 Power-On Self-Test failed. Check wiring and module."); // Print error message if POST failed
  }
}

void loop() {
  // Nothing to do in the loop for this example
}
