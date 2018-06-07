#include <Arduino.h>
#include <Finger.h>
#include <DRV8833.h>

Finger::Finger(int encoderPinA, int encoderPinB,int in1, int in2,int max) {
    pinMode(encoderPinA, INPUT);
    digitalWrite(encoderPinA, HIGH);
    pinMode(encoderPinB, INPUT);
    digitalWrite(encoderPinB, HIGH);
    pinMode(in1, OUTPUT);
    pinMode(in2, OUTPUT);
    _max = max;
    _in1 = in1;
    _in2 = in2;
    driver.attachMotorA(in1,in2);
    _encoderPinA = encoderPinA;
    _encoderPinB = encoderPinB;
}

void Finger::readEncoder() {
    _current = encoderCount;
    int a = digitalRead(Finger::_encoderPinA);
    int b = digitalRead(Finger::_encoderPinB);
    if (a == HIGH) {
        if (b == LOW) {
            encoderCount = encoderCount + 1;
        }
        else {
            encoderCount = encoderCount - 1;
        }
    }
    else {
        if (b == HIGH) {
            encoderCount = encoderCount + 1;
        }
        else {
            encoderCount = encoderCount - 1;
        }
    }
    if(_current != encoderCount){
        currentMillis = millis();
    }
 
}



        
void Finger::move() {
    if(stop-t < encoderCount && stop+t > encoderCount){
        driver.motorAStop();
        currentMillis = millis();
    }
    else if(stop < encoderCount){

      //  
      driver.motorAReverse();
        // if(millis() - currentMillis > 500){
        //     encoderCount = _max;
        //     stop = _max;
        // }

    }
    else if(stop > encoderCount){
      // _current = encoderCount;
      driver.motorAForward();
        if(millis() - currentMillis > 500){
            encoderCount = _max;
            stop = encoderCount;
        }
    }

}

int Finger::getPos() {
    return encoderCount;
}
void Finger::setPos(int pos){
    if (pos < 0 )
        stop = 0;
    else
        stop  = pos;
    // stop = (pos < max ) ? pos : max;
}