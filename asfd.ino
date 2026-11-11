#include <Servo.h>

Servo servo1;
Servo servo2;
Servo servo3;
Servo servo4;

void setup() {
  Serial.begin(9600);

  servo1.attach(11);
  servo2.attach(10);
  servo3.attach(9);
  servo4.attach(6);
}

void loop() {
  if (Serial.available() > 0) {
    char servoId = Serial.read(); // Leia o identificador do servo

    int pos = Serial.parseInt(); // Leia a posição desejada

    switch (servoId) {
      case '1':
        servo1.write(pos); // Mova o servo1 para a posição desejada
        break;
      case '2':
        servo2.write(pos); // Mova o servo2 para a posição desejada
        break;
      case '3':
        servo3.write(pos); // Mova o servo3 para a posição desejada
        break;
      case '4':
        servo4.write(pos); // Mova o servo4 para a posição desejada
        break;
    }
  }
}
