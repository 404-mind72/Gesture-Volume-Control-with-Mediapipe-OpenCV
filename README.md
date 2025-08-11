## 🎛 Gesture Volume Control with Mediapipe & OpenCV
## 📌 Project Description
Gesture Volume Control is a Python-based application that allows users to control their computer's volume simply by gesturing with their hands in front of the camera.
This application utilizes MediaPipe Hands to detect hand landmarks and then measures the distance between the thumb and index finger as a reference for volume.
Volume control is performed through PyCaw, which interacts directly with the Windows audio system.

## ✨ Key Features
- Real-time Volume Control — slide the distance between your thumb and index finger to adjust the volume.
- Accurate Hand Detection — uses MediaPipe with a model optimized for single hands.
- Fingertip Coordinates — each fingertip is labeled (x, y) on the screen.
- Volume Indicator — a visual bar that moves up and down as the finger distance changes.
- FPS Monitoring — displays FPS to ensure optimal camera performance.
- Hand Skeleton Visualization — green lines and red dots for each hand joint.

## 🛠 Technology Used
- OpenCV Captures and processes video from a camera
- MediaPipe Hands Detects hand landmarks in real-time
- NumPy Mathematical calculations and value interpolation
- PyCaw Volume control on Windows operating systems
- Comtypes Interacts with Windows APIs via COM

🏗 Program Architecture
1. Video Capture
   The camera captures video frames using cv2.VideoCapture().
2. Landmark Detection
   The frames are processed with MediaPipe Hands to obtain 21 landmark points.
3. Distance Calculation
   The program takes the coordinates of landmarks ID 4 (thumb) and ID 8 (index finger) and calculates the distance using math.hypot().
4. Volume Interpolation
   The distance values are converted to the system volume scale using numpy.interp().
5. System Volume Control
   The volume is controlled through the PyCaw API.
6. Visualization
   Displaying connecting lines between hand points Circles and coordinate labels at the fingertips

FPS in the upper left corner

Volume bar on the left side of the screen
