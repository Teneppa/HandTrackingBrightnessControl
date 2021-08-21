# HandTrackingBrightnessControl
A hand tracking demo made with mediapipe where you can control lights with pinching your fingers and moving your hand up/down.

### Programs:
* Python3 - basic.py
* Arduino - 1_DisplayLight_SerialBrightness.ino - Neopixel demo
* Arduino - 1_SerialBrightness_PWM.ino - Regular LED demo

### Requirements:
#### Python packages:
* Mediapipe (pip3 install mediapipe)
* CV2 (pip3 install opencv-python)
* pySerial (pip3 install pyserial)
* numpy (pip3 install numpy)

#### Hardware:
* Webcam
* Arduino
* Neopixel LED-strip (unless you modify the code)

#### Pinout (Neopixel):
| Arduino pin   | Where you connect it |
| ------------- | ------------- |
| D2  | LED Strip Din |
| 5V | +5V |
| GND | GND |

#### Pinout (Regular LED WITH A RESISTOR!):
| Arduino pin   | Where you connect it |
| ------------- | ------------- |
| D3  | +LED |
| GND | -LED |
