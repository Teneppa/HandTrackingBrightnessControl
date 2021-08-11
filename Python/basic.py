"""This is an example from taken from
    https://google.github.io/mediapipe/solutions/hands#python-solution-api
    that is modified to act as an virtual slider that you can control with your hands.

    Requirements:
    - Webcam
    - Arduino
    """
import sys
import math
import cv2
import mediapipe as mp
from numpy.core.fromnumeric import var
import serial

# This is for mapping the hand position to an 8-bit value
from numpy import interp

# Hand tracking stuff
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands
drawing_styles = mp.solutions.drawing_styles

# This is used to detect the change between pinching
# and not pinching so that we can save the start position
PINCHING = False

# The starting position <Y> of the pinch
pinchStart = 0

# Difference in brightness
variable = 0

# The Arduino's serial port parameters
serialPort = "COM10"
baudrate = 115200

# Spare your eyes from this, but this will check if the port exists
# and tells you if it doesn't
try:
    s = serial.Serial(serialPort, baudrate)
except Exception as e:
    print("\n", e)
    print(f">No device found on {serialPort} probably")

    sys.exit(69)


def sup(val):
    """Send the new slider value to the Arduino and add a semicolon to the message

    Args:
        val ([str]): The new slider position
    """
    # Add semicolon after the value
    msg = str(val)+";"

    # Encode the message
    encodedMessage = msg.encode()

    # Send the encoded message
    s.write(encodedMessage)


# For webcam input:
cap = cv2.VideoCapture(1)

with mp_hands.Hands(
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5) as hands:
    while cap.isOpened():
        success, image = cap.read()
        if not success:
            print("Ignoring empty camera frame.")
            # If loading a video, use 'break' instead of 'continue'.
            continue

        # Flip the image horizontally for a later selfie-view display, and convert
        # the BGR image to RGB.
        image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
        
        # To improve performance, optionally mark the image as not writeable to
        # pass by reference.
        image.flags.writeable = False
        results = hands.process(image)

        # Draw the hand annotations on the image.
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(
                    image, hand_landmarks, mp_hands.HAND_CONNECTIONS,
                    drawing_styles.get_default_hand_landmark_style(),
                    drawing_styles.get_default_hand_connection_style())

            # Find the markers for the index finger and thumb, calculate the distance,
            # convert it to brightness and sent it to the Arduino
            try:
                listOfMarks = hand_landmarks.landmark

                # NOTE: https://google.github.io/mediapipe/solutions/hands#python-solution-api

                #p1 = THUMB_TIP
                #p2 = IDNEX_FINGER_TIP

                p1 = listOfMarks[4]
                p2 = listOfMarks[8]

                # Calculate the distance between the fingertips
                pinch = math.sqrt((p1.x-p2.x)**2+(p1.y-p2.y)**2+(p1.z-p2.z)**2)

                # If the fingertips are close enough, consider it as pinching your
                # fingers.
                if pinch < 0.1:

                    # If this is the first frame that the pinching was detected,
                    # save the avgerage Y position so we can compare how much we
                    # moved our hand up/down
                    if not PINCHING:
                        pinchStart = (p1.y+p2.y)/2
                    else:
                        # How much did the hand move
                        percentage = (pinchStart-(p1.y+p2.y)/2)*2

                        # We need to map the distance to brightness
                        minVal = -0.5
                        maxVal = minVal*-1

                        # Check that it doesn't go over the limits
                        if percentage > maxVal:
                            percentage = 1
                        if percentage < minVal:
                            percentage = -1

                        # Interpolate the percentage to 8-bit value so we can manipulate
                        # the brightness with this value
                        m = interp(percentage, [minVal, maxVal], [-255, 255])

                        # Add the new value to the previously saved and
                        # limit the brightness to the range of 0-255
                        brightness = m+variable
                        if brightness > 255:
                            brightness = 255
                        if brightness < 0:
                            brightness = 0

                        # Print stuff and send the brightness to the Arduino
                        print("CURRENT: ", (pinchStart-(p1.y+p2.y)/2)*10, "\tPERCENTAGE: ",
                              percentage, "\t VAL:", m, "\t VARIABLE: ", variable, "\t BRI: ", brightness)
                        sup(int(brightness))

                    PINCHING = True
                else:
                    if PINCHING:
                        variable += m

                        if variable > 255:
                            variable = 255
                        if variable < 0:
                            variable = 0

                        print(variable)

                    PINCHING = False
            except Exception as e:
                print(e)

        # Show the image
        cv2.imshow('MediaPipe Hands', image)

        # Press <Q> to exit
        if cv2.waitKey(1) & 0xFF == 113:
            break

cap.release()
