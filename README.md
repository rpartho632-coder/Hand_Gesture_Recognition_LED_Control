
# Hand Gesture Recognition LED Control

A real-time Hand Gesture Recognition LED Control
System using Python, OpenCV, MediaPipe, Arduino UNO
and Proteus Simulation.

## Features

- Real-time Hand Detection
- Five Finger Recognition
- Control 5 LEDs using Hand Gestures
- Serial Communication between Python and Arduino
- I2C LCD Display
- Proteus Virtual Simulation
- Maintains the last LED state when the hand
  is removed from the camera

## Technologies Used

- Python
- OpenCV
- MediaPipe
- PySerial
- Arduino UNO
- C++
- Proteus 8 Professional
- Arduino IDE

## Project Structure

```text
Hand_Gesture_Recognition_LED_Control/
├── Python/
├── Arduino/
├── Proteus/
├── Images/
├── .gitignore
└── README.md
```

## Hardware Components

- Arduino UNO
- 5 LEDs
- 5 Resistors
- 16x2 I2C LCD
- Virtual Serial Port Pair
- Computer Webcam

## Arduino Pin Configuration

| Component | Arduino Pin |
|---|---|
| Thumb LED | D2 |
| Index LED | D3 |
| Middle LED | D4 |
| Ring LED | D5 |
| Little LED | D6 |

## Serial Configuration

- Python Port: COM10
- Proteus Port: COM11
- Baud Rate: 9600

Note: Configure the virtual COM port pair
according to your computer.

## Python Installation

Install Python 3.12.

Install required packages:

```bash
pip install -r Python/requirements.txt
```

Run the Python program:

```bash
python Python/main.py
```

## Arduino Setup

1. Open the Arduino IDE.
2. Open the Arduino source file.
3. Select Arduino UNO.
4. Compile the code.
5. Export the compiled HEX file.

## Proteus Simulation

1. Open the Proteus project.
2. Load the Arduino HEX file.
3. Configure the COMPIM serial port.
4. Start the simulation.
5. Run the Python program.

## How It Works

The webcam captures hand movements.
MediaPipe detects the five fingers.
Python sends the finger states through serial
communication to Arduino UNO in Proteus.

Arduino controls five LEDs and updates the LCD.

When the hand disappears from the camera,
the previous LED state remains unchanged.

## Author

Partho Chandra Roy

## License

This project is open-source under the MIT License.
