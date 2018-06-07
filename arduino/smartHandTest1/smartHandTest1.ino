/*
 * DRV8833_Test
 * Simple test for the DRV8833 library.
 * The DRV8833 is a dual motor driver carrier made by Pololu.
 * You can find it here: https://www.pololu.com/product/2130
 *
 * Attach the positive wire of a motor to the Aout1 and the negative
 * wire to the Aout2 pins on the DRV8833.
 * Attach the Arduino's ground to the one of the GND pins on the DRV8833.
 * Attach a 9V battery's positive connection to the Vin pin
 * on the DRV8833, and the negative connection to one of the GND pins.
 * 
 * Created March 16, 2015, by Aleksandr J. Spackman.
 */

#include <Finger.h>
#include <Servo.h>

// Create an instance of the DRV8833:
Finger Pinky(2,5,8,9,1000);
Finger Ring(3,4,10,11,1000);
Finger Midle(17,18,6,7,1000);
Finger Indx(16,19,14,15,1000);
Finger Thumb(20,21,22,23,1800);

Servo Abs;
void setup() {
  // put your setup code here, to run once:
  
  // Start the serial port:
  Abs.attach(12);
  Serial.begin(9600);
  
  // Wait for the serial port to connect. Needed for Leonardo.
  while (!Serial);
  attachInterrupt(digitalPinToInterrupt(2),readPinky,CHANGE);
  attachInterrupt(digitalPinToInterrupt(3),readRing,CHANGE);
  attachInterrupt(digitalPinToInterrupt(18),readMidle,CHANGE);
  attachInterrupt(digitalPinToInterrupt(19),readIndx,CHANGE);
  attachInterrupt(digitalPinToInterrupt(20),readThumb,CHANGE);
  // Attach a motor to the input pins:
 
}
void readThumb(){
Thumb.readEncoder();
}
void readPinky(){
Pinky.readEncoder();
}
void readMidle(){
Midle.readEncoder();
}
void readIndx(){
Indx.readEncoder();
}
void readRing(){
Ring.readEncoder();
}

int absVal =0;
void loop() {
  
    Abs.write(55); 
  if(Serial.available()){
    String value = "";
    String label = "";
    bool isLabel = true;
    while(Serial.available()){
      char c= (char)Serial.read();
      if(c =='=')
        isLabel = false;
      else if(isLabel)
        label+=c;
      else
        value+=c;
      delay(5);
    }
    if(label=="thumb"){
      Thumb.setPos(value.toInt());
    }
    else if(label=="pinky"){
      Pinky.setPos(value.toInt());
    }
    else if(label=="ring"){
      Ring.setPos(value.toInt());
    }
    else if(label=="indx"){
      Indx.setPos(value.toInt());
    }
    else if(label=="midle"){
      Midle.setPos(value.toInt());
    }
  }
  Thumb.move();
  Serial.println(Thumb.getPos());
  Midle.move();
  Pinky.move();
  Ring.move();
  Indx.move();
//  
//  Pinky.setPos(1300);
//  delayPos(500);
//  Ring.setPos(1500);
//  delayPos(500);
//  Midle.setPos(1500);
//  delayPos(500);
//  Indx.setPos(1300);
//  delayPos(500);
//  Thumb.setPos(1000);
//  Abs.write(120);
//  delayPos(500);
//  Thumb.setPos(0);
//  Abs.write(55);
//  delayPos(500);
//  Indx.setPos(0);
//  delayPos(500);
//  Midle.setPos(0);
//  delayPos(500);
//  Ring.setPos(0);
//  delayPos(500);
//  Pinky.setPos(0);
//  delayPos(500);

}
void delayPos(int mil){
  for(int i=0;i<mil;i++){
    Thumb.move();
    Midle.move();
    Pinky.move();
    Ring.move();
    Indx.move();
    delay(1);
  }
  
}
void loop2(){
  Thumb.setPos(1000);
  delay(1000);
  Thumb.setPos(0);
}

