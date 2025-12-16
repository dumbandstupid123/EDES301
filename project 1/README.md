📡 Pocket Radar — Autonomous Sentry System (PocketBeagle)

A terrestrial scanning “sentry radar” powered by a PocketBeagle (Debian Linux).

Scans a 180° sector using an HC-SR04 ultrasonic sensor mounted on an SG90 servo, then renders detections on a self-hosted, military-style web dashboard — no cloud required.

Features

Real-time visualization: HTML5 Canvas dashboard served from the PocketBeagle
Auto-Scan mode: continuous sweep left ↔ right
Manual “Sniper” mode: aim precisely via a web slider
Intruder alert: RED ALERT + optional lock when targets breach threshold (default < 30 cm)
Driverless GPIO: raw Linux SysFS interaction (bypasses flaky GPIO libraries)

Hardware Required
PocketBeagle (Debian Linux image)
SG90 Micro Servo (pan mechanism)
HC-SR04 Ultrasonic sensor
Breadboard (power rails)
Jumper wires (male-to-male)
Micro-USB cable (power + data)
Voltage Warning (Important)

PocketBeagle GPIO uses 3.3V logic. HC-SR04 is usually powered by 5V, and its ECHO output may be 5V.

Do not drive a 3.3V GPIO input directly with a 5V ECHO pin.
Use a voltage divider or level shifter on ECHO → PocketBeagle.

Example divider (common):

1 kΩ from ECHO → GPIO
2 kΩ from GPIO → GND

🔌 Wiring
1) Power rails

PocketBeagle P1_05 (VBUS / 5V) → Breadboard + rail (red)
PocketBeagle P1_16 (GND) → Breadboard - rail (blue)

2) Servo (SG90)
Servo Red → + rail (5V)
Servo Brown → - rail (GND)
Servo Orange (signal) → PocketBeagle P1_36

3) Ultrasonic (HC-SR04)

VCC → + rail (5V)
GND → - rail (GND)
TRIG → PocketBeagle P2_02
ECHO → PocketBeagle P2_04 (through level shifting recommended)

🚀 Setup
Step 1 — Connect to Cloud9 IDE

Plug the PocketBeagle into your computer via USB, then open:

Windows: http://192.168.7.2:3000
Mac/Linux: http://192.168.6.2:3000

Step 2 — Create the script

In Cloud9, create:

sonar.py
Paste the code from this repo into that file.

Step 3 — Run
sudo python3 pocket_radar.py

sudo is required for hardware pin access.

🖥️ Dashboard

Open the dashboard in a browser:

Windows: http://192.168.7.2:8888
Mac/Linux: http://192.168.6.2:8888

Controls

AUTO SCAN: default — sweeps left and right continuously
MANUAL AIM: stops sweep; aim with slider
SCAN SPEED: lower value = faster stepping
ALARM THRESHOLD (cm): triggers RED ALERT

🔧 Troubleshooting

Distance always 0 / “Timeout”
Check power: sensor VCC must be on 5V rail from P1_05

Confirm TRIG (P2_02) and ECHO (P2_04) aren’t swapped
Make sure ECHO is not overdriving GPIO (use divider/level shifter)

Servo buzzes but doesn’t move
Servo is underpowered — must be on 5V rail (P1_05) with shared ground

Don’t power a servo from a 3.3V GPIO pin
OSError: [Errno 98] Address already in use

Old instance is still running:
sudo fuser -k 8888/tcp

📝 License
Open-source — build your own sentry bot.
