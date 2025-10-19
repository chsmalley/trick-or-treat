#include <IRremote.hpp> // include the library
// #include <IRremote.h>

#define DECODE_MAGIQUEST

const int irPins[4] = {2, 3, 4, 5};
IRrecv* irReceivers[4];
decode_results results;

void setup() {
  Serial.begin(9600);

  for (int i = 0; i < 4; i++) {
    irReceivers[i] = new IRrecv(irPins[i]);
    irReceivers[i]->enableIRIn();  // Start the receiver
    // turn on IR receiver
    IrReceiver.begin(IR_RECEIVE_PIN, ENABLE_LED_FEEDBACK);
  }
}

void loop() {
  for (int i = 0; i < 4; i++) {
    if (irReceivers[i]->decode()) {
      Serial.println(i);  // Send which receiver got the signal
      irReceivers[i]->resume();  // Receive the next signal
      delay(200);  // Debounce to avoid multiple triggers
    }
  }
}


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
