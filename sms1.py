from twilio.rest import Client
import sys
import os

# Twilio credentials (Replace with your actual credentials)
TWILIO_ACCOUNT_SID = "ACda77e08b5934898d0150b1db5e4de5a4"
TWILIO_AUTH_TOKEN = "c73cdd0cf61db813ba38cef657287415"
TWILIO_PHONE_NUMBER = "+17627635184"
TO_PHONE_NUMBER = "+916380825972"

# Server path where images are stored (Must be accessible online)
IMAGE_SERVER_URL = "https://05af-2409-40f4-411a-4c50-bc95-272f-63d8-4214.ngrok-free.app/uploads/"  # Modify accordingly

def send_sms(image_path):
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

    if image_path == "multiple_people_detected":
        message = client.messages.create(
            body="🚨 Alert! More than 2 people detected in ATM area!",
            from_=TWILIO_PHONE_NUMBER,
            to=TO_PHONE_NUMBER
        )
    else:
        image_url = IMAGE_SERVER_URL + os.path.basename(image_path)

        message = client.messages.create(
            body="🚨 Alert! No Mask Detected. See attached image.",
            from_=TWILIO_PHONE_NUMBER,
            to=TO_PHONE_NUMBER,
            media_url=[image_url]
        )

    print(f"✅ SMS Sent! Message SID: {message.sid}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        send_sms(sys.argv[1])
    else:
        print("⚠ No image path provided!")
