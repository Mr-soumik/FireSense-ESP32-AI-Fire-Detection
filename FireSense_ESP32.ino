const int GREEN_LED = 26;
const int RED_LED = 27;
const int BUZZER = 25;

char state = 'S';
unsigned long lastRx = 0;
unsigned long lastBeep = 0;
bool beepOn = false;

void setup() {
  Serial.begin(115200);
  pinMode(GREEN_LED, OUTPUT);
  pinMode(RED_LED, OUTPUT);
  pinMode(BUZZER, OUTPUT);
  digitalWrite(GREEN_LED, HIGH);
  digitalWrite(RED_LED, HIGH);
  digitalWrite(BUZZER, HIGH);
  delay(300);
  digitalWrite(GREEN_LED, LOW);
  digitalWrite(RED_LED, LOW);
  digitalWrite(BUZZER, LOW);
  lastRx = millis();
}

void loop() {
  while (Serial.available()) {
    char c = Serial.read();
    if (c == 'F' || c == 'S') {
      state = c;
      lastRx = millis();
    }
  }

  if (millis() - lastRx > 3000) {
    digitalWrite(GREEN_LED, LOW);
    digitalWrite(RED_LED, LOW);
    digitalWrite(BUZZER, LOW);
    return;
  }

  if (state == 'F') {
    digitalWrite(GREEN_LED, LOW);
    if (millis() - lastBeep >= 150) {
      lastBeep = millis();
      beepOn = !beepOn;
      digitalWrite(RED_LED, beepOn);
      digitalWrite(BUZZER, beepOn);
    }
  } else {
    digitalWrite(GREEN_LED, HIGH);
    digitalWrite(RED_LED, LOW);
    digitalWrite(BUZZER, LOW);
    beepOn = false;
  }
}
