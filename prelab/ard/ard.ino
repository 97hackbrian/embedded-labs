#include <Servo.h>
#define ledPin 9
#define relayPin 5      
#define servoPin 2
Servo servoMotor;

#define pwma 6
#define ain2 7
#define ain1 8
void setup() {
  Serial.begin(9600);
  pinMode(ledPin,OUTPUT);
  pinMode(relayPin,OUTPUT);
  pinMode(pwma,OUTPUT);
  pinMode(ain1,OUTPUT);
  pinMode(ain2,OUTPUT);
  pinMode(servoPin,OUTPUT);
  servoMotor.attach(servoPin);
  servoMotor.write(-90);
  digitalWrite(relayPin, HIGH);
}

void loop() {
  while (Serial.available() > 0) {
    char command = Serial.read();
    
    if (command == '1') {
      for(int x=0;x<=10;x++){    
        digitalWrite(ledPin, HIGH);
        delay(100);
        digitalWrite(ledPin, LOW);
        delay(100);
      }
    }
    else{
      digitalWrite(ledPin, LOW);
    }

    if (command == '2') {
      digitalWrite(ain1,HIGH);
      digitalWrite(ain2,LOW);
      analogWrite(pwma,120);
      delay(3000);
      digitalWrite(ain1,LOW);
      digitalWrite(ain2,LOW);
      analogWrite(pwma,0);
    }
    else{
      digitalWrite(ain1,LOW);
      digitalWrite(ain2,LOW);
      analogWrite(pwma,0);
    }


    if (command == '3') {
      for(int x=0;x<=10;x++){    
        digitalWrite(relayPin, HIGH);
        delay(100);
        digitalWrite(relayPin, LOW);
        delay(100);
      }
    }
    else{
      digitalWrite(relayPin, HIGH);
    }



    if (command == '4') {
      servoMotor.write(-90);
      for(int x=-90;x<=90;x++){    
        servoMotor.write(x);
        delay(5);
      }
      for(int x=90;x>=-90;x--){    
        servoMotor.write(x);
        delay(5);
      }
    }
    else{
      servoMotor.write(-90);
    }
}
}
