#include <Adafruit_NeoPixel.h>

#define LED_PIN   2
#define LED_COUNT 19

Adafruit_NeoPixel strip(LED_COUNT, LED_PIN, NEO_GRB + NEO_KHZ800);

void setup() {
  Serial.begin(115200);
  strip.begin();
}

void colorWipe(uint32_t color, int wait) {
  for (int i = 0; i < strip.numPixels(); i++) { // For each pixel in strip...
    strip.setPixelColor(i, color);         //  Set pixel's color (in RAM)
    strip.show();                          //  Update strip to match
    delay(wait);                           //  Pause for a moment
  }
}

void fill(uint32_t color) {
  for (int i = 0; i < strip.numPixels(); i++) {
    strip.setPixelColor(i, color);
  }
  strip.show();
}

uint8_t brightness = 255;

void loop() {
  while (Serial.available() > 0) {
    String msg = Serial.readStringUntil(';');
    Serial.flush();

    brightness = msg.toInt();
  }

  strip.setBrightness(brightness);
  fill(strip.Color(255,130,0));
}
