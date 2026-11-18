
#include <Wire.h>
#include <LiquidCrystal_I2C.h>

LiquidCrystal_I2C lcd(0x20, 16, 2);

const int ledPins[5] = {2, 3, 4, 5, 6};

String receivedData = "";

// ======================================
// UPDATED: Store the last LED states
// ======================================

int lastFingers[5] = {0, 0, 0, 0, 0};

void updateLCD(int openCount) {

  lcd.clear();

  lcd.setCursor(0, 0);
  lcd.print("LED:");
  lcd.print(openCount > 0 ? "ON " : "OFF");

  lcd.print(" O:");
  lcd.print(openCount);

  lcd.setCursor(0, 1);
  lcd.print("OPEN:");
  lcd.print(openCount);

  lcd.print(" CLOSE:");
  lcd.print(5 - openCount);
}


void setup() {

  Serial.begin(9600);

  for (int i = 0; i < 5; i++) {

    pinMode(ledPins[i], OUTPUT);

    digitalWrite(ledPins[i], LOW);
  }

  lcd.init();
  lcd.backlight();

  lcd.setCursor(0, 0);
  lcd.print("Hand Gesture AI");

  lcd.setCursor(0, 1);
  lcd.print("Waiting Data...");

}


void loop() {

  while (Serial.available() > 0) {

    char ch = Serial.read();

    if (ch == '\n') {

      processData(receivedData);

      receivedData = "";

    }

    else if (ch != '\r') {

      if (receivedData.length() < 5) {

        receivedData += ch;

      }

      else {

        receivedData = "";

      }

    }

  }

}


void processData(String data) {

  if (data.length() != 5) return;

  // Validate received data
  for (int i = 0; i < 5; i++) {

    if (data[i] != '0' && data[i] != '1') {

      return;

    }

  }

  int openCount = 0;

  // ======================================
  // UPDATED: Update only when new valid
  // data is received. Otherwise last state
  // remains unchanged.
  // ======================================

  for (int i = 0; i < 5; i++) {

    lastFingers[i] = data[i] - '0';

    digitalWrite(
      ledPins[i],
      lastFingers[i]
    );

    openCount += lastFingers[i];

  }

  updateLCD(openCount);

}
