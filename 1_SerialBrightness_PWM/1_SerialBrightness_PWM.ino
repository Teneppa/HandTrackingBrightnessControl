// Connect the LED to this pin
uint8_t ledPin = 3;

void setup() {
  // Set the LED as an output
  pinMode(ledPin, OUTPUT);

  // Open up the serial port so we can communicate
  // with the Python script
  Serial.begin(115200);
}

// This stores the brightness (it's not really needed
// but yea here it is)
uint8_t brightness = 255;

void loop() {
  // If there's a new message
  while (Serial.available() > 0) {

    // Read the message and remove the semicolon from the end
    String msg = Serial.readStringUntil(';');

    // Clear the serial buffer just in case we can't read it fast enough
    Serial.flush();

    // Convert the message to a number
    brightness = msg.toInt();
  }

  // Change the LED's brightness
  analogWrite(ledPin, brightness);
}
