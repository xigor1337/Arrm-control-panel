#include <Servo.h>

Servo servos[6];
int initial_positions[] = {90, 90, 90, 90, 90, 70};
int speed = 10;

void setup() {
  Serial.begin(9600);
  
  for (int i = 0; i < 6; i++) {
    servos[i].attach(2 + i);
    servos[i].write(initial_positions[i]);
  }
}

void loop() {
  if (Serial.available() > 0) {
    String input = Serial.readStringUntil('\n');
    processInput(input);
  }
}

void processInput(String input) {
  int new_positions[6];
  int previous_positions[6];
  
  for (int i = 0; i < 6; i++) {
    int commaIndex = input.indexOf(',');
    int semicolonIndex = input.indexOf(';');
    
    String prevValue = input.substring(0, commaIndex);
    String newValue = input.substring(commaIndex + 1, semicolonIndex != -1 ? semicolonIndex : input.length());
    
    previous_positions[i] = prevValue.toInt();
    new_positions[i] = newValue.toInt();
    
    if (semicolonIndex != -1) {
      input = input.substring(semicolonIndex + 1);
    }
  }
  
  for (int i = 0; i < 6; i++) {
    moveServo(servos[i], previous_positions[i], new_positions[i]);
  }
}

void moveServo(Servo &servo, int start, int end) {
  if (start < end) {
    for (int i = start; i <= end; i++) {
      servo.write(i);
      delay(speed);
    }
  } else {
    for (int i = start; i >= end; i--) {
      servo.write(i);
      delay(speed);
    }
  }
}
