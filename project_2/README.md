## EDES301 Project 2: Digital Etch-A-Sketch PCB

## Project Overview
This project involves the design and layout of a custom Printed Circuit Board (PCB) for a digital Etch-A-Sketch system. The board interfaces a microcontroller development board with an SPI LCD screen, analog inputs for drawing control, and digital inputs for system commands.

This design was created using Autodesk EAGLE as part of the EDES301 course requirements.

## Hardware Specifications
The PCB connects the following components to the main microcontroller:
* **Display:** Interface for Adafruit SPI LCD Screen (Model 1770 or similar).
* **User Input:**
    * 2x Potentiometers (Control for X and Y axis drawing).
    * 2x Push Buttons (For "Clear Screen" or mode selection).
* **Status Indicators:** Red, Green, and Blue LEDs for system status feedback.
* **Storage:** MicroSD card slot for saving drawings or loading assets.
* **Host:** Headers for NUCLEO development board connection.

## Manufacturing
The board is designed with standard 2-layer constraints:
* **Trace Width:** 10 mil (Signal) / 15 mil (Power).
* **Vias:** 12 mil drill / 24 mil diameter.
* **Fabrication:** Files are formatted for standard CAM processing (Gerber RS-274X).
