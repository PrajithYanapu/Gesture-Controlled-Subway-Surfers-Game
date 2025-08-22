🎮 Gesture-Controlled Subway Surfers 🚀🖐️

Play Subway Surfers hands-free — just wave your fingers in front of the webcam to jump, roll, and dodge trains! 🚆✨

This project combines computer vision, automation, and gaming to bring gesture-controlled gameplay to life. Built with Python, MediaPipe, Selenium, and PyAutoGUI, it transforms your hand gestures into real-time in-game actions.

🔑 Key Features

Hand Gesture Recognition 🖐️ – Real-time finger detection using MediaPipe Hands (21 landmark tracking).

Seamless Game Automation 🎯 – Launches and interacts with Subway Surfers on Poki.com via Selenium.

Gesture-to-Action Mapping 🎮

👆 1 Finger → Jump (↑ key)

✌️ 2 Fingers → Roll (↓ key)

🤟 3 Fingers → Move Right (→ key)

🖖 4 Fingers → Move Left (← key)

Optimized Performance ⚡ – Frame skipping + confidence thresholds for smooth real-time play.

⚙️ Tech Stack

Python 🐍 – Core logic

MediaPipe 🔍 – Hand tracking & gesture recognition

OpenCV 🎥 – Webcam integration

PyAutoGUI ⌨️ – Keyboard automation

Selenium 🌐 – Game launch & control

🚀 How It Works

Webcam → MediaPipe – Detects 21 hand landmarks.

Finger Counting Logic – Determines how many fingers are raised.

Mapped Gestures → Key Presses – PyAutoGUI sends key events (↑ ↓ → ←).

Subway Surfers Responds – Character jumps, rolls, or changes lane instantly.

🛠️ Installation & Setup
git clone https://github.com/ankitparwatkar/Gesture-Controlled-Gaming-Setup.git
cd gesture-controlled-subway-surfers
pip install -r requirements.txt


Add ChromeDriver to the project root (matching your Chrome version).

Run jupyter notebook game.ipynb.

Wave your hand & play 🚀.

🧩 Troubleshooting

Kernel Crash? → Place chromedriver in root & check webcam permissions.

Laggy Gestures? → Increase frame_skip in code or close background apps.

💡 Why It’s Cool

Turns your webcam into a game controller.

A perfect mashup of AI, automation, and fun gaming.

Demonstrates real-time computer vision + practical automation.

👉 This description is now engaging, professional, and unique, while still keeping it resume + GitHub friendly.
