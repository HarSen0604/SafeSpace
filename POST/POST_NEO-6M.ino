#include <SoftwareSerial.h> // Include the SoftwareSerial library for serial communication

// Define the pins for serial communication with the NEO-6M module
#define NEO_6M_RX_PIN 2 // Connect NEO-6M TX pin to Arduino digital pin 2
#define NEO_6M_TX_PIN 3 // Connect NEO-6M RX pin to Arduino digital pin 3

SoftwareSerial neoSerial(NEO_6M_RX_PIN, NEO_6M_TX_PIN); // Create a SoftwareSerial object

void setup() {
  Serial.begin(9600); // Initialize serial communication with the computer
  neoSerial.begin(9600); // Initialize serial communication with the NEO-6M module
  delay(1000); // Wait for the NEO-6M module to initialize
  performPOST(); // Perform Power-On Self Test
}

void loop() {
  // Nothing to do here in this example
}

void performPOST() {
  // Print a message indicating the start of the POST
  Serial.println("Starting Power-On Self Test (POST) for NEO-6M GPS module...");

  // Check if NEO-6M module is responding
  neoSerial.println("$PMTK000*32");
  delay(100); // Wait for response
  if (neoSerial.find("$PMTK001,0,3,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0")) {
    // NEO-6M module is responding correctly
    Serial.println("NEO-6M GPS module is responding.");
    Serial.println("Power-On Self Test (POST) passed.");
  } else {
    // NEO-6M module is not responding correctly
    Serial.println("NEO-6M GPS module is not responding.");
    Serial.println("Power-On Self Test (POST) failed.");
  }
}
