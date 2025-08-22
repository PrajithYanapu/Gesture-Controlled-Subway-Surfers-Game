import streamlit as st
import cv2
import mediapipe as mp
import pyautogui
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import threading
import time
import queue

# --- Page Configuration ---
st.set_page_config(
    page_title="Gesture-Controlled Subway Surfers",
    page_icon="🎮",
    layout="wide"
)

# --- Custom CSS for a Modern UI ---
st.markdown("""
<style>
    /* General Styles */
    .stApp {
        background-color: #121212;
        color: #e0e0e0;
    }
    /* Main container for the title */
    .title-container {
        text-align: center;
        background: linear-gradient(45deg, #ff5722, #ff9800);
        color: white;
        padding: 25px;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(255, 87, 34, 0.5);
        margin-bottom: 20px;
    }
    .title-container h1 {
        font-size: 3em;
        font-weight: bold;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    /* Button Styles */
    .stButton>button {
        background-color: #ff5722;
        color: white;
        padding: 15px 30px;
        font-size: 1.2em;
        font-weight: bold;
        border-radius: 10px;
        border: none;
        box-shadow: 0 2px 5px rgba(0,0,0,0.2);
        transition: background-color 0.3s, transform 0.2s;
    }
    .stButton>button:hover {
        background-color: #e64a19;
        transform: scale(1.05);
    }
    /* Status indicators */
    .status-text {
        font-size: 1.1em;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# --- Session State Initialization ---
if 'is_running' not in st.session_state:
    st.session_state.is_running = False
if 'driver' not in st.session_state:
    st.session_state.driver = None
if 'stop_event' not in st.session_state:
    st.session_state.stop_event = threading.Event()

# --- MediaPipe Hand Tracking Setup ---
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7, min_tracking_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

# --- Core Functions ---

def launch_game_thread():
    """Launches the Subway Surfers game in a Selenium-controlled Chrome window."""
    try:
        st.session_state.stop_event.clear()
        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized") # Start maximized for better view
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        driver.get("https://poki.com/en/g/subway-surfers")
        st.session_state.driver = driver
        # Keep the thread alive until stopped
        while not st.session_state.stop_event.is_set():
            time.sleep(1)
    except Exception as e:
        st.error(f"Failed to launch browser: {e}")
    finally:
        if st.session_state.driver:
            st.session_state.driver.quit()
            st.session_state.driver = None

def gesture_control_thread(frame_queue):
    """Captures webcam feed, detects hand gestures, and adds frames to a queue."""
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        st.error("Cannot open webcam.")
        return

    cap.set(cv.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv.CAP_PROP_FRAME_HEIGHT, 480)
    last_action_time = 0
    action_cooldown = 0.4 # Cooldown in seconds to prevent spamming actions

    while not st.session_state.stop_event.is_set():
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.flip(frame, 1)
        img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(img_rgb)
        finger_count = 0

        if results.multi_hand_landmarks:
            hand_landmarks = results.multi_hand_landmarks[0]
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # A more robust finger counting logic
            finger_tips = [8, 12, 16, 20]
            thumb_tip = 4
            fingers_up = []

            # Check for 4 fingers (index, middle, ring, pinky)
            for tip_idx in finger_tips:
                if hand_landmarks.landmark[tip_idx].y < hand_landmarks.landmark[tip_idx - 2].y:
                    fingers_up.append(1)
                else:
                    fingers_up.append(0)
            finger_count = sum(fingers_up)

            # Special check for thumb (based on x-coordinate relative to its base)
            if hand_landmarks.landmark[thumb_tip].x < hand_landmarks.landmark[thumb_tip - 1].x:
                 finger_count +=1


            # Perform action with cooldown
            current_time = time.time()
            if current_time - last_action_time > action_cooldown:
                perform_action(finger_count)
                last_action_time = current_time

        # Put the processed frame into the queue to be displayed by Streamlit
        try:
            frame_queue.put_nowait(frame)
        except queue.Full:
            pass # Skip frame if queue is full

    cap.release()

def perform_action(finger_count):
    """Maps finger count to keyboard presses."""
    actions = {1: 'up', 2: 'down', 3: 'right', 4: 'left'}
    if finger_count in actions:
        pyautogui.press(actions[finger_count])
        st.sidebar.info(f"Action: {actions[finger_count].upper()} ({finger_count} fingers)")


# --- Streamlit UI Layout ---
st.markdown('<div class="title-container"><h1>🎮 Gesture-Controlled Subway Surfers</h1></div>', unsafe_allow_html=True)
st.info("Use your hand gestures to control the game. Make sure to click on the game window first!")

col1, col2 = st.columns([2, 1])

with col1:
    st.header("Camera Feed")
    video_placeholder = st.empty()
    video_placeholder.markdown("### Press 'Start' to activate the camera.")

with col2:
    st.header("Controls")
    if st.button("🚀 Start Game & Controller", key="start_button", disabled=st.session_state.is_running):
        st.session_state.is_running = True
        st.session_state.stop_event.clear()
        st.success("Starting services... Please wait.")

        # Create a queue to share frames between threads
        frame_queue = queue.Queue(maxsize=2)

        # Start threads
        threading.Thread(target=launch_game_thread, daemon=True).start()
        threading.Thread(target=gesture_control_thread, args=(frame_queue,), daemon=True).start()

        # Update UI to show camera feed
        while st.session_state.is_running:
            try:
                frame = frame_queue.get(timeout=1)
                video_placeholder.image(frame, channels="BGR")
            except queue.Empty:
                if not st.session_state.is_running:
                    break

    if st.button("🛑 Stop Game & Controller", key="stop_button", disabled=not st.session_state.is_running):
        st.session_state.is_running = False
        st.session_state.stop_event.set()
        video_placeholder.markdown("### Services stopped.")
        st.info("All processes have been terminated.")
        # A small delay to allow threads to clean up
        time.sleep(2)
        st.rerun()

st.sidebar.header("Instructions")
st.sidebar.markdown("""
1.  **Click 'Start'**: This will open a new Chrome window with the game and activate your webcam.
2.  **Focus the Game**: **IMPORTANT!** Click inside the game window to make sure it receives the keyboard commands.
3.  **Show Your Hand**:
    * **1 Finger Up**: Jump (Up Arrow)
    * **2 Fingers Up**: Roll (Down Arrow)
    * **3 Fingers Up**: Move Right (Right Arrow)
    * **4 Fingers Up**: Move Left (Left Arrow)
4.  **Click 'Stop'**: To close the game and turn off the camera.
""")
