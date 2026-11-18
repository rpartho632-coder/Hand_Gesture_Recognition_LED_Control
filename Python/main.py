
import cv2
import mediapipe as mp
import serial
import time

# =========================
# CONFIGURATION
# =========================

SERIAL_PORT = "COM10"
BAUD_RATE = 9600
CAMERA_INDEX = 0

arduino = None
camera = None
hands = None

previous_data = ""

names = ["Thumb", "Index", "Middle", "Ring", "Little"]


def detect_fingers(hand, handedness):

    lm = hand.landmark

    # Thumb
    if handedness == "Right":
        thumb = int(lm[4].x < lm[3].x)
    else:
        thumb = int(lm[4].x > lm[3].x)

    # Four fingers
    index = int(lm[8].y < lm[6].y)
    middle = int(lm[12].y < lm[10].y)
    ring = int(lm[16].y < lm[14].y)
    little = int(lm[20].y < lm[18].y)

    return [thumb, index, middle, ring, little]


try:

    # =========================
    # SERIAL CONNECTION
    # =========================

    print("Connecting Arduino...")

    arduino = serial.Serial(
        SERIAL_PORT,
        BAUD_RATE,
        timeout=0.1,
        write_timeout=1
    )

    time.sleep(2)
    arduino.reset_input_buffer()

    print("Arduino Connected!")

    # =========================
    # MEDIAPIPE
    # =========================

    mp_hands = mp.solutions.hands
    mp_draw = mp.solutions.drawing_utils

    hands = mp_hands.Hands(
        static_image_mode=False,
        max_num_hands=1,
        model_complexity=0,
        min_detection_confidence=0.6,
        min_tracking_confidence=0.6
    )

    # =========================
    # CAMERA
    # =========================

    camera = cv2.VideoCapture(
        CAMERA_INDEX,
        cv2.CAP_DSHOW
    )

    camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    camera.set(cv2.CAP_PROP_BUFFERSIZE, 1)

    if not camera.isOpened():
        raise RuntimeError("Camera not found!")

    print("Camera Started!")
    print("Press Q in camera window to exit.")

    # =========================
    # MAIN LOOP
    # =========================

    while True:

        success, frame = camera.read()

        if not success:
            print("Camera frame error!")
            break

        frame = cv2.flip(frame, 1)

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        rgb.flags.writeable = False

        result = hands.process(rgb)

        rgb.flags.writeable = True

        # ======================================
        # UPDATED: Keep previous LED data
        # when hand is not detected
        # ======================================

        if result.multi_hand_landmarks:

            hand = result.multi_hand_landmarks[0]

            handedness = result.multi_handedness[0]
            label = handedness.classification[0].label

            mp_draw.draw_landmarks(
                frame,
                hand,
                mp_hands.HAND_CONNECTIONS
            )

            # Detect current finger positions
            fingers = detect_fingers(hand, label)

            # Convert finger states to serial data
            data = "".join(map(str, fingers))

            # Send only when hand gesture changes
            if data != previous_data:

                arduino.write(
                    (data + "\n").encode("ascii")
                )

                previous_data = data

                print("Data Sent:", data)

        else:

            # UPDATED:
            # Do NOT send 00000 when hand disappears.
            # Arduino will keep the previous LED state.

            cv2.putText(
                frame,
                "HAND NOT DETECTED - HOLDING LAST STATE",
                (10, 25),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.45,
                (0, 255, 255),
                2
            )

        # ======================================
        # DISPLAY LAST KNOWN FINGER STATE
        # ======================================

        if previous_data:

            fingers = [int(value) for value in previous_data]

        else:

            fingers = [0, 0, 0, 0, 0]

        open_count = sum(fingers)
        close_count = 5 - open_count

        status = "ON" if open_count > 0 else "OFF"

        cv2.putText(
            frame,
            f"LED: {status}",
            (10, 55),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.55,
            (0, 255, 0),
            2
        )

        cv2.putText(
            frame,
            f"OPEN: {open_count} CLOSE: {close_count}",
            (10, 80),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            (255, 255, 0),
            2
        )

        for i in range(5):

            text = f"{names[i]}: {fingers[i]}"

            cv2.putText(
                frame,
                text,
                (10, 115 + i * 25),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (0, 255, 0) if fingers[i] else (0, 0, 255),
                1
            )

        cv2.imshow("Hand Gesture LED Control", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            print("Closing camera...")
            break


except KeyboardInterrupt:

    print("Program interrupted!")


except Exception as error:

    print("ERROR:", error)


finally:

    # ======================================
    # UPDATED: Turn off LEDs only on exit
    # ======================================

    if arduino is not None and arduino.is_open:

        try:
            arduino.write(b"00000\n")
            time.sleep(0.2)

        except Exception:
            pass

    if camera is not None:
        camera.release()

    if hands is not None:
        hands.close()

    if arduino is not None and arduino.is_open:
        arduino.close()

    cv2.destroyAllWindows()

    print("All devices closed!")



# # pip install mediapipe==0.10.21
# # py -3.12 -m venv venv312
# # venv312\Scripts\activate