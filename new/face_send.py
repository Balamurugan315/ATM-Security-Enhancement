# image_alert.py

import cloudinary
import cloudinary.uploader
from twilio.rest import Client
import sys

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

def upload_to_cloudinary(image_path):
    try:
        upload_result = cloudinary.uploader.upload(image_path)
        return upload_result.get("secure_url")
    except Exception as e:
        print("❌ Cloudinary Upload Failed:", e)
        return None

def send_alert_sms(image_path=None, reason="face_verification_failed"):
    try:
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        if image_path == "multiple_people_detected":
            message = client.messages.create(
                body="⚠️ Alert! More than 2 people detected in ATM area!",
                from_=TWILIO_PHONE_NUMBER,
                to=TO_PHONE_NUMBER
            )
        else:
            image_url = upload_to_cloudinary(image_path)
            if not image_url:
                raise Exception("Image upload failed")
            message = client.messages.create(
                body=f"🚨 Alert! {reason}. See attached image.",
                from_=TWILIO_PHONE_NUMBER,
                to=TO_PHONE_NUMBER,
                media_url=[image_url]
            )
        print(f"✅ Alert SMS Sent! Message SID: {message.sid}")
    except Exception as e:
        print(f"❌ Error sending alert SMS: {str(e)}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        path_or_flag = sys.argv[1]
        reason = sys.argv[2] if len(sys.argv) > 2 else "face_verification_failed"
        send_alert_sms(path_or_flag, reason)
    else:
        print("⚠️ No arguments provided!") 