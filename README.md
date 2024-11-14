# LED strip controller with voice recognition 

This is the programming part of my BEng thesis - 3 colour LED strip controller with voice commands.

## About & features

- Controls the colour and brightness
- Three built-in operation modes:
  1. RGB -  smooth transitions between different colours, constant brightness
  2. Breathing - constant colour with changing brightness gives the effect of breathing
  3. Static - both colour and brightness are constant, but can be set
- Allows for setting up to 2 schedules with 2 different colours, brightness levels and modes changing at specified time
- Allows for storing up to 3 user defined custom colours
- Handles physical key presses through GPIO module
- Handles voice commands via record.py (requires a microphone and the Internet connection)
- Uses PWM to control the low-voltage nMOSFET transistors (connected to the 5 V output), which in turn change the power transferred to each colour row

## Technologies

- Python
- Raspberry Pi
- GPIO

## Installation

1. Clone the repo
   ```bash
   https://github.com/arthel37/Engineering_thesis/
   ```
2. Connect the circuit
3. Run record.py in the background
4. Run led_har.py
