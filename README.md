🖐️ Virtual Mouse Using OpenCV
Control your computer's mouse pointer with hand movements captured by a webcam.
This Python project uses OpenCV to capture and process video, MediaPipe to detect hand landmarks, and PyAutoGUI to move the cursor and perform clicks.
✨ Features
- Real-time webcam input and detection of one hand.
- Cursor movement using the index fingertip.
- Left-click by bringing the thumb and index fingertip close together.
- Smoothed cursor movement to reduce shaking.
- On-screen hand landmarks and a highlighted fingertip.
- Yellow control region, live status messages, and an FPS display.
- Green visual feedback when a click is triggered.
🛠️ Technologies
Technology	Purpose
Python	Application logic
OpenCV	Webcam capture, image processing, and visual interface
MediaPipe	Hand landmark detection
PyAutoGUI	Mouse movement and clicking
NumPy	Mapping webcam coordinates to screen coordinates


⚙️ Setup
Requirements
- Python 3.11 recommended for the dependency versions below.
- A working webcam.
- A desktop session where the application can access the camera and control the pointer.
1. Download the project
git clone https://github.com/Tilanwishwajith-ai/Virtual-Mouse-Project.git
cd Virtual-Mouse-Project
2. Create a virtual environment
python -m venv .venv
Activate it on Windows Command Prompt:
.venv\Scripts\activate.bat
Or on macOS/Linux:
source .venv/bin/activate
3. Install dependencies
python -m pip install --upgrade pip
python -m pip install "numpy==1.26.4" "opencv-contrib-python==4.11.0.86" "mediapipe==0.10.21" pyautogui
The current script uses MediaPipe's legacy mp.solutions.hands API. These versions retain that API and keep the OpenCV and NumPy requirements compatible. Install this OpenCV package in the new environment without adding another OpenCV package alongside it.
4. Run the application
python virtual_mouse.py
🎮 Controls
Action	How to use it
Move the cursor	Move your index fingertip across the yellow control region
Left-click	Bring your thumb and index fingertip close together
Stop the application	Focus the webcam window and press Q


For better tracking, keep your hand visible and use good lighting.
🧠 How It Works
1. OpenCV captures a webcam frame and mirrors it.
2. MediaPipe detects the hand landmarks.
3. The script reads the index fingertip and thumb-tip positions.
4. NumPy maps the index fingertip position to the screen coordinates.
5. A smoothing calculation reduces abrupt cursor movement.
6. PyAutoGUI moves the pointer.
7. When the two fingertips are less than 40 pixels apart in the webcam frame, the script triggers a left-click.
🔧 Configuration
The settings are currently defined inside virtual_mouse.py.
Setting	Current value
Camera index	0
Requested camera resolution	1280 × 720
Maximum detected hands	1
Cursor smoothing factor	5
Control-region inset	100 pixels
Click-distance threshold	40 pixels


The camera's actual resolution depends on the webcam.
📌 Current Limitations
- Only one hand is tracked.
- Holding the pinch gesture can trigger repeated clicks because the script checks it on every frame.
- Right-click, scrolling, and drag-and-drop are not currently implemented.
🌱 Future Improvements
- Add a click cooldown to prevent repeated clicks.
- Support scrolling, right-click, and drag gestures.
- Add camera-connection error handling.
- Migrate hand detection to the newer MediaPipe Tasks API.
👨‍💻 Author
Tilan Wishwajith
- Email: tilanwishwajith@gmail.com
- GitHub: Tilanwishwajith-ai
- LinkedIn: Tilan Wishwajith
📚 References
- OpenCV Python packages 
- MediaPipe 0.10.21
- MediaPipe legacy Solutions API change
