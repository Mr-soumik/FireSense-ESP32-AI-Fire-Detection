<div align="center">

# 🔥 FireSense — AI Fire Detection with ESP32

**Real-time computer-vision fire detection that triggers a physical alarm — built with Python, OpenCV and an ESP32.**

![ESP32](https://img.shields.io/badge/Hardware-ESP32-E7352C?style=for-the-badge&logo=espressif&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.8%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)
![OpenCV](https://img.shields.io/badge/OpenCV-Computer%20Vision-5C3EE8?style=for-the-badge&logo=opencv&logoColor=white)
![Arduino](https://img.shields.io/badge/Arduino-IDE-00979D?style=for-the-badge&logo=arduino&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

[![YouTube](https://img.shields.io/badge/YouTube-TechTadka360-FF0000?style=for-the-badge&logo=youtube&logoColor=white)](https://youtube.com/@techtadka360official)
[![Instagram](https://img.shields.io/badge/Instagram-techtadka360official-E4405F?style=for-the-badge&logo=instagram&logoColor=white)](https://instagram.com/techtadka360official)
[![Facebook](https://img.shields.io/badge/Facebook-TechTadka360-1877F2?style=for-the-badge&logo=facebook&logoColor=white)](https://www.facebook.com/share/1EkKAJNLdB/)

</div>

---

## 📖 Overview

**FireSense** watches a live webcam feed, detects flames in real time, and instantly drives a physical alarm on an **ESP32**.

- 🟢 **No fire** → screen shows `SAFE`, green LED stays on
- 🔴 **Fire detected** → screen shows `FIRE DETECTED`, red LED and buzzer blink

The PC does the vision work and talks to the ESP32 over USB serial. No cloud, no internet, no model download required.

## Author

**Soumik Ghosh** — *TechTadka360*  
- YouTube: [@techtadka360](https://www.youtube.com/@techtadka360official)  
- Instagram: [@techtadka360official](https://www.instagram.com/techtadka360official)  
- GitHub: [Mr-soumik](https://github.com/Mr-soumik)
- Facebook: [@techtadka360](https://www.facebook.com/share/1F3sa9eeeV/)

## ✨ Features

- Real-time flame detection using HSV colour segmentation in OpenCV
- Noise filtering with blur, erosion and dilation
- Voting window across frames to cut false alarms and flicker
- Auto-detects the ESP32 serial port (or pass it manually)
- Clean on-screen `SAFE` / `FIRE DETECTED` status overlay
- ESP32 fail-safe: outputs switch off if the PC link is lost for 3 seconds
- Single-file ESP32 sketch, single-file Python script
- Easy to tune from the constants at the top of the script

## 🧰 Components Required

| Qty | Component |
|-----|-----------|
| 1 | ESP32 Dev Module |
| 1 | Green LED |
| 1 | Red LED |
| 2 | 220Ω resistors |
| 1 | Active buzzer |
| 1 | Breadboard + jumper wires |
| 1 | USB cable |
| 1 | PC / laptop with webcam (or phone via DroidCam) |

## 🔌 Wiring

| ESP32 Pin | Connects To |
|-----------|-------------|
| GPIO 26 | 220Ω resistor → Green LED (+), LED (−) → GND |
| GPIO 27 | 220Ω resistor → Red LED (+), LED (−) → GND |
| GPIO 25 | Buzzer (+), Buzzer (−) → GND |

## 🚀 Getting Started

### 1. Flash the ESP32
1. Open `FireSense_ESP32.ino` in Arduino IDE
2. Select board **ESP32 Dev Module**
3. Select the correct COM port and click **Upload**
4. Close Serial Monitor afterwards (it blocks the port)

### 2. Install Python dependencies
```bash
pip install opencv-python numpy pyserial
```

### 3. Run
```bash
python fire_detect.py
```
If the port is not found automatically:
```bash
python fire_detect.py COM5
```
Press `q` or `Esc` to quit.

## ⚙️ How It Works

```
Webcam ──► OpenCV (HSV fire mask + filtering) ──► Frame voting ──► Serial 'F' / 'S' ──► ESP32 ──► LEDs + Buzzer
```

1. Each frame is blurred and converted to HSV
2. Pixels in the bright orange-yellow flame range are masked
3. Small noise is removed and remaining regions are measured
4. Detection must pass a multi-frame vote before the alarm triggers
5. The PC sends `F` (fire) or `S` (safe) to the ESP32, which drives the outputs

## 🛠️ Tuning

Edit the constants at the top of `fire_detect.py`:

| Setting | Purpose |
|---------|---------|
| `CAMERA_INDEX` | Change to `1` if the wrong camera opens |
| `MIN_AREA` | Lower to detect smaller flames, raise to reduce false alarms |
| `LOWER` / `UPPER` | HSV range of flame colour |
| `VOTE_WINDOW` / `VOTE_NEEDED` | How many frames must agree before alarm |
| `CLEAR_FRAMES` | How long flame must be gone before returning to SAFE |

## ❓ Troubleshooting

- **Camera not opening** → change `CAMERA_INDEX`
- **Fire not detected** → lower `MIN_AREA`, improve lighting
- **False alarms** → raise `MIN_AREA`, remove bright orange/yellow objects from view
- **Buzzer only clicks** → it is a passive buzzer; use an active one
- **Port busy** → close Arduino Serial Monitor

## ⚠️ Disclaimer

This is an educational and demonstration project. It is **not** a certified safety device and must **not** be relied on to protect life or property. Always use a certified smoke or fire alarm.

## 📁 Project Structure

```
FireSense/
├── FireSense_ESP32.ino   # ESP32 firmware
├── fire_detect.py        # PC-side vision script
└── README.md
```

## 🌐 Connect With Me

**TechTadka360** — Electronics, ESP32, Arduino and DIY maker projects.

| Platform | Link |
|----------|------|
| ▶️ YouTube | [@techtadka360official](https://youtube.com/@techtadka360official) |
| 📸 Instagram | [@techtadka360official](https://instagram.com/techtadka360official) |
| 👍 Facebook | [TechTadka360](https://www.facebook.com/share/1EkKAJNLdB/) |
| 💻 GitHub | [Mr-soumik](https://github.com/Mr-soumik) |

If this project helped you, please ⭐ the repo and subscribe for more builds!

## 📄 License

Released under the [MIT License](LICENSE).

---

<div align="center">

**Made with ❤️ by Soumik · TechTadka360**

</div>
