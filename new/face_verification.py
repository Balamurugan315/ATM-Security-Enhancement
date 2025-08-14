import cv2
import numpy as np
import face_recognition
import os
import time
import subprocess
import sys
from datetime import datetime
from ui_theme import theme, Colors

# Initialize camera
cap = cv2.VideoCapture(0)

# Set window properties
cv2.namedWindow(theme.window_name, cv2.WINDOW_NORMAL)
cv2.resizeWindow(theme.window_name, *theme.window_size)

# Load known face encodings
known_face_encodings = []
known_face_names = []

# Load known faces from the 'known_faces' directory
known_faces_dir = 'known_faces'
for filename in os.listdir(known_faces_dir):
    if filename.endswith(('.jpg', '.jpeg', '.png')):
        image_path = os.path.join(known_faces_dir, filename)
        face_image = face_recognition.load_image_file(image_path)
        face_encoding = face_recognition.face_encodings(face_image)
        if face_encoding:
            known_face_encodings.append(face_encoding[0])
            known_face_names.append(os.path.splitext(filename)[0])

# Initialize variables
face_locations = []
face_encodings = []
face_names = []
process_this_frame = True
verification_start_time = None
verification_timeout = 5  # seconds
no_face_detected = False
multiple_people_detected = False
otp_verified = False
phone_number = "+916380825972"  # Default phone number
last_alert_time = None
alert_cooldown = 10  # seconds between alerts
verification_required = False
unverified_face_image = None  # Store the unverified face image path
system_status = "System Ready"  # Current system status
status_type = "info"  # Current status type

def save_captured_image(frame, reason):
    """Save the captured frame with timestamp and reason"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"captured_{reason}_{timestamp}.jpg"
    cv2.imwrite(filename, frame)
    return filename

def send_alert(image_path=None, is_otp=False, phone_number=None, reason="Face verification failed"):
    """Send alert using the SMS script"""
    global last_alert_time
    
    current_time = time.time()
    if last_alert_time and (current_time - last_alert_time) < alert_cooldown:
        print(f"⏳ Waiting for cooldown period ({alert_cooldown} seconds)...")
        return False
        
    try:
        if is_otp:
            cmd = ["python", "sms1.py", "--otp", phone_number]
        else:
            cmd = ["python", "sms1.py", image_path, reason]
        
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        if "❌" not in result.stdout:  # Check if there were no errors
            last_alert_time = current_time
            return True
        return False
    except subprocess.CalledProcessError as e:
        print(f"❌ Error sending alert: {e}")
        return False

def send_otp_with_retry(phone_number):
    """Send OTP with retries"""
    max_attempts = 3
    for attempt in range(max_attempts):
        print(f"📱 Attempting to send OTP (Attempt {attempt + 1}/{max_attempts})...")
        if send_alert(is_otp=True, phone_number=phone_number):
            print("✅ OTP sent successfully")
            return True
        if attempt < max_attempts - 1:
            print("⏳ Waiting 3 seconds before retrying...")
            time.sleep(3)
    print("❌ Failed to send OTP after multiple attempts")
    return False

def verify_otp(entered_otp, phone_number):
    """Verify the entered OTP"""
    try:
        cmd = ["python", "sms1.py", "--verify", entered_otp, phone_number]
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return "OTP verified successfully" in result.stdout
    except subprocess.CalledProcessError:
        return False

def handle_verification_required(frame):
    """Handle the verification process when required"""
    global verification_required, otp_verified, unverified_face_image, system_status, status_type
    
    if not verification_required:
        system_status = "Verification Required"
        status_type = "warning"
        print("⚠️ Verification required! Sending OTP...")
        # Save the unverified face image
        unverified_face_image = save_captured_image(frame, "unverified_face")
        
        # Try to send OTP with retries
        if send_otp_with_retry(phone_number):
            verification_required = True
            system_status = "OTP Sent - Waiting for Verification"
            print("🔐 Please enter the OTP received on your phone (Press 'v' to verify)")
        else:
            system_status = "Verification Failed - Please Try Again"
            status_type = "danger"
            print("❌ Could not initiate verification process. Please try again.")
            return False
    else:
        # Draw verification box
        frame = theme.draw_verification_box(frame, "Press 'v' to enter OTP")
    return True

def proceed_to_transaction():
    """Handle the transition to transaction page"""
    global system_status, status_type
    system_status = "Proceeding to Transaction"
    status_type = "success"
    print("✅ Proceeding to transaction page...")
    
    # Example transaction options
    transaction_options = [
        "Withdraw Cash",
        "Check Balance",
        "Transfer Money",
        "Change PIN",
        "Exit"
    ]
    
    # Draw transaction screen
    frame = theme.draw_transaction_screen(frame, transaction_options)
    return frame

print("🚀 Starting ATM Security System...")
print("Press 'q' to quit")
print("Press 'v' to verify OTP")

while True:
    ret, frame = cap.read()
    if not ret:
        print("❌ Failed to grab frame")
        break

    # Resize frame for faster processing
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
    rgb_small_frame = small_frame[:, :, ::-1]

    if process_this_frame:
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        face_names = []
        for face_encoding in face_encodings:
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding, tolerance=0.6)
            name = "Unknown"

            if True in matches:
                first_match_index = matches.index(True)
                name = known_face_names[first_match_index]

            face_names.append(name)

    process_this_frame = not process_this_frame

    # Display results
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        is_verified = name != "Unknown"
        frame = theme.draw_face_box(frame, top, right, bottom, left, name, is_verified)

    # Handle verification logic
    if not otp_verified:
        if len(face_locations) == 0:
            if verification_start_time is None:
                verification_start_time = time.time()
                no_face_detected = True
                system_status = "No Face Detected"
                status_type = "danger"
            elif time.time() - verification_start_time >= verification_timeout and no_face_detected:
                handle_verification_required(frame)
                verification_start_time = None
                no_face_detected = False
        elif len(face_locations) > 2:
            if not multiple_people_detected:
                system_status = "Multiple People Detected"
                status_type = "danger"
                print("⚠️ Multiple people detected! Sending alert...")
                image_path = save_captured_image(frame, "multiple_people")
                if send_alert(image_path=image_path, reason="Multiple people detected in ATM area"):
                    print("✅ Alert sent with captured image")
                multiple_people_detected = True
        else:
            verification_start_time = None
            no_face_detected = False
            multiple_people_detected = False

            if "Unknown" in face_names:
                handle_verification_required(frame)
            else:
                system_status = "Face Verified"
                status_type = "success"
    else:
        # After OTP verification
        if unverified_face_image:
            system_status = "Sending Verification Image"
            status_type = "info"
            print("📸 Sending unverified face image...")
            if send_alert(image_path=unverified_face_image, reason="Unverified face image"):
                print("✅ Unverified face image sent successfully")
            unverified_face_image = None
        
        frame = proceed_to_transaction()
        otp_verified = False
        verification_required = False

    # Draw status bar and instructions
    frame = theme.draw_status_bar(frame, system_status, status_type)
    frame = theme.draw_instructions(frame, [
        "Press 'q' to quit",
        "Press 'v' to verify OTP"
    ])

    # Display the frame
    cv2.imshow(theme.window_name, frame)

    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break
    elif key == ord('v'):
        if verification_required and not otp_verified:
            entered_otp = input("Enter the OTP received: ")
            if verify_otp(entered_otp, phone_number):
                print("✅ OTP verified successfully!")
                otp_verified = True
                system_status = "OTP Verified"
                status_type = "success"
            else:
                print("❌ Invalid OTP! Please try again.")
                system_status = "Invalid OTP"
                status_type = "danger"

cap.release()
cv2.destroyAllWindows() 