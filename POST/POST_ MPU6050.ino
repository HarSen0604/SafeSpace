#include <Wire.h>
#include <MPU6050.h>

MPU6050 mpu;

void setup() {
  Serial.begin(9600);
  
  // Initialize MPU6050
  Wire.begin();
  mpu.initialize();

  // Check if MPU6050 connection is successful
  if (!mpu.testConnection()) {
    Serial.println("MPU6050 connection failed!");
    while (1); // Loop indefinitely if connection fails
  }

  Serial.println("MPU6050 connection successful!");

  // Perform self test (optional)
  // Note: MPU6050 does not provide a built-in self-test function
  // You can manually check sensor values if needed
}

void loop() {
  // Read accelerometer and gyroscope data
  int16_t ax, ay, az;
  int16_t gx, gy, gz;
  
  mpu.getMotion6(&ax, &ay, &az, &gx, &gy, &gz);

  // Print accelerometer and gyroscope data
  Serial.print("Accelerometer: ");
  Serial.print("x=");
  Serial.print(ax);
  Serial.print(" y=");
  Serial.print(ay);
  Serial.print(" z=");
  Serial.println(az);

  Serial.print("Gyroscope: ");
  Serial.print("x=");
  Serial.print(gx);
  Serial.print(" y=");
  Serial.print(gy);
  Serial.print(" z=");
  Serial.println(gz);

  delay(1000); // Delay for 1 second
}
