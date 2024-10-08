# Hand-Gesture-Recognition-System-for-Hospitals

## Overview

This project implements a **Hand Gesture Recognition System** using **OpenCV** and **Python**. The system captures real-time video from a webcam, detects hand gestures, and maps them to specific actions such as calling a nurse, requesting water, or turning off lights. The project is particularly useful in hands-free environments such as healthcare or smart home control.

## Features

- Real-time hand gesture detection using a webcam.
- Skin color segmentation to isolate the hand from the background.
- Contour detection** to identify the hand region.
- Convex hull and convexity defect analysis to detect the number of raised fingers.
- Mapped gestures to commands such as:
  - 1 finger: Call nurse
  - 2 fingers: Need water
  - 3 fingers: Pain relief
  - 4 fingers: Call doctor
  - 5 fingers: Need help
  - ... and more.

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/<your-username>/<repository-name>.git
   cd <repository-name>
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the program:
   ```bash
   python gesture_recognition.py
   ```

## Dependencies

- Python 3.x
- OpenCV for image processing and video capture.
- NumPy for numerical operations.

Install dependencies using:
```bash
pip install opencv-python numpy
```
## How It Works

1. Video Capture: The webcam feed is captured and processed frame by frame.
2. Region of Interest (ROI): A specific area in the frame is defined where the hand gestures will be detected.
3. Skin Detection: The system uses a defined HSV color range to detect skin color and isolate the hand from the background.
4. Contour and Convex Hull: The largest contour is considered as the hand, and a convex hull is applied around it. Convexity defects between the hand and hull are analyzed to detect raised fingers.
5. Gesture Recognition: The system counts the number of fingers and matches them with pre-defined gestures for specific actions.
## Gesture Mapping
- 1 finger: Call nurse
- 2 fingers: Need water
- 3 fingers: Pain relief
- 4 fingers: Call doctor
- 5 fingers: Need help
- 6+ fingers: Additional actions like turning off lights, turning on TV, etc.
## Example Output

| Gesture        | Action                |
|----------------|-----------------------|
| 1 finger       | Call nurse            |
| 2 fingers      | Need water            |
| 3 fingers      | Pain relief           |
| 4 fingers      | Call doctor           |
| 5 fingers      | Need help             |
| 6+ fingers     | Smart home controls   |

## Customization

You can modify the gestures and their associated actions by editing the logic inside the `process_frame()` function. For example, you can add more custom gestures or map the existing gestures to different actions.

## Future Improvements

- Gesture recognition accuracy improvement.
- Adding support for more gestures.
- Integration with IoT devices for smart home control.
- Deploying on mobile or embedded systems for real-world applications.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
## Author
Pragna Seetha
