# Multidisciplinary Project - Smart AC

A simplified model of a smart air conditioner using rudimentory sensors and commands

## Key Features

- **Automatic cooling and humidifying**: Handoff control the cooling and humidifying system through temperature and humidity
sensory.
- **Human detection**: AC operation based on human presence detected through a camera.
- **Energy consumption calculation**: Collect usage data to process energy consuption rate per month.
- **GPS locator**: AC operation based on individuals’ GPS location (for now, only the admin
(house owner) is tracked).

## Getting Started
### Prerequisites

Before you proceed, ensure that you have Python 3.8 installed with these libraries:

- adafruit-io
- tensorflow
- keras
- Pillow
- opencv-python
- pyserial

A free account on [Adafruit IO](https://io.adafruit.com/) is also required.  

### Installation

1. Clone the repository.
2. Create a file named "key" and save your Adafruit IO key there.
3. Run the main.py file.
