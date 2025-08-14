🛡️ Face Detection & Alert System

A comprehensive security monitoring system combining **face recognition**, **mask detection**, and **crowd monitoring** with **real-time SMS alerts** using Twilio.

---

📌 System Components

1️⃣ Face Recognition System  
- 🖼️ Training data stored in `TrainingImage/`  
- 👤 Multiple user profiles (individual directories per user)  
- 📷 Real-time face detection & matching  
- 📂 Stores unknown face captures for review  

2️⃣ User Management System  
- 📄 User details stored in `Details/Details.csv`  
- 📑 Information stored:  
  - 🆔 User ID  
  - 👤 Full Name  
  - 📱 Phone Number  
  - 💰 Initial Deposit  
- 👥 Supports multiple profiles  

3️⃣ Alert System (`sms1.py`)  
- 📲 Real-time SMS notifications via Twilio  
- 🚨 Triggers:  
  - 😷 No mask detected  
  - 👥 More than 2 people detected  
  - ❓ Unknown face detected  
- 🖼️ Image attachment for verification  

---

📂 Project Structure
```plaintext
├── Unknown_Face_Captures/    # Unrecognized faces
├── TrainingImage/            # User face training data
│   ├── 000/
│   ├── 123/
│   └── ...
├── TrainingImageLabel/       # Labeled training images
├── uploads/                  # Temporary image storage
├── Details/                  # User data
│   └── Details.csv
├── new/                      # Registration/updates
├── sms1.py                   # SMS alert script
└── last_otp.txt              # OTP storage
````

---

✨ Features

* 🔍 Face detection & recognition
* 😷 Real-time mask detection
* 👥 Crowd monitoring (>2 people)
* 📲 Instant SMS alerts via Twilio
* 📸 Image capture & storage
* 🗂️ Training image management
* 👤 User profile management
* 🔐 OTP-based verification
* 📁 Unknown face logging

---

⚙️ Prerequisites

* 🐍 Python 3.x
* 📡 Twilio account & credentials
* 📦 Python packages:

  ```bash
  pip install twilio opencv-python numpy face_recognition
  ```

---

🚀 Setup Instructions

1. Clone the repository
2. Install dependencies:

   ```bash
   pip install twilio opencv-python numpy face_recognition
   ```
3. Configure Twilio in `sms1.py`:

   * `TWILIO_ACCOUNT_SID`
   * `TWILIO_AUTH_TOKEN`
   * `TWILIO_PHONE_NUMBER`
   * `TO_PHONE_NUMBER`
4. Update `IMAGE_SERVER_URL` in `sms1.py`

---

▶️ Usage

1. Place training images in `TrainingImage/`
2. Add user details in `Details/Details.csv`
3. Run the face detection system
4. System will:

   * Detect faces
   * Check masks
   * Monitor crowd size
   * Send SMS alerts 🚨

---

🚨 Alert Triggers

* 😷 No Mask detected
* 👥 More than 2 people
* ❓ Unknown face detected

---

📊 Data Management

* 🗂️ CSV format for user data
* 📂 Images organized in directories
* 📁 Separate storage for unknown faces
* 🧹 Regular cleanup recommended

---

🔒 Security Notes

* 🛡️ Keep Twilio credentials secure
* 📷 Update training images regularly
* 📜 Monitor logs for suspicious activity
* 🔐 Protect user privacy
* 🧪 Perform regular security audits

---

🛠 Maintenance

* 🧹 Clean `Unknown_Face_Captures/` regularly
* 📷 Update training images
* 📡 Monitor Twilio usage & limits
* 🔄 Regular system health checks
* 💾 Backup user data

---

🔗 Integration Points

* Twilio API 📲
* Image server for captured images 🖼️
* Face recognition engine 👁️
* User management system 👤

---

💬 Support
📩 Create an issue in the repository for help.


