# otp_handler.py

from twilio.rest import Client
import random
from datetime import datetime
import sys

# Twilio credentials
TWILIO_ACCOUNT_SID = "AC8dd049ca15552bd6929e37023d4a0518"
TWILIO_AUTH_TOKEN = "f6151e0dc4dcd41a2ac0e3cb68257037"
TWILIO_PHONE_NUMBER = "+14782955598"
TO_PHONE_NUMBER = "+916380825972"

# OTP storage
last_otp = None
last_otp_time = None
OTP_VALIDITY = 300  # 5 minutes

def generate_otp():
    """Generate a 6-digit OTP"""
    return str(random.randint(100000, 999999))

def send_otp_sms(phone_number=TO_PHONE_NUMBER):
    """Generate and send OTP via SMS"""
    try:
        # Generate new OTP
        otp = generate_otp()
        
        # Send OTP via SMS
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        message = client.messages.create(
            body=f"🔐 Your ATM verification OTP is: {otp}. Valid for 5 minutes.",
            from_=TWILIO_PHONE_NUMBER,
            to=phone_number
        )
        print(f"✅ OTP Sent! Message SID: {message.sid}")
        
        # Store OTP and timestamp
        global last_otp, last_otp_time
        last_otp = otp
        last_otp_time = datetime.now()
        
        return otp
    except Exception as e:
        print(f"❌ Error sending OTP SMS: {str(e)}")
        return None

def verify_otp(entered_otp):
    """Verify if the entered OTP is valid"""
    global last_otp, last_otp_time
    if not last_otp or not last_otp_time:
        print("❌ No OTP has been generated yet")
        return False
    if (datetime.now() - last_otp_time).total_seconds() > OTP_VALIDITY:
        print("❌ OTP has expired")
        return False
    return entered_otp == last_otp

if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == "--otp":
            phone = sys.argv[2] if len(sys.argv) > 2 else TO_PHONE_NUMBER
            otp = send_otp_sms(phone)
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
        print("⚠️ No arguments provided!") 