#include <Servo.h>

Servo servo1;
Servo servo2;
Servo servo3;
Servo servo4;

void setup() {
  Serial.begin(9600);

  servo1.attach(2); //funciona
  servo2.attach(3); //funciona
  servo3.attach(4); //funciona 
  servo4.attach(6);

  servo1.write(0);
  servo2.write(90);
  servo3.write(90);
  servo4.write(90);

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
