
#include <ros.h>
#include <ros/time.h>
#include <sensor_msgs/Range.h>
#include <Wire.h>
#include <VL53L0X.h>

//#define XSHUT_pin6 not required for address change

#define XSHUT_pin2 4
#define XSHUT_pin1 5

//ADDRESS_DEFAULT 0b0101001 or 41
//#define Sensor1_newAddress 41 not required address change
#define Sensor2_newAddress 42


VL53L0X Sensor1;
VL53L0X Sensor2;

ros::NodeHandle  nh;


sensor_msgs::Range range_msg;
ros::Publisher pub_range( "range_data", &range_msg);
char frameid[] = "/tof_ranger";
unsigned long range_timer;

void setup()
{ /*WARNING*/
  //Shutdown pins of VL53L0X ACTIVE-LOW-ONLY NO TOLERANT TO 5V will fry them
  pinMode(XSHUT_pin1, OUTPUT);
  pinMode(XSHUT_pin2, OUTPUT);

  
  Serial.begin(9600);
  
  Wire.begin();

  pinMode(XSHUT_pin2, INPUT);
  delay(10);
  Sensor2.setAddress(Sensor2_newAddress);
  pinMode(XSHUT_pin1, INPUT);
  delay(10);
  
  Sensor1.init();
  Sensor2.init();

  
  Sensor1.setTimeout(500);
  Sensor2.setTimeout(500);


  // Start continuous back-to-back mode (take readings as
  // fast as possible).  To use continuous timed mode
  // instead, provide a desired inter-measurement period in
  // ms (e.g. sensor.startContinuous(100)).
  Sensor1.startContinuous();
  Sensor2.startContinuous();

  nh.initNode();
  nh.advertise(pub_range);
  
  range_msg.radiation_type = sensor_msgs::Range::INFRARED;
  range_msg.field_of_view = 0.01;
  range_msg.min_range = 57;
  range_msg.max_range = 8190;
}

void loop()
{
  Serial.print(Sensor1.readRangeContinuousMillimeters());
  Serial.print(',');
  Serial.print(Sensor2.readRangeContinuousMillimeters());
  Serial.println();
  if ( (millis()-range_timer) > 50){
    range_msg.header.frame_id =  "Sensor1";
    range_msg.range=Sensor1.readRangeContinuousMillimeters();
    range_msg.header.stamp = nh.now();
    pub_range.publish(&range_msg);
    range_msg.header.frame_id =  "Sensor2";
    range_msg.range=Sensor2.readRangeContinuousMillimeters();
    pub_range.publish(&range_msg);

    range_timer =  millis() + 50;
  }
  nh.spinOnce();
}
