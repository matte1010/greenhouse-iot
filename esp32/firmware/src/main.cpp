#include <Arduino.h>

// put function declarations here:
int myFunction(int, int);

void setup() {
  Serial.begin(115200);
  delay(1000);
  Serial.println("ESP32 PlatformIO setup works!");
}

void loop() {
  Serial.println("Running...");
  delay(2000);
}

// put function definitions here:
int myFunction(int x, int y) {
  return x + y;
}