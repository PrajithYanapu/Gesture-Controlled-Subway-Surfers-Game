# Gesture-Controlled Subway Surfers 🚅✨

Control [Subway Surfers](https://poki.com/en/g/subway-surfers) using hand gestures via webcam! Built with Python, MediaPipe, Selenium, and PyAutoGUI.

## Features
- **Hand Gesture Recognition**: Detect fingers using MediaPipe.
- **Game Automation**: Launch and interact with Subway Surfers via Selenium.
- **Keyboard Mapping**:
  - 👆 **1 Finger**: Jump (↑ key)
  - ✌️ **2 Fingers**: Roll (↓ key)
  - 🤟 **3 Fingers**: Move Right (→ key)
  - 🖖 **4 Fingers**: Move Left (← key)
- **Performance Optimized**: Frame skipping and high-confidence detection.

## Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/ankitparwatkar/Gesture-Controlled-Gaming-Setup.git
   cd gesture-controlled-subway-surfers
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
   *`requirements.txt`:*
   ```
   selenium==4.10.0
   opencv-python==4.5.3.56
   mediapipe==0.9.0
   pyautogui==0.9.54
   ```

3. **Download ChromeDriver**:
   - Ensure your Chrome browser version matches the driver.
   - Download from [ChromeDriver](https://sites.google.com/chromium.org/driver/) and place it in the project root.

## Usage

1. **Launch the Jupyter Notebook**:
   ```bash
   jupyter notebook game.ipynb
   ```

2. **Run the Selenium Cell**:
   - Executes `game.ipynb` cells sequentially.
   - Wait 5 seconds for the game to load on Poki.com.
   - Click the game window to focus it.

3. **Gesture Control**:
   - Show your hand to the webcam.
   - Use finger counts (1-4) to trigger actions.
   - Press `q` to quit the gesture controller.

## Troubleshooting

- **Kernel Crashes**:
  - Ensure `chromedriver` is in the project root.
  - Grant webcam access to Jupyter.
  - Update dependencies to the exact versions listed.

- **Laggy Gestures**:
  - Adjust `frame_skip` in the notebook (higher = fewer frames processed).
  - Reduce background applications.

## How It Works

1. **MediaPipe Hands**: Detects 21 hand landmarks in real-time.
2. **Finger Counting Logic**:
   ```python
   # Checks if fingertip (e.g., index finger at landmark 8) is above lower joint
   finger_count = sum([1 for idx in [8, 12, 16, 20] 
                       if hand_landmarks.landmark[idx].y < hand_landmarks.landmark[idx-2].y])
   ```
3. **PyAutoGUI**: Translates finger counts to keyboard presses.

---

Made with ❤️ by Ankit Parwatkar. Acknowledge [MediaPipe](https://mediapipe.dev/) and [Selenium](https://www.selenium.dev/).
```
