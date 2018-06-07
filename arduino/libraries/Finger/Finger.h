#ifndef Finger_h
#define Finger_h
#include <Arduino.h>
#include <DRV8833.h>
class Finger {
    public:
        Finger(int phase, int enable, int encoderPinA, int encoderPinB, int max);
        void readEncoder();
        void move();
        int getPos();
        void setPos(int pos);
        int _encoderPinA, _encoderPinB, _in1, _in2,_max;
        DRV8833 driver = DRV8833();
    private:
        volatile int encoderCount = 0;
        volatile int stop = 0;
        volatile int _current=9999999;
        unsigned long currentMillis;
        int t = 5;
};

#endif
