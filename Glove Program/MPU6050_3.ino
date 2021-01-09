// Arduino Wire library is required if I2Cdev I2CDEV_ARDUINO_WIRE implementation
// is used in I2Cdev.h
#include "Wire.h"
 
// I2Cdev and MPU6050 must be installed as libraries, or else the .cpp/.h files
// for both classes must be in the include path of your project
#include "I2Cdev.h"
#include "MPU6050.h"
 
// class default I2C address is 0x68
// specific I2C addresses may be passed as a parameter here
// AD0 low = 0x68 (default for InvenSense evaluation board)
// AD0 high = 0x69
MPU6050 accelgyro;
 
int16_t ax, ay, az;
int16_t gx, gy, gz;
 
#define BUTTON_PIN 7
#define LED 6
#define THUMB A0
#define INDEX A1
#define MIDDLE A2
#define RING A3
#define LITTLE A6

#define THUMB_THRESHOLD 450
#define INDEX_THRESHOLD 200
#define MIDDLE_THRESHOLD 200
#define RING_THRESHOLD 700
#define LITTLE_THRESHOLD -1

#define AX_THRESHOLD 28000
#define AY_THRESHOLD 28000
#define AZ_THRESHOLD 28000
#define GX_THRESHOLD 19000
#define GY_THRESHOLD 19000
#define GZ_THRESHOLD 19000

const int THRESHOLD[11] ={THUMB_THRESHOLD,INDEX_THRESHOLD,MIDDLE_THRESHOLD,
RING_THRESHOLD,LITTLE_THRESHOLD,AX_THRESHOLD,AY_THRESHOLD,AZ_THRESHOLD,
GX_THRESHOLD,GY_THRESHOLD,GX_THRESHOLD};

void pause(){
  bool flag=1;
  if(flag){
    digitalWrite(LED,HIGH);
    while(flag==1){
      flag=0;
      for(int i=0;i<15;i++){
        if(digitalRead(BUTTON_PIN)==1) flag=1;  
      }
    }
    while(flag==0){
      for(int i=0;i<15;i++){
        if(digitalRead(BUTTON_PIN)==1) flag=1;  
      }
    }
    while(flag==1){
      flag=0;
      for(int i=0;i<15;i++){
        if(digitalRead(BUTTON_PIN)==1) flag=1;  
      }
    }
    digitalWrite(LED,LOW);

    
  }
}
 
void setup() {
  // join I2C bus (I2Cdev library doesn't do this automatically)
  Wire.begin();
 
  // initialize serial communication
  Serial.begin(19200);
  // initialize device
  accelgyro.initialize();
  
  // configure Arduino LED for
  pinMode(BUTTON_PIN, INPUT);
  pinMode(LED,OUTPUT);

  pinMode(THUMB, INPUT);
  pinMode(INDEX, INPUT);
  pinMode(MIDDLE, INPUT);
  pinMode(RING, INPUT);
  pinMode(LITTLE, INPUT);
  //Serial.println("O");
  delay(2000);
  //Serial.println("K");
}


int caliCount = 70;

void exec()
{
  //5 finger + 6 acceleration
  long long valSum[11] = {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0};
  //int16_t val[6] = {0, 0, 0, 0, 0, 0};
  int calibData[11] = {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0};
  bool button_flag = false;
  //get sum
  unsigned long time1 = millis();
  for (int i = 0; i < caliCount; ++i) {
    accelgyro.getMotion6(&ax, &ay, &az, &gx, &gy, &gz);
    valSum[0] += analogRead(THUMB);
    valSum[1] += analogRead(INDEX);
    valSum[2] += analogRead(MIDDLE);
    valSum[3] += analogRead(RING);
    valSum[4] += analogRead(LITTLE);

    valSum[5] += ax;
    valSum[6] += ay;
    valSum[7] += az;
    valSum[8] += gx;
    valSum[9] += gy;
    valSum[10] += gz;
    
    if(digitalRead(BUTTON_PIN)){
      button_flag = true;
    }
    delay(2);
  }
   if(button_flag) {
    pause();
    return;
  }

  //mean
  for (int i = 0; i < 11; ++i) {
    calibData[i] += int(valSum[i] / caliCount);
    if(digitalRead(BUTTON_PIN)){
      button_flag = true;
    }
  }

  char output[11];
  
  for (int i = 0; i < 5; ++i) {
    if(calibData[i] > THRESHOLD[i]) output[i] = '0';
    else output[i] = '1';

  }
  //Serial.print(" ");
  for (int i = 5; i < 11; ++i) {
    if(calibData[i] > THRESHOLD[i]) output[i] = '1';
    else if(calibData[i] < -THRESHOLD[i]) output[i] = '2';
    else output[i] = '0';
    //Serial.print(" ");
  }
  //Serial.print(" "+calibData[5]);
  bool outputflag=false;
  for(int i=0;i<11;++i)
  {
    if(output[i]!='0')outputflag=true;
  }
  if(outputflag)
  {
    for(int i=0;i<11;++i)
    {
      Serial.print(output[i]);
    }
    Serial.println("");
  }
  else{
    return;
  }
  while(millis()-time1<500){
    if(digitalRead(BUTTON_PIN)){
      pause();
      return;
    }
  }
  
//  unsigned long time1 = millis();


 
}

void loop() {
  //5 finger + 6 acceleration
  exec();

}
