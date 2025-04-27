import streamlit as st
from ultralytics import YOLO
import cv2
import tempfile
import numpy as np
import pandas as pd
from datetime import datetime
import requests
import os
from PIL import Image
import logging
import mysql.connector

# Setup logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger()

# Load YOLO model
model = YOLO(r"D:\Employee Monitoring YOLO V11\runs\detect\train5\weights\best.pt")

# Connect to MySQL database
def get_db_connection():
#     conn = mysql.connector.connect(
#     host="fdb1030.awardspace.net",
#     user="4625513_employeemonitoring",
#     password="(The password for 4625513_employeemonitoring)",
#     database="4625513_employeemonitoring"
# )
    return mysql.connector.connect(
        host="localhost",  # Replace with your host
        user="root",       # Replace with your MySQL username
        password="123asd!@#", # Replace with your MySQL password
        database="employee_monitoring"
    )

# Streamlit page settings
st.set_page_config(page_title="Employee Monitoring System", layout="wide")
st.markdown("<h1 style='text-align: center; color: #2E86AB;'>👨‍💻 Employee Monitoring System</h1>", unsafe_allow_html=True)
st.sidebar.title("🛠️ Options")

# Sidebar - Inputs
st.sidebar.subheader("📥 Input Source")
uploaded_file = st.sidebar.file_uploader("Upload Video or Image", type=["mp4", "avi", "mov", "jpg", "jpeg", "png"])
image_url = st.sidebar.text_input("Or Enter an Image URL")
frame_skip = st.sidebar.slider("Frame Skip Rate", 1, 10, 1)

# Sidebar - Model Settings
st.sidebar.subheader("⚙️ Model Settings")
confidence_thresh = st.sidebar.slider("Confidence Threshold", 0.0, 1.0, 0.5)
overlap_thresh = st.sidebar.slider("Overlap Threshold (IoU)", 0.0, 1.0, 0.5)
dynamic_threshold = st.sidebar.checkbox("Enable Dynamic Confidence")

# Class labels
class_labels = [
    'Arriving', 'Closing_Door', 'Conversation', 'Drinking_Water', 'Eating', 'Greeting', 'Idle', 'Leaving',
    'Person_Writing_on_paper', 'Sitting_Down', 'Sleeping', 'Sneezing', 'Standing', 'Working',
    'falling_down', 'opening_door', 'standing_up_employee', 'using_phone'
]
class_counts = {label: 0 for label in class_labels}
action_logs = []
action_frames = {}

# Minimum frames for detecting valid actions
MIN_FRAMES_THRESHOLD = 5
ABNORMAL_IDLE_THRESHOLD = 300  # Seconds (5 minutes of idle time)
ACTIVE_TIME_THRESH = 1800  # Active time threshold (30 minutes)

# Helper functions
def adjust_confidence_threshold():
    return 0.3 if dynamic_threshold else confidence_thresh
def process_frame(frame, frame_counter):
    """Detect and annotate frame"""
    results = model(frame, conf=adjust_confidence_threshold(), iou=overlap_thresh)
    detected_classes = []
    
    # Processing each detection result
    for result in results:
        for box in result.boxes:
            cls_id = int(box.cls[0])
            confidence = float(box.conf[0])
            if 0 <= cls_id < len(class_labels):
                label = class_labels[cls_id]
                detected_classes.append(label)
                class_counts[label] += 1

                if label not in action_frames:
                    action_frames[label] = {'start_frame': frame.copy(), 'end_frame': None, 'frame_count': 1, 'start_time': None, 'end_time': None}
                else:
                    action_frames[label]['end_frame'] = frame.copy()
                    action_frames[label]['frame_count'] += 1
                    action_frames[label]['end_time'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                if action_frames[label]['start_time'] is None:
                    action_frames[label]['start_time'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                bbox = box.xyxy[0].cpu().numpy()
                x1, y1, x2, y2 = map(int, bbox)
                # Using bright yellow for rectangle and black for text
                color = tuple(np.random.randint(0, 255, 3).tolist())
                cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
                cv2.putText(frame, f"{label} ({confidence:.2f})", (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                day_of_week = datetime.now().strftime("%A")  # Get the day of the week
                action_logs.append({
                    "Timestamp": timestamp,
                    "Label": label,
                    "Confidence": confidence,
                    "Coordinates": f"({x1}, {y1}, {x2}, {y2})",
                    "Frame": frame_counter,
                    "Day_of_Week": day_of_week
                })
                
          

    logger.info(f"Processed frame {frame_counter} - Detected classes: {detected_classes}")
    return frame, detected_classes



# Helper function to calculate time difference
def calculate_time_difference(start_time, end_time):
    """Calculate the time difference in seconds"""
    start_time_obj = datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S")
    end_time_obj = datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S")
    return (end_time_obj - start_time_obj).total_seconds()

# Helper function to calculate productivity metrics
def calculate_productivity_metrics():
    total_active_time = 0
    total_idle_time = 0
    abnormal_idle_time = []
    increasing_productivity_time = 0
    decreasing_productivity_time = 0

    # Define labels associated with increasing and decreasing productivity
    increasing_productivity_labels = ['Working', 'Sitting_Down', 'Person_Writing_on_paper']
    decreasing_productivity_labels = ['Idle', 'Sleeping', 'Conversation', 'Drinking_Water', 'Eating', 'Sneezing', 'falling_down']

    # Calculate active vs idle time, and classify actions into increasing or decreasing productivity
    for label, frames in action_frames.items():
        if frames['frame_count'] >= MIN_FRAMES_THRESHOLD:
            total_time = calculate_time_difference(frames['start_time'], frames['end_time'])

            # Classify based on labels
            if label in increasing_productivity_labels:
                increasing_productivity_time += total_time
            elif label in decreasing_productivity_labels:
                decreasing_productivity_time += total_time
            elif label in ['Idle', 'Sleeping']:
                total_idle_time += total_time
                if total_time > ABNORMAL_IDLE_THRESHOLD:
                    abnormal_idle_time.append({label: total_time})
            else:
                total_active_time += total_time

    return total_active_time, total_idle_time, abnormal_idle_time, increasing_productivity_time, decreasing_productivity_time


   
# Insert filtered logs into the database after filtering the action frames
def save_filtered_logs_to_db():
    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        query = """INSERT INTO action_logs (timestamp_start, timestamp_end, label, frames_detected, total_time_seconds, day_of_week)
                   VALUES (%s, %s, %s, %s, %s, %s)"""

        for label, frames in action_frames.items():
            if frames['frame_count'] >= MIN_FRAMES_THRESHOLD:
                total_time = calculate_time_difference(frames['start_time'], frames['end_time'])
                
                # Get the day of the week for start time
                start_time_obj = datetime.strptime(frames['start_time'], "%Y-%m-%d %H:%M:%S")
                day_of_week = start_time_obj.strftime("%A")  # Example: Monday, Tuesday, etc.

                cursor.execute(query, (
                    frames['start_time'], 
                    frames['end_time'], 
                    label, 
                    frames['frame_count'], 
                    total_time,
                    day_of_week  # Save the day here
                ))

        connection.commit()
        cursor.close()
        connection.close()
        logger.info("Filtered logs with day of week successfully inserted into the database.")

    except mysql.connector.Error as err:
        logger.error(f"Error inserting filtered logs into database: {err}")


# Handle input
if uploaded_file or image_url:
    if image_url:
        try:
            response = requests.get(image_url)
            img_array = np.asarray(bytearray(response.content), dtype=np.uint8)
            frame = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
            cap = [frame]
        except Exception as e:
            logger.error(f"Error loading image: {e}")
            st.error(f"Error loading image: {e}")
            cap = None
    elif uploaded_file:
        tfile = tempfile.NamedTemporaryFile(delete=False)
        tfile.write(uploaded_file.read())
        cap = cv2.VideoCapture(tfile.name)

    stframe = st.empty()
    st.markdown("### 🎥 Detection Preview")
    frame_counter = 0

    with st.spinner("Processing..."):
        while (isinstance(cap, cv2.VideoCapture) and cap.isOpened()) or isinstance(cap, list):
            ret, frame = (cap.read() if isinstance(cap, cv2.VideoCapture) else (True, cap[0]))
            if not ret:
                break

            frame_counter += 1
            if frame_counter % frame_skip != 0:
                continue

            frame, detected_classes = process_frame(frame, frame_counter)
            
            # Resize frame for larger display (1200x800)
            resized_frame = cv2.resize(frame, (600, 300))
            stframe.image(cv2.cvtColor(resized_frame, cv2.COLOR_BGR2RGBA), channels="RGB", use_column_width=True)

            if isinstance(cap, list):
                break

        if isinstance(cap, cv2.VideoCapture):
            cap.release()

    # Sidebar - Summary
    st.sidebar.subheader("📊 Detection Summary")
    for label, count in class_counts.items():
        st.sidebar.write(f"{label}: {count}")

    # Logs
    # Logs

    
    st.markdown("### 📑 Action Logs")
    if action_logs:
        action_logs_filtered = []
        for label, frames in action_frames.items():
            if frames['frame_count'] >= MIN_FRAMES_THRESHOLD:
                total_time = calculate_time_difference(frames['start_time'], frames['end_time'])
                action_logs_filtered.append({
                    "Timestamp Start": frames['start_time'],
                    "Timestamp End": frames['end_time'],
                    "Label": label,
                    "Frames Detected": frames['frame_count'],
                    "Total Time (seconds)": total_time,
                })

                # Insert filtered logs into the database
                
# Call the function after processing frames
        save_filtered_logs_to_db()

        logs_df = pd.DataFrame(action_logs_filtered)
        st.dataframe(logs_df)
        
        # Log the data to a CSV file for external analysis
        csv = logs_df.to_csv(index=False)
        st.download_button("📥 Download Logs", csv, "action_logs.csv", "text/csv")

        total_active_time, total_idle_time, abnormal_idle_time, increasing_productivity_time, decreasing_productivity_time = calculate_productivity_metrics()

        st.markdown("### ⏱️ Productivity Metrics")
        st.write(f"Total Active Time: {total_active_time / 60:.2f} minutes")
        st.write(f"Total Idle Time: {total_idle_time / 60:.2f} minutes")
        st.write(f"Time Contributing to Increasing Productivity: {increasing_productivity_time / 60:.2f} minutes")
        st.write(f"Time Contributing to Decreasing Productivity: {decreasing_productivity_time / 60:.2f} minutes")
        
        if abnormal_idle_time:
            st.markdown("⚠️ Abnormal Idle Time Detected")
            for idle in abnormal_idle_time:
                st.write(idle)

else:
    st.info("👈 Upload a video/image or paste an image URL to start monitoring.")
