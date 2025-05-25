#include <IRremote.hpp> // include the library
#define IR_RECEIVE_PIN A0

#define DECODE_MAGIQUEST


// The magiquest payload is a bit different from the
// standard IRremote payload
union magiquest {
  uint64_t llword;
  uint8_t byte[8];
  uint32_t lword[2];
  struct {
    uint16_t magnitude;
    uint32_t wand_id;
    uint8_t padding;
    uint8_t scrap;
  } cmd ;
};


void setup() {
  Serial.begin(9600);
  while (!Serial) {
    ;
  }

  Serial.println("Comms enabled - beginning sensing");

  // turn on IR receiver
  IrReceiver.begin(IR_RECEIVE_PIN, ENABLE_LED_FEEDBACK);
}

void loop() {
  // Wait and decode
  if (IrReceiver.decode()) {
    // translate the bit stream into something we can use
    // to understand a MagiQuest wand
    // IrReceiver.printIRResultShort(&Serial);
    // IrReceiver.printIRSendUsage(&Serial);
    // decodeMagiQuest(&results, &data);
    // if (IrReceiver.decodedIRData.address == 56705) {
    //   Serial.println("HELLO CAMILLA");
    // }
    // if (IrReceiver.decodedIRData.address == 60929) {
    //   Serial.println("HELLO JULIET");
    // }

    String protocol = IrReceiver.getProtocolString();
    uint16_t address = IrReceiver.decodedIRData.address;
    uint16_t extra = IrReceiver.decodedIRData.extra;
    uint16_t command = IrReceiver.decodedIRData.command;
    unsigned long value = IrReceiver.decodedIRData.decodedRawData;

    // Send the data in JSON-like string
    Serial.print("{\"protocol\":\"");
    Serial.print(protocol);
    Serial.print("\",\"address\":");
    Serial.println(address);
    Serial.print(",\"extra\":");
    Serial.println(extra);
    Serial.print(",\"command\":");
    Serial.println(command);
    Serial.println("}");

    // keep receiving data 
    IrReceiver.resume();
  }

  // wait a bit, and then back to receiving and decoding
  delay(100);
}
