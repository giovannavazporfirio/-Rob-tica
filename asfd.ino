#include <Servo.h>

Servo servo1;
Servo servo2;
Servo servo3;
Servo servo4;

int pos1 = 0;
int pos2 = 90;
int pos3 = 90;
int pos4 = 90;

void moverServo(Servo &servo, int &posAtual, int posDesejada) {
  if (posDesejada > posAtual) {
    for (int i = posAtual; i <= posDesejada; i++) {
      servo.write(i);
      delay(15);
    }
  } 
  else {
    for (int i = posAtual; i >= posDesejada; i--) {
      servo.write(i);
      delay(15);
    }
  }

  posAtual = posDesejada;
}

void setup() {
  Serial.begin(9600);

  servo1.attach(2);
  servo2.attach(3);
  servo3.attach(7);
  servo4.attach(6);

  servo1.write(pos1);
  servo2.write(pos2);
  servo3.write(pos3);
  servo4.write(pos4);
}

void loop() {
  if (Serial.available() > 0) {
    char servoId = Serial.read();

    int pos = Serial.parseInt();

    pos = constrain(pos, 0, 180);

    switch (servoId) {
      case '1':
        moverServo(servo1, pos1, pos);
        break;

      case '2':
        moverServo(servo2, pos2, pos);
        break;

      case '3':
        moverServo(servo3, pos3, pos);
        break;

      case '4':
        moverServo(servo4, pos4, pos);
        break;
    }
  }
}
