# SmartRecycle AI — Smart Waste Sorting System

**SmartRecycle AI** is a graduation project that combines computer vision with an Arduino-based sorting mechanism. It uses a custom-trained **YOLO11s** object detection model to recognize recyclable waste in real time and provides a desktop dashboard for monitoring detections.

The system recognizes four waste categories: **glass, plastic, paper, and metal**.

## Features

- **Real-time detection:** Processes live camera frames using a YOLO model (`best.pt`).
- **Visual predictions:** Draws bounding boxes, class names, and confidence scores on detected objects.
- **Desktop dashboard:** Displays the camera stream, prediction confidence, device/model status, and detection statistics.
- **Analysis views:** Includes category distribution and detection activity visualizations.
- **Arduino communication:** Sends a category-specific command through a serial connection to support physical waste sorting.
- **Detection stability:** Requires consistent detections before sending commands to reduce repeated or accidental triggering.

## Technologies

- **Python** — application logic
- **Ultralytics YOLO11** — waste detection
- **OpenCV** — camera capture and image processing
- **PySide6 (Qt)** — desktop interface
- **PySerial** — Arduino serial communication
- **NumPy** — image-processing dependency

## How It Works

1. A connected camera captures a live video stream.
2. The trained YOLO model predicts waste categories and confidence scores.
3. The interface shows the predictions and updates the monitoring views.
4. Once a detection meets the confidence and stability rules, the application sends a serial command to the Arduino, if connected.
5. The Arduino-controlled mechanism can then direct the item to its designated compartment.

The detection configuration in `logic/camera_engine.py` currently uses a **0.70 confidence threshold**, **5 stable frames**, and a **4-second command cooldown**.

### Arduino command mapping

| Detected waste | Serial command |
| --- | --- |
| Glass | `a` |
| Plastic | `b` |
| Paper | `c` |
| Metal | `d` |

Commands are sent as lines, for example `a\n`, over a **9600 baud** serial connection. The configured Windows port is `COM5`; change it to match your machine.

> **Hardware note:** The Python application continues running if the Arduino is not connected, but physical sorting requires compatible Arduino hardware and firmware. Arduino firmware is not included in this repository.

## Project Structure

```text
smart-waste-sorting-system/
├── main.py                  # Application entry point
├── best.pt                  # Trained YOLO model weights
├── components/              # Reusable Qt interface components
├── core/                    # Main window and application pages
├── logic/
│   └── camera_engine.py     # Camera, inference and serial commands
├── assets/                  # Interface icons, styling and graphics
├── *.html                   # Supporting interface design files
├── .gitignore
└── requirements.txt
```

## Installation and Run

**Prerequisites:** Python, a working camera, and an operating system that supports the installed Qt and YOLO dependencies. An Arduino is optional for viewing predictions, but required for physical sorting.

1. Clone the repository:

   ```bash
   git clone https://github.com/ahmetsezerr/smart-waste-sorting-system.git
   cd smart-waste-sorting-system
   ```

2. Create a virtual environment:

   ```bash
   python -m venv .venv
   ```

3. Activate the virtual environment on Windows PowerShell:

   ```powershell
   .\.venv\Scripts\Activate.ps1
   ```

4. Install the dependencies:

   ```bash
   python -m pip install -r requirements.txt
   ```

5. Launch from the **repository root** (where `best.pt` is located):

   ```bash
   python main.py
   ```

6. Open the dashboard and start the camera to begin detection.

If the Arduino is connected to a different port, edit `SERIAL_PORT` in `logic/camera_engine.py`. The default camera index is `0`; change `camera_index` in `core/main_window.py` if you need a different camera.

## Screenshots

Screenshots of the dashboard, live prediction results, and analysis page can be added here to demonstrate the application.

## Scope and Notes

- The included `best.pt` file is the trained inference model. The original training image dataset and training notebooks are not included in this repository.
- The main desktop interface is implemented with **PySide6**. HTML files in the repository are supplementary design resources, not the runtime frontend.
- Detection counters and visualizations describe the application's current session; the repository does not include a persistent database for these statistics.
- This is an academic graduation project and a demonstration of AI-assisted waste classification and sorting, rather than a production-ready industrial system.
