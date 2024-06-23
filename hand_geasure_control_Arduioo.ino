#include <Servo.h>

#define NO_OF_VAL_REC 5        // Number of values to receive
#define DIGIT_PER_VAL_REC 1    // Number of digits per value

Servo thumbServo;             // Servo objects
Servo indexServo;
Servo middleServo;
Servo ringServo;
Servo pinkyServo;

int valsRec[NO_OF_VAL_REC];   // Array to store received values
int stringLength = NO_OF_VAL_REC * DIGIT_PER_VAL_REC + 1;  // Length of received string
int counter = 0;               // Counter to track received characters
bool counterStart = false;     // Flag to indicate start of receiving
String receivedString;         // String to store received characters

void setup() {
  Serial.begin(9600);  // Initialize serial communication
  // Attach servos to pins
  thumbServo.attach(11));
  indexServo.attach(9);
  middleServo.attach(5);
  ringServo.attach(3);
  pinkyServo.attach(6);
}

void loop() {
  receiveData();   // Function to receive data from serial
  controlServos(); // Function to control servos based on received values
}

void controlServos() {
  // Control each servo based on received values
  // If the value is 1, set servo angle to 0, else set it to 60
  if (valsRec[0] == 1) {
    thumbServo.write(0);
  } else {
    thumbServo.write(60);
  }

  // If the value is 1, set servo angle to 0, else set it to 140
  if (valsRec[1] == 1) {
    indexServo.write(0);
  } else {
    indexServo.write(140);
  }

  // If the value is 1, set servo angle to 140, else set it to 0
  if (valsRec[2] == 1) {
    middleServo.write(140);
  } else {
    middleServo.write(0);
  }

  // If the value is 1, set servo angle to 90, else set it to 0
  if (valsRec[3] == 1) {
    ringServo.write(90);
  } else {
    ringServo.write(0);
  }

  // If the value is 1, set servo angle to 0, else set it to 160
  if (valsRec[4] == 1) {
    pinkyServo.write(0);
  } else {
    pinkyServo.write(160);
  }
}

void receiveData() {
  while (Serial.available()) {
    char c = Serial.read();   // Read character from serial buffer
    if (c == '$') {
      counterStart = true;    // Set flag to indicate start of receiving
    }
    if (counterStart) {
      if (counter < stringLength) {
        receivedString = String(receivedString + c);  // Accumulate characters into receivedString
        counter++;    // Increment counter
      }
      if (counter >= stringLength) {
        for (int i = 0; i < NO_OF_VAL_REC; i++) {
          int num = (i * DIGIT_PER_VAL_REC) + 1;   // Calculate starting position of each value
          valsRec[i] = receivedString.substring(num, num + DIGIT_PER_VAL_REC).toInt();  // Parse substring to integer and store in valsRec array
        }
        receivedString = "";   // Reset receivedString
        counter = 0;           // Reset counter
        counterStart = false;  // Reset flag
      }
    }
  }
}
