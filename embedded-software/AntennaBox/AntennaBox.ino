#include <ArduinoLowPower.h>
#include <SigFox.h>



typedef struct __attribute__ ((packed)) sigfox_payload1 {
  uint8_t   payload_type;
  uint8_t   lat_sign;
  uint8_t   lon_sign;
  uint32_t  lat;
  uint32_t  lon;
  uint32_t  pressure;
}                                       SigfoxPayload1;

typedef struct __attribute__ ((packed)) sigfox_payload2 {
  uint8_t   payload_type;
  uint8_t   acc;
  uint16_t  ph;
  uint16_t  humidity;
  uint16_t  temperature;
  uint16_t  turbidity;
  uint16_t  conductivity;
}                                       SigfoxPayload2;


// stub for message which will be sent
SigfoxPayload1 msg1;
SigfoxPayload2 msg2;



void setup() 
{
  if (!SigFox.begin()) {
    // Something is really wrong, try rebooting
    Serial.println("Unable to init the Atmel ATA8520 Sigfox chipset");
    reboot();
  }

  //Send module to standby until we need to send a message
  SigFox.end();

  // Enable debug prints and LED indication
  SigFox.debug();
}


void loop() 
{
   // Start the module
  SigFox.begin();
  
  // Wait at least 30ms after first configuration (100ms before)
  delay(100);

  // Clears all pending interrupts
  SigFox.status();
  delay(1);

  // Send the first payload
  SigFox.beginPacket();
  SigFox.write((uint8_t*)&msg1, 12);
  SigFox.endPacket();

  // Send the second payload
  SigFox.beginPacket();
  SigFox.write((uint8_t*)&msg2, 12);
  SigFox.endPacket();
  
  // Sleep for 15 minutes
  LowPower.sleep(20 * 60 * 1000);
}


void reboot() 
{
  NVIC_SystemReset();
  while (1);
}
