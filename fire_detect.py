import sys
import time
from collections import deque

import cv2
import numpy as np
import serial
import serial.tools.list_ports

CAMERA_INDEX = 0
BAUD = 115200
MIN_AREA = 120
LOWER = np.array([0, 110, 215])
UPPER = np.array([35, 255, 255])
VOTE_WINDOW = 6
VOTE_NEEDED = 3
CLEAR_FRAMES = 12


def find_port():
    if len(sys.argv) > 1:
        return sys.argv[1]
    for p in serial.tools.list_ports.comports():
        text = (p.description + " " + p.hwid).upper()
        if any(k in text for k in ("CP210", "CH340", "CH910", "USB SERIAL", "USB-SERIAL", "SILICON LABS", "UART")):
            return p.device
    ports = list(serial.tools.list_ports.comports())
    return ports[0].device if ports else None


def detect_fire(frame):
    blur = cv2.GaussianBlur(frame, (7, 7), 0)
    hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, LOWER, UPPER)
    mask = cv2.erode(mask, None, iterations=1)
    mask = cv2.dilate(mask, None, iterations=3)
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    boxes = []
    for c in contours:
        if cv2.contourArea(c) >= MIN_AREA:
            boxes.append(cv2.boundingRect(c))
    return boxes


def draw_label(frame, text, bg):
    h, w = frame.shape[:2]
    font = cv2.FONT_HERSHEY_DUPLEX
    scale = 1.1 if text != "SAFE" else 0.8
    (tw, th), _ = cv2.getTextSize(text, font, scale, 2)
    x = (w - tw) // 2
    y = h - 30
    cv2.rectangle(frame, (x - 14, y - th - 14), (x + tw + 14, y + 14), bg, -1)
    cv2.putText(frame, text, (x, y), font, scale, (255, 255, 255), 2, cv2.LINE_AA)


def main():
    port = find_port()
    if not port:
        print("ESP32 not found. Plug it in and run: python fire_detect.py COM5")
        return
    print("Using port:", port)
    esp = serial.Serial(port, BAUD, timeout=0.1)
    time.sleep(2)

    cap = cv2.VideoCapture(CAMERA_INDEX)
    if not cap.isOpened():
        print("Camera not opened. Change CAMERA_INDEX at top of file.")
        return
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    votes = deque(maxlen=VOTE_WINDOW)
    fire = False
    clear_count = 0
    last_sent = 0
    last_char = "S"

    while True:
        ok, frame = cap.read()
        if not ok:
            break

        boxes = detect_fire(frame)
        votes.append(1 if boxes else 0)

        if sum(votes) >= VOTE_NEEDED:
            fire = True
            clear_count = 0
        elif fire:
            clear_count += 1
            if clear_count >= CLEAR_FRAMES:
                fire = False

        ch = "F" if fire else "S"
        now = time.time()
        if ch != last_char or now - last_sent > 0.5:
            esp.write(ch.encode())
            last_sent = now
            last_char = ch

        if fire:
            for (x, y, w, h) in boxes:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
            draw_label(frame, "FIRE DETECTED", (40, 0, 190))
        else:
            draw_label(frame, "SAFE", (60, 160, 40))

        cv2.imshow("TechTadka360 FireSense", frame)
        if cv2.waitKey(1) & 0xFF in (ord("q"), 27):
            break

    esp.write(b"S")
    esp.close()
    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
