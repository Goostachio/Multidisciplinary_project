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

Before you proceed, ensure that you have Python version 3.8 or above installed with these libraries:

- adafruit-io
- tensorflow
- keras
- Pillow
- opencv-python
- pyserial
- numpy
- dash
- pandas
- dash_bootstrap_components
- dash_bootstrap_template
- plotly 

A free account on [Adafruit IO](https://io.adafruit.com/) is also required.  

### Installation

1. Clone the repository.
2. Run the main.py file.
3. Visit http://127.0.0.1:8050/ for the data analytics (shown on a local dashboard).
4. visit https://io.adafruit.com/Multidisciplinary_Project/dashboards/ai-iot-dashboard?kiosk=true to view the adafruit dashboard.
