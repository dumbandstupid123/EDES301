📡 Pocket Radar: Autonomous Sentry System

Pocket Radar is a terrestrial scanning system powered by the PocketBeagle. It uses an ultrasonic sensor mounted on a servo motor to scan a 180-degree sector, detecting objects in real-time and visualizing them on a self-hosted "Military Style" web dashboard.

🎯 Features

Real-Time Visualization: HTML5 Canvas dashboard served directly from the chip (no cloud needed).

Auto-Scan Mode: Sweeps back and forth continuously.

Manual Sniper Mode: Control the turret angle precisely via a web slider.

Intruder Alert: Visual RED ALERT and logic locking when targets breach the safety threshold (< 30cm).

Driverless Architecture: Uses raw Linux SysFS interaction to bypass broken GPIO libraries.

🛠️ Hardware Requirements

PocketBeagle (x1): The brain (Debian Linux image).

SG90 Micro Servo (x1): Pan mechanism.

HC-SR04 Sensor (x1): Ultrasonic rangefinder.

Breadboard (x1): For power distribution.

Jumper Wires (x10+): Male-to-Male connections.

Micro-USB Cable (x1): Power & Data connection to laptop.

🔌 Wiring Guide (Crucial)

⚠️ WARNING: The PocketBeagle logic is 3.3V, but the sensor requires 5V. You MUST use the specific pins listed below to avoid damaging your board or having the sensor fail to trigger.

1. Power Distribution (The Rail)

PocketBeagle P1_05 (VBUS): Connect to Breadboard Red (+) Rail.

PocketBeagle P1_16 (GND): Connect to Breadboard Blue (-) Rail.

2. Servo Motor (SG90)

Red Wire: Connect to Red (+) Rail (5V).

Brown Wire: Connect to Blue (-) Rail (GND).

Orange Wire (Signal): Connect to PocketBeagle P1_36.

3. Ultrasonic Sensor (HC-SR04)

VCC: Connect to Red (+) Rail (5V).

GND: Connect to Blue (-) Rail (GND).

Trig: Connect to PocketBeagle P2_02.

Echo: Connect to PocketBeagle P2_04.

🚀 Installation & Setup

Step 1: Connect to the Board

Plug the PocketBeagle into your computer via USB. Open Chrome and navigate to the Cloud9 IDE:

Windows: http://192.168.7.2:3000

Mac/Linux: http://192.168.6.2:3000

Step 2: Create the Script

In the Cloud9 file tree, right-click and create a new file named pocket_radar.py. Paste the code from this repository into that file.

Step 3: Run the System

Open the terminal at the bottom of the Cloud9 window and run:

sudo python3 pocket_radar.py


Note: sudo is required to access the hardware pins.

🖥️ Using the Dashboard

Once the script is running, open a new browser tab and go to:

Windows: http://192.168.7.2:8888

Mac/Linux: http://192.168.6.2:8888

Controls

AUTO SCAN: The default mode. The radar sweeps left and right automatically.

MANUAL AIM: Stops the sweep. Drag the Manual Aiming slider to point the sensor at a specific angle.

SCAN SPEED: Adjust how fast the servo moves (Lower = Faster).

ALARM THRESHOLD: Set the distance (cm) for the "Red Alert" trigger.

🔧 Troubleshooting

Problem: "Timeout" or Distance is always 0

Fix: Check your power! Is the sensor VCC connected to the Red Rail? Is the Red Rail connected to P1_05? (P1_14 is only 3.3V and will not work).

Fix: Check wires. Are Trig (P2_02) and Echo (P2_04) swapped?

Problem: Servo buzzes but doesn't move

Fix: The servo is underpowered. Ensure it is sharing the P1_05 (5V) rail, not plugged into a 3.3V GPIO pin.

Problem: OSError: [Errno 98] Address already in use

Fix: The previous instance of the code is still running in the background. Run this command to kill it:

sudo fuser -k 8888/tcp


📝 License

This project is open-source. Feel free to modify and adapt for your own sentry bot needs!
