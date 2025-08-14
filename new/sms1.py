import cloudinary
import cloudinary.uploader
from twilio.rest import Client
import sys
import os
import random
import time
from datetime import datetime

# Cloudinary config
cloudinary.config(
    cloud_name="dazyf5ejp",
    api_key="196374664982641",
    api_secret="G5tENJKH4OlxQ8hfHF_tzWbPli8"
)

# Twilio credentials
TWILIO_ACCOUNT_SID = "AC8dd049ca15552bd6929e37023d4a0518"
TWILIO_AUTH_TOKEN = "f6151e0dc4dcd41a2ac0e3cb68257037"
TWILIO_PHONE_NUMBER = "+14782955598"
TO_PHONE_NUMBER = "+916380825972"

# Store the last generated OTP and its timestamp
last_otp = None
last_otp_time = None
OTP_VALIDITY = 300  # 5 minutes in seconds
MAX_RETRIES = 3  # Maximum number of retries for OTP generation
SMS_RETRY_DELAY = 2  # seconds between SMS retries

def generate_otp():
    """Generate a 6-digit OTP"""
    try:
        # Generate a random 6-digit number
        otp = str(random.randint(100000, 999999))
        print(f"✅ Generated OTP: {otp}")
        return otp
    except Exception as e:
        print(f"❌ Error generating OTP: {str(e)}")
        return None

def send_otp_sms(otp, phone_number):
    """Send OTP via SMS"""
    try:
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        message = client.messages.create(
            body=f"🔐 Your ATM verification OTP is: {otp}. Valid for 5 minutes. Please enter this OTP to verify your identity.",
            from_=TWILIO_PHONE_NUMBER,
            to=phone_number or TO_PHONE_NUMBER
        )
        print(f"✅ OTP Sent! Message SID: {message.sid}")
        return True
    except Exception as e:
        print(f"❌ Error sending OTP SMS: {str(e)}")
        return False

def verify_otp(entered_otp):
    """Verify if the entered OTP is valid"""
    global last_otp, last_otp_time
    
    if not last_otp or not last_otp_time:
        print("❌ No OTP has been generated yet")
        return False
    
    # Check if OTP is expired
    if (datetime.now() - last_otp_time).total_seconds() > OTP_VALIDITY:
        print("❌ OTP has expired")
        return False
    
    # Check if OTP matches
    is_valid = entered_otp == last_otp
    if is_valid:
        print("✅ OTP is valid")
    else:
        print("❌ Invalid OTP")
    return is_valid

def upload_to_cloudinary(image_path):
    """Upload image to Cloudinary and return the URL"""
    try:
        upload_result = cloudinary.uploader.upload(image_path)
        image_url = upload_result.get("secure_url")
        print(f"✅ Uploaded to Cloudinary: {image_url}")
        return image_url
    except Exception as e:
        print("❌ Cloudinary Upload Failed:", e)
        return None

def send_sms(image_path=None, phone_number=None, is_otp=False, reason="face_verification_failed"):
    global last_otp, last_otp_time
    
    try:
        if is_otp:
            # Generate OTP
            otp = generate_otp()
            if not otp:
                raise Exception("Failed to generate OTP")
            
            # Store OTP and timestamp
            last_otp = otp
            last_otp_time = datetime.now()
            
            # Send OTP via SMS
            if not send_otp_sms(otp, phone_number):
                raise Exception("Failed to send OTP SMS")
                
            return otp
        elif image_path == "multiple_people_detected":
            client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
            message = client.messages.create(
                body="⚠️ Alert! More than 2 people detected in ATM area!",
                from_=TWILIO_PHONE_NUMBER,
                to=TO_PHONE_NUMBER
            )
            print(f"✅ Alert SMS Sent! Message SID: {message.sid}")
        else:
            # Upload image to Cloudinary
            image_url = upload_to_cloudinary(image_path)
            if not image_url:
                raise Exception("Failed to upload image to Cloudinary")

            # Send SMS with image
            client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
            message = client.messages.create(
                body=f"🚨 Alert! {reason}. See attached image.",
                from_=TWILIO_PHONE_NUMBER,
                to=TO_PHONE_NUMBER,
                media_url=[image_url]
            )
            print(f"✅ Image SMS Sent! Message SID: {message.sid}")

        return None

    except Exception as e:
        print(f"❌ Error in send_sms: {str(e)}")
        return None

if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == "--otp":
            phone = sys.argv[2] if len(sys.argv) > 2 else None
            otp = send_sms(is_otp=True, phone_number=phone)
            if otp:
                print(f"Generated OTP: {otp}")
        elif sys.argv[1] == "--verify":
            if len(sys.argv) < 3:
                print("❌ OTP not provided")
                sys.exit(1)
            entered_otp = sys.argv[2]
            if verify_otp(entered_otp):
                print("✅ OTP verified successfully")
                sys.exit(0)
            else:
                print("❌ Invalid or expired OTP")
                sys.exit(1)
        else:
            reason = sys.argv[2] if len(sys.argv) > 2 else "Face verification failed"
            send_sms(sys.argv[1], reason=reason)
    else:
        print("⚠️ No arguments provided!")
