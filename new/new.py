import tkinter as tk
from tkinter import Message, Text
import cv2 
import os
import tkinter.ttk as ttk
import tkinter.font as font
import numpy as np
from PIL import Image, ImageTk
import csv
import json
import pandas as pd
import shutil
import time
import subprocess
from tkinter import messagebox
import pygame
from tensorflow.keras.models import load_model
from datetime import datetime
from ui_theme import theme, Colors
from otp_verify import send_otp_sms, verify_otp
from face_send import send_alert_sms


class ATMApp:
    def __init__(self, master):
        self.root = root
        self.root.title(theme.window_name)
        self.root.geometry("1000x600+300+100")
        self.root.configure(bg=Colors.DARK_GRAY_TK)
        
        # UI Style Definitions
        self.title_font = ("Helvetica", 24, "bold")
        self.header_font = ("Helvetica", 18, "bold")
        self.label_font = ("Helvetica", 12)
        self.entry_font = ("Helvetica", 12)
        self.button_font = ("Helvetica", 12, "bold")
        self.notification_font = ('Helvetica', 10, 'italic')

        # Updated color scheme to match new theme
        self.APP_BG = Colors.DARK_GRAY_TK
        self.FRAME_BG = Colors.WHITE_TK
        self.TEXT_COLOR = Colors.BLACK_TK
        self.TITLE_COLOR = Colors.PRIMARY_TK
        self.BUTTON_PRIMARY_BG = Colors.PRIMARY_TK
        self.BUTTON_PRIMARY_FG = Colors.WHITE_TK
        self.BUTTON_SECONDARY_BG = Colors.GRAY_TK
        self.BUTTON_SECONDARY_FG = Colors.WHITE_TK
        self.NOTIFICATION_BG = Colors.LIGHT_BLUE_TK
        self.NOTIFICATION_FG = Colors.BLACK_TK
        self.ENTRY_BG = Colors.WHITE_TK
        self.ENTRY_FG = Colors.BLACK_TK

        self.widget_padding_x = 10
        self.widget_padding_y = 5
        self.frame_padding_x = 20
        self.frame_padding_y = 20
        
        # Create main container with new theme
        self.main_container = tk.Frame(self.root, bg=self.APP_BG)
        self.main_container.pack(fill='both', expand=True)
        
        # Create frames with new theme
        self.welcome_frame = tk.Frame(self.main_container, bg=self.FRAME_BG)
        self.login_frame = tk.Frame(self.main_container, bg=self.FRAME_BG)
        self.register_frame = tk.Frame(self.main_container, bg=self.FRAME_BG)
        
        # Initialize all frames
        self.setup_welcome_frame()
        self.setup_login_frame()
        self.setup_register_frame()
        
        # Show welcome frame initially
        self.show_frame(self.welcome_frame)
        
        # Load data
        self.data = self.loading_data()

    def show_frame(self, frame):
        # Hide all frames
        for f in [self.welcome_frame, self.login_frame, self.register_frame]:
            f.pack_forget()
        # Show the requested frame
        frame.pack(fill='both', expand=True)
    
    def loading_data(self):
        file = open('new/data.txt', 'r', encoding='utf-8')
        data = json.load(file)
        file.close()
        return data
    
    def saving_data(self, data):
        file = open('new/data.txt', 'w', encoding='utf-8')
        json.dump(data, file, ensure_ascii=False)
        file.close()
    
    def setup_welcome_frame(self):
        self.welcome_frame.configure(bg=self.FRAME_BG)
        # Create left frame for image
        left_frame = tk.Frame(self.welcome_frame, bg=self.FRAME_BG)
        left_frame.grid(row=0, column=0, padx=(self.frame_padding_x, self.widget_padding_x), pady=self.frame_padding_y, sticky="nsew")
        
        # Load and display the image
        image = Image.open("new/Atm.jpg")
        self.atm_image = ImageTk.PhotoImage(image)
        image_label = tk.Label(left_frame, image=self.atm_image, bg=self.FRAME_BG)
        image_label.image = self.atm_image
        image_label.pack(padx=self.widget_padding_x, pady=self.widget_padding_y)
        
        # Create right frame for buttons with new theme
        right_frame = tk.Frame(self.welcome_frame, bg=self.FRAME_BG)
        right_frame.grid(row=0, column=1, padx=(self.widget_padding_x, self.frame_padding_x), pady=self.frame_padding_y, sticky="nsew")
        
        self.welcome_frame.grid_columnconfigure(0, weight=1)
        self.welcome_frame.grid_columnconfigure(1, weight=1)

        welcome_label = tk.Label(right_frame, text="Welcome to ATM System", font=self.title_font, fg=self.TITLE_COLOR, bg=self.FRAME_BG)
        welcome_label.pack(padx=self.widget_padding_x, pady=(self.widget_padding_y * 4, self.widget_padding_y * 2), anchor="center")
        
        # Updated button styling
        login_button = tk.Button(right_frame, text="Login", width=20, font=self.button_font, 
                               bg=self.BUTTON_PRIMARY_BG, fg=self.BUTTON_PRIMARY_FG, relief=tk.FLAT,
                               pady=self.widget_padding_y, command=lambda: self.show_frame(self.login_frame))
        login_button.pack(pady=self.widget_padding_y, padx=self.widget_padding_x, anchor="center")
        
        register_button = tk.Button(right_frame, text="Register", width=20, font=self.button_font, 
                                  bg=self.BUTTON_SECONDARY_BG, fg=self.BUTTON_SECONDARY_FG, relief=tk.FLAT,
                                  pady=self.widget_padding_y, command=lambda: self.show_frame(self.register_frame))
        register_button.pack(pady=self.widget_padding_y, padx=self.widget_padding_x, anchor="center")
    
    def setup_login_frame(self):
        self.login_frame.configure(bg=self.FRAME_BG)
        # Create left frame for image
        left_frame = tk.Frame(self.login_frame, bg=self.FRAME_BG)
        left_frame.grid(row=0, column=0, padx=(self.frame_padding_x, self.widget_padding_x), pady=self.frame_padding_y, sticky="nsew")
        
        image_label = tk.Label(left_frame, image=self.atm_image, bg=self.FRAME_BG)
        image_label.image = self.atm_image
        image_label.pack(padx=self.widget_padding_x, pady=self.widget_padding_y)
        
        # Create right frame for login form with new theme
        right_frame = tk.Frame(self.login_frame, bg=self.FRAME_BG)
        right_frame.grid(row=0, column=1, padx=(self.widget_padding_x, self.frame_padding_x), pady=self.frame_padding_y, sticky="nsew")

        self.login_frame.grid_columnconfigure(0, weight=1)
        self.login_frame.grid_columnconfigure(1, weight=1)

        form_container = tk.Frame(right_frame, bg=self.FRAME_BG)
        form_container.pack(pady=self.widget_padding_y * 2, padx=self.widget_padding_x, expand=True)
        
        welcome_label = tk.Label(form_container, text="Login to ATM System", font=self.header_font, fg=self.TITLE_COLOR, bg=self.FRAME_BG)
        welcome_label.pack(pady=(self.widget_padding_y * 2, self.widget_padding_y * 2))
        
        # Updated form styling
        username_label = tk.Label(form_container, text="Card Number:", font=self.label_font, fg=self.TEXT_COLOR, bg=self.FRAME_BG)
        username_label.pack(anchor="w", padx=self.widget_padding_x)
        self.login_card_entry = tk.Entry(form_container, font=self.entry_font, width=35, bg=self.ENTRY_BG, fg=self.ENTRY_FG, relief=tk.SOLID, bd=1)
        self.login_card_entry.pack(pady=self.widget_padding_y, padx=self.widget_padding_x, ipady=4)
        
        password_label = tk.Label(form_container, text="Pin:", font=self.label_font, fg=self.TEXT_COLOR, bg=self.FRAME_BG)
        password_label.pack(anchor="w", padx=self.widget_padding_x)
        self.login_pin_entry = tk.Entry(form_container, font=self.entry_font, width=35, show="*", bg=self.ENTRY_BG, fg=self.ENTRY_FG, relief=tk.SOLID, bd=1)
        self.login_pin_entry.pack(pady=self.widget_padding_y, padx=self.widget_padding_x, ipady=4)
        
        # Restore both notification and message labels
        self.login_notification = tk.Label(form_container, text="", bg=self.NOTIFICATION_BG, fg=self.NOTIFICATION_FG, 
                                         width=35, height=1, font=self.notification_font, wraplength=300)
        self.login_notification.pack(pady=self.widget_padding_y, padx=self.widget_padding_x)
        
        self.login_message = tk.Label(form_container, text="", bg=self.NOTIFICATION_BG, fg=self.NOTIFICATION_FG, 
                                    width=35, height=1, font=self.notification_font, wraplength=300)
        self.login_message.pack(pady=self.widget_padding_y, padx=self.widget_padding_x)
        
        # Updated button styling
        buttons_frame = tk.Frame(form_container, bg=self.FRAME_BG)
        buttons_frame.pack(pady=(self.widget_padding_y * 2, 0))

        login_button = tk.Button(buttons_frame, text="Login", width=15, font=self.button_font, 
                               bg=self.BUTTON_PRIMARY_BG, fg=self.BUTTON_PRIMARY_FG, relief=tk.FLAT,
                               pady=self.widget_padding_y, command=self.login_submit)
        login_button.pack(side=tk.LEFT, padx=self.widget_padding_y)
        
        back_button = tk.Button(buttons_frame, text="Back", width=15, font=self.button_font, 
                              bg=self.BUTTON_SECONDARY_BG, fg=self.BUTTON_SECONDARY_FG, relief=tk.FLAT,
                              pady=self.widget_padding_y, command=lambda: self.show_frame(self.welcome_frame))
        back_button.pack(side=tk.LEFT, padx=self.widget_padding_y)
    
    def setup_register_frame(self):
        self.register_frame.configure(bg=self.FRAME_BG)
        # Create left frame for image
        left_frame = tk.Frame(self.register_frame, bg=self.FRAME_BG)
        left_frame.grid(row=0, column=0, padx=(self.frame_padding_x, self.widget_padding_x), pady=self.frame_padding_y, sticky="nsew")
        
        image_label = tk.Label(left_frame, image=self.atm_image, bg=self.FRAME_BG)
        image_label.image = self.atm_image
        image_label.pack(padx=self.widget_padding_x, pady=self.widget_padding_y)
        
        # Create right frame for registration form with new theme
        right_frame = tk.Frame(self.register_frame, bg=self.FRAME_BG)
        right_frame.grid(row=0, column=1, padx=(self.widget_padding_x, self.frame_padding_x), pady=self.frame_padding_y, sticky="nsew")

        self.register_frame.grid_columnconfigure(0, weight=1)
        self.register_frame.grid_columnconfigure(1, weight=1)

        form_container = tk.Frame(right_frame, bg=self.FRAME_BG)
        form_container.pack(pady=self.widget_padding_y, padx=self.widget_padding_x, expand=True)

        reg_title = tk.Label(form_container, text="Create New Account", font=self.header_font, fg=self.TITLE_COLOR, bg=self.FRAME_BG)
        reg_title.pack(pady=(self.widget_padding_y, self.widget_padding_y * 2))
        
        # Updated registration form fields
        fields = [
            ("Name:", "name_entry", False),
            ("Mobile:", "mobile_entry", False),
            ("Account No:", "Acc_entry", False),
            ("Initial Deposit:", "deposit_entry", False),
            ("Card Number:", "reg_card_entry", False),
            ("Pin:", "reg_pin_entry", True)
        ]

        for label_text, entry_attr, is_secret in fields:
            row_frame = tk.Frame(form_container, bg=self.FRAME_BG)
            row_frame.pack(fill=tk.X, pady=2)

            lbl = tk.Label(row_frame, text=label_text, font=self.label_font, fg=self.TEXT_COLOR, bg=self.FRAME_BG, width=15, anchor="w")
            lbl.pack(side=tk.LEFT, padx=(0, self.widget_padding_x))
            
            entry_val = tk.Entry(row_frame, font=self.entry_font, width=30, bg=self.ENTRY_BG, fg=self.ENTRY_FG, relief=tk.SOLID, bd=1)
            if is_secret:
                entry_val.config(show="*")
            setattr(self, entry_attr, entry_val)
            entry_val.pack(side=tk.LEFT, expand=True, fill=tk.X, ipady=4)

        self.reg_notification = tk.Label(form_container, text="", bg=self.NOTIFICATION_BG, fg=self.NOTIFICATION_FG, 
                                       width=45, height=1, font=self.notification_font, wraplength=350)
        self.reg_notification.pack(pady=self.widget_padding_y)
        
        self.reg_message = tk.Label(form_container, text="", bg=self.NOTIFICATION_BG, fg=self.NOTIFICATION_FG, 
                                  width=45, height=1, font=self.notification_font, wraplength=350)
        self.reg_message.pack(pady=self.widget_padding_y)
        
        # Updated registration buttons
        buttons_frame = tk.Frame(form_container, bg=self.FRAME_BG)
        buttons_frame.pack(pady=(self.widget_padding_y * 2, 0))

        submit_button = tk.Button(buttons_frame, text="Submit", width=15, font=self.button_font, 
                                bg=self.BUTTON_PRIMARY_BG, fg=self.BUTTON_PRIMARY_FG, relief=tk.FLAT,
                                pady=self.widget_padding_y, command=self.reg_submit)
        submit_button.pack(side=tk.LEFT, padx=self.widget_padding_y)
        
        back_button = tk.Button(buttons_frame, text="Back", width=15, font=self.button_font, 
                              bg=self.BUTTON_SECONDARY_BG, fg=self.BUTTON_SECONDARY_FG, relief=tk.FLAT,
                              pady=self.widget_padding_y, command=lambda: self.show_frame(self.welcome_frame))
        back_button.pack(side=tk.LEFT, padx=self.widget_padding_y)

    def reg_submit(self):
        Userid = self.reg_card_entry.get()
        self.reg_message.pack_forget()
        if Userid.isdigit():
            if self.TakeImages() == 1:
                if self.TrainImages():
                    user_data = {
                        "password": self.reg_pin_entry.get(),
                        "phone_number": self.mobile_entry.get(),
                    }
                    self.data[Userid] = user_data
                    self.saving_data(self.data)
                    # Show registration success popup
                    messagebox.showinfo("Registration", "Registration Successful!")
                else:
                    pass
        else:
            self.reg_message.config(text="User Id should contain numbers only!!!")
            self.reg_message.pack()
        self.reg_clear()
        print(self.data)


    def TakeImages(self):
        Id = self.reg_card_entry.get()
        name = self.reg_pin_entry.get()
        phone = self.mobile_entry.get()
        initial_deposit = float(self.deposit_entry.get())
        ret = 0

        if Id not in self.data:
            # Load the trained mask detection model
            model = load_model("new/face_mask_detector.h5", compile=True)

            # Load OpenCV's Deep Learning face detector
            prototxt_path = "new/deploy.prototxt.txt"
            model_path = "new/res10_300x300_ssd_iter_140000.caffemodel"
            net = cv2.dnn.readNetFromCaffe(prototxt_path, model_path)

            # Initialize pygame for playing sound
            pygame.mixer.init()
            sound_file = "new/alert_more_than_2.mp3"

            # Create folder path using the account number
            base_folder = "TrainingImage"
            user_folder = os.path.join(base_folder, Id)
            os.makedirs(user_folder, exist_ok=True)

            cam = cv2.VideoCapture(0)
            harcascadePath = "new/haarcascade_frontalface_default.xml"
            detector = cv2.CascadeClassifier(harcascadePath)
            sampleNum = 0

            # Start mask detection and image capturing
            no_mask_captured = False

            while True:
                ret, img = cam.read()
                if not ret:
                    break

                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                faces = detector.detectMultiScale(gray, 1.3, 5)

                if len(faces) > 2:
                    print("⚠ More than 2 people detected! Exiting...")
                    pygame.mixer.music.load(sound_file)
                    pygame.mixer.music.play()
                    pygame.time.delay(2000)
                    print("Try Again")
                    exit(0);

                for (x, y, w, h) in faces:
                    if x < 0 or y < 0 or w <= 0 or h <= 0:
                        continue

                    face_roi = gray[y:y + h, x:x + w]
                    face_rgb = cv2.cvtColor(face_roi, cv2.COLOR_GRAY2RGB)
                    face_resized = cv2.resize(face_rgb, (128, 128)).astype("float32") / 255.0
                    face_resized = np.expand_dims(face_resized, axis=0)

                    prediction = model.predict(face_resized)[0][0]
                    confidence = round(float(prediction) * 100, 2)

                    if prediction >= 0.5:  # No Mask
                        label = f"No Mask ({confidence}%)"
                        color = (0, 0, 255)

                        filename = os.path.join(user_folder, f"{name}.{Id}.{sampleNum}.jpg")
                        cv2.imwrite(filename, face_roi)
                        print(f"Saved face image: {filename}")
                        sampleNum += 1

                        if sampleNum >= 100:
                            no_mask_captured = True
                            break
                    else:
                        label = f"Mask ({100 - confidence}%)"
                        color = (0, 255, 0)

                    cv2.rectangle(img, (x, y), (x + w, y + h), color, 2)
                    cv2.putText(img, label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)

                if no_mask_captured:
                    break

                cv2.imshow("Face Registration", img)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

            cam.release()
            cv2.destroyAllWindows()

            if sampleNum > 0:
                res = f"Images Saved for ID: {Id} Name: {name}"
                headers = ["Id", "Name", "Phone", "Initial_Deposit"]

                file_exists = os.path.exists('Details/Details.csv')
                with open('Details/Details.csv', 'a+', newline='') as csvFile:
                    writer = csv.writer(csvFile)
                    if not file_exists:
                        writer.writerow(headers)
                    writer.writerow([Id, name, phone, initial_deposit])

                self.reg_message.configure(text=res)
                ret = 1
            else:
                self.reg_message.configure(text="No images were captured. Please try again.")
        else:
            self.reg_message.configure(text="Username Already Exists...Try another one!!!")
        return ret
    

    def TrainImages(self):
        recognizer = cv2.face_LBPHFaceRecognizer.create()
        harcascadePath = "new/haarcascade_frontalface_default.xml"
        detector = cv2.CascadeClassifier(harcascadePath)

        faces, Ids = [], []

        # Traverse all account subfolders under 'TrainingImage'
        base_path = "TrainingImage"
        for root, dirs, files in os.walk(base_path):
            for file in files:
                if file.endswith(".jpg") or file.endswith(".png"):
                    path = os.path.join(root, file)
                    img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
                    if img is None:
                        continue
                    # Use Haar Cascade to detect face again (for robustness)
                    faces_rects = detector.detectMultiScale(img)
                    for (x, y, w, h) in faces_rects:
                        faces.append(img[y:y + h, x:x + w])
                        # Extract ID from the filename (e.g., "name.ID.0.jpg")
                        try:
                            filename_parts = file.split(".")
                            if len(filename_parts) >= 2:
                                Ids.append(int(filename_parts[1]))
                        except:
                            continue

        if faces and Ids:
            recognizer.train(faces, np.array(Ids))
            os.makedirs("TrainingImageLabel", exist_ok=True)
            recognizer.save("TrainingImageLabel/Trainner.yml")
            self.reg_message.configure(text="Registration Successful")
            return True
        else:
            self.reg_message.configure(text="No faces found for training.")
            return False
    def reg_clear(self):
        self.reg_card_entry.delete(0, 'end')
        self.reg_pin_entry.delete(0, 'end')
        self.name_entry.delete(0, 'end')
        self.mobile_entry.delete(0, 'end')
        self.Acc_entry.delete(0, 'end')
        self.deposit_entry.delete(0, 'end')
    def login_submit(self):
        username = self.login_card_entry.get()
        password = self.login_pin_entry.get()
        self.login_message.pack_forget()
        if username in self.data:
            user_data = self.data[username]
            if user_data["password"] == password:
                phone_number = user_data.get("phone_number", "Phone Number Not Provided")
                self.TrackImages(username)
            else:
                self.login_message.config(text="Id and Password do not match")
                self.login_message.pack()
        else:
            self.login_message.config(text="Entered Id does not exist")
            self.login_message.pack()
        self.login_clear()


    def TrackImages(self, UserId):
        recognizer = cv2.face.LBPHFaceRecognizer_create()
        recognizer.read("TrainingImageLabel/Trainner.yml")
        faceCascade = cv2.CascadeClassifier("new/haarcascade_frontalface_default.xml")
        mask_model = load_model("new/face_mask_detector.h5", compile=True)

        cam = cv2.VideoCapture(0)
        font = cv2.FONT_HERSHEY_SIMPLEX
        run_count = 0
        face_verified = False
        start_time = time.time()
        no_face_time = None

        # Create folder for unknown captures
        unknown_folder = "Unknown_Face_Captures"
        os.makedirs(unknown_folder, exist_ok=True)

        while True:
            ret, img = cam.read()
            if not ret:
                self.login_message.configure(text="Camera error. Please try again.")
                break

            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = faceCascade.detectMultiScale(gray, 1.1, 4)

            current_time = time.time()
            elapsed_time = current_time - start_time
            pygame.mixer.init()
            sound_file = "new/alert_more_than_2.mp3"

            if len(faces) > 2:
                print("⚠ More than 2 people detected! Exiting...")
                pygame.mixer.music.load(sound_file)
                pygame.mixer.music.play()
                pygame.time.delay(2000)  # Wait 2 seconds before exiting
                exit(0)
            elif len(faces) == 0:
                if no_face_time is None:
                    no_face_time = current_time
                elif current_time - no_face_time >= 5:
                    self.login_message.configure(text="No face detected for 5 seconds. Sending OTP...")
                    # Save the last frame before sending OTP
                    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                    filename = os.path.join(unknown_folder, f"NoFace_{timestamp}.jpg")
                    cv2.imwrite(filename, img)
                    # Send the image
                    send_alert_sms(filename, "No face detected")
                    cam.release()
                    cv2.destroyAllWindows()
                    self.otp_verification(UserId, self.data)
                    return
            else:
                no_face_time = None  # Reset no face timer when face is detected

            if elapsed_time >= 5 and not face_verified:
                self.login_message.configure(text="Face verification timeout. Sending OTP...")
                # Save the last frame before sending OTP
                timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                filename = os.path.join(unknown_folder, f"Timeout_{timestamp}.jpg")
                cv2.imwrite(filename, img)
                # Send the image
                send_alert_sms(filename, "Face verification timeout")
                cam.release()
                cv2.destroyAllWindows()
                self.otp_verification(UserId, self.data)
                return

            for (x, y, w, h) in faces:
                face_roi_color = img[y:y+h, x:x+w]
                face_rgb = cv2.cvtColor(face_roi_color, cv2.COLOR_BGR2RGB)
                face_resized = cv2.resize(face_rgb, (128, 128)).astype("float32") / 255.0
                face_resized = np.expand_dims(face_resized, axis=0)

                prediction = mask_model.predict(face_resized)[0][0]
                if prediction < 0.5:
                    self.login_message.configure(text="Please remove mask before verification.")
                    cv2.putText(img, "Mask Detected", (x, y - 10), font, 0.8, (0, 0, 255), 2)
                    cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)
                else:
                    face_roi_gray = gray[y:y+h, x:x+w]
                    face_roi_gray = cv2.resize(face_roi_gray, (128, 128))

                    Id, conf = recognizer.predict(face_roi_gray)
                    print(f"ID: {Id}, Confidence: {conf}")

                    if conf < 85:
                        if str(Id) == UserId:
                            face_verified = True
                            self.login_message.configure(text="Face verified successfully!")
                            cam.release()
                            cv2.destroyAllWindows()
                            # Show login success popup
                            messagebox.showinfo("Login", "Login Successful!")
                            self.perform_transaction(UserId)
                            return
                        else:
                            self.login_message.configure(text="Face mismatch. Please try again.")
                            # Save image and send alert
                            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                            filename = os.path.join(unknown_folder, f"Mismatch_{timestamp}.jpg")
                            cv2.imwrite(filename, img)
                            print(f"Face mismatch captured: {filename}")
                            # Send the image
                            send_alert_sms(filename, "Face mismatch detected")
                            time.sleep(2)  # Optional wait before breaking
                            break
                    else:
                        self.login_message.configure(text=f"Face not recognized. Confidence: {conf}")

                    cv2.putText(img, f"ID: {Id} Conf: {conf:.2f}", (x, y - 10), font, 0.7, (0, 255, 0), 2)
                    cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)

            run_count += 1
            cv2.imshow("Face Verification", img)
            if cv2.waitKey(1) & 0xFF == ord('q') or run_count >= 100 or face_verified:
                break

        cam.release()
        cv2.destroyAllWindows()

        if not face_verified:
            self.login_message.configure(text="Face verification failed or mask not removed.")
            # Save the last frame before sending OTP
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            filename = os.path.join(unknown_folder, f"Failed_{timestamp}.jpg")
            cv2.imwrite(filename, img)
            # Send the image
            send_alert_sms(filename, "Face verification failed")
            self.otp_verification(UserId, self.data)

    def login_clear(self):
        try:
            if hasattr(self, 'login_card_entry') and self.login_card_entry.winfo_exists():
                self.login_card_entry.delete(0, 'end')
            if hasattr(self, 'login_pin_entry') and self.login_pin_entry.winfo_exists():
                self.login_pin_entry.delete(0, 'end')
        except tk.TclError:
            # Widget was destroyed, ignore the error
            pass

    def perform_transaction(self, user_id):
        def saving_data(user_data):
            # Read the existing data from the file
            with open('new/data.txt', 'r', encoding='utf-8') as file:
                data = json.load(file)
            
            # Update the user's data
            data[user_id] = user_data
            
            # Write the updated data back to the file
            with open('new/data.txt', 'w', encoding='utf-8') as file:
                json.dump(data, file, ensure_ascii=False)

        def update_csv(user_id, current_balance):
            # Open "Details/Details.csv" in read mode and create a temporary list to hold the updated data
            rows = []
            with open('Details/Details.csv', 'r') as file:
                reader = csv.reader(file)
                for row in reader:
                    if row[0] == user_id:
                        row[3] = str(current_balance)  # Update balance
                    rows.append(row)
            
            # Write the updated data back to the file
            with open('Details/Details.csv', 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerows(rows)

        def open_withdraw_window():
            withdraw_window = tk.Toplevel(self.root)
            withdraw_window.title("Withdraw Money")
            withdraw_window.geometry("400x300")
            withdraw_window.configure(bg=self.FRAME_BG)
            
            # Center the window
            withdraw_window.update_idletasks()
            width = withdraw_window.winfo_width()
            height = withdraw_window.winfo_height()
            x = (withdraw_window.winfo_screenwidth() // 2) - (width // 2)
            y = (withdraw_window.winfo_screenheight() // 2) - (height // 2)
            withdraw_window.geometry(f'{width}x{height}+{x}+{y}')

            def update_withdraw(user_id, withdraw_amount):
                # Open "Details/Details.csv" and create a temporary list to hold the updated data
                rows = []
                with open('Details/Details.csv', 'r') as file:
                    reader = csv.reader(file)
                    for row in reader:
                        if row[0] == user_id:
                            current_balance = float(row[3])
                            new_balance = current_balance - withdraw_amount
                            if new_balance >= 0:
                                row[3] = str(new_balance)
                            else:
                                messagebox.showerror("Error", "Insufficient balance!")
                                return False
                        rows.append(row)
                
                # Write the updated data back to the file
                with open('Details/Details.csv', 'w', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerows(rows)
                return True

            def perform_withdraw():
                try:
                    withdraw_amount = float(withdraw_entry.get())
                    if withdraw_amount <= 0:
                        messagebox.showerror("Error", "Please enter a valid amount!")
                        return
                    
                    if update_withdraw(user_id, withdraw_amount):
                        messagebox.showinfo("Success", f"Withdrawn ${withdraw_amount:.2f}")
                        withdraw_window.destroy()
                except ValueError:
                    messagebox.showerror("Error", "Please enter a valid number!")

            # Create and pack widgets with new theme
            tk.Label(withdraw_window, text="Enter Amount to Withdraw:", font=self.label_font, 
                    bg=self.FRAME_BG, fg=self.TEXT_COLOR).pack(pady=20)
            
            withdraw_entry = tk.Entry(withdraw_window, font=self.entry_font, width=20, 
                                    bg=self.ENTRY_BG, fg=self.ENTRY_FG)
            withdraw_entry.pack(pady=10)
            
            tk.Button(withdraw_window, text="Withdraw", font=self.button_font,
                     bg=self.BUTTON_PRIMARY_BG, fg=self.BUTTON_PRIMARY_FG,
                     command=perform_withdraw).pack(pady=20)

        def open_deposit_window():
            deposit_window = tk.Toplevel(self.root)
            deposit_window.title("Deposit Money")
            deposit_window.geometry("400x300")
            deposit_window.configure(bg=self.FRAME_BG)
            
            # Center the window
            deposit_window.update_idletasks()
            width = deposit_window.winfo_width()
            height = deposit_window.winfo_height()
            x = (deposit_window.winfo_screenwidth() // 2) - (width // 2)
            y = (deposit_window.winfo_screenheight() // 2) - (height // 2)
            deposit_window.geometry(f'{width}x{height}+{x}+{y}')

            def update_deposit(user_id, deposit_amount):
                # Open "Details/Details.csv" and create a temporary list to hold the updated data
                rows = []
                with open('Details/Details.csv', 'r') as file:
                    reader = csv.reader(file)
                    for row in reader:
                        if row[0] == user_id:
                            current_balance = float(row[3])
                            new_balance = current_balance + deposit_amount
                            row[3] = str(new_balance)
                        rows.append(row)
                
                # Write the updated data back to the file
                with open('Details/Details.csv', 'w', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerows(rows)

            def perform_deposit():
                try:
                    deposit_amount = float(deposit_entry.get())
                    if deposit_amount <= 0:
                        messagebox.showerror("Error", "Please enter a valid amount!")
                        return
                    
                    update_deposit(user_id, deposit_amount)
                    messagebox.showinfo("Success", f"Deposited ${deposit_amount:.2f}")
                    deposit_window.destroy()
                except ValueError:
                    messagebox.showerror("Error", "Please enter a valid number!")

            # Create and pack widgets with new theme
            tk.Label(deposit_window, text="Enter Amount to Deposit:", font=self.label_font,
                    bg=self.FRAME_BG, fg=self.TEXT_COLOR).pack(pady=20)
            
            deposit_entry = tk.Entry(deposit_window, font=self.entry_font, width=20,
                                   bg=self.ENTRY_BG, fg=self.ENTRY_FG)
            deposit_entry.pack(pady=10)
            
            tk.Button(deposit_window, text="Deposit", font=self.button_font,
                     bg=self.BUTTON_PRIMARY_BG, fg=self.BUTTON_PRIMARY_FG,
                     command=perform_deposit).pack(pady=20)

        def check_balance_window():
            # Create a tkinter window with new theme
            balance_window = tk.Toplevel(self.root)
            balance_window.title("Check Balance")
            balance_window.geometry("400x300")
            balance_window.configure(bg=self.FRAME_BG)
            
            # Center the window
            balance_window.update_idletasks()
            width = balance_window.winfo_width()
            height = balance_window.winfo_height()
            x = (balance_window.winfo_screenwidth() // 2) - (width // 2)
            y = (balance_window.winfo_screenheight() // 2) - (height // 2)
            balance_window.geometry(f'{width}x{height}+{x}+{y}')

            def check_balance(user_id):
                # Open "Details/Details.csv" and find the user's balance
                with open('Details/Details.csv', 'r') as file:
                    reader = csv.reader(file)
                    for row in reader:
                        if row[0] == user_id:
                            balance = float(row[3])
                            balance_label.config(text=f"Current Balance: ${balance:.2f}")
                            return
                    balance_label.config(text="User not found!")

            # Create and pack widgets with new theme
            tk.Label(balance_window, text="Account Balance", font=self.header_font,
                    bg=self.FRAME_BG, fg=self.TITLE_COLOR).pack(pady=20)
            
            balance_label = tk.Label(balance_window, text="", font=self.label_font,
                                   bg=self.FRAME_BG, fg=self.TEXT_COLOR)
            balance_label.pack(pady=10)
            
            check_balance(user_id)
            
            tk.Button(balance_window, text="Close", font=self.button_font,
                     bg=self.BUTTON_SECONDARY_BG, fg=self.BUTTON_SECONDARY_FG,
                     command=balance_window.destroy).pack(pady=20)

        def logout():
            self.show_frame(self.welcome_frame)

        # Create transaction window with new theme
        transaction_window = tk.Toplevel(self.root)
        transaction_window.title("ATM Transactions")
        transaction_window.geometry("600x400")
        transaction_window.configure(bg=self.FRAME_BG)
        
        # Center the window
        transaction_window.update_idletasks()
        width = transaction_window.winfo_width()
        height = transaction_window.winfo_height()
        x = (transaction_window.winfo_screenwidth() // 2) - (width // 2)
        y = (transaction_window.winfo_screenheight() // 2) - (height // 2)
        transaction_window.geometry(f'{width}x{height}+{x}+{y}')

        # Create and pack widgets with new theme
        tk.Label(transaction_window, text="Select Transaction", font=self.title_font,
                bg=self.FRAME_BG, fg=self.TITLE_COLOR).pack(pady=20)

        # Create buttons with new theme
        tk.Button(transaction_window, text="Withdraw Money", font=self.button_font,
                 bg=self.BUTTON_PRIMARY_BG, fg=self.BUTTON_PRIMARY_FG,
                 command=open_withdraw_window).pack(pady=10)
        
        tk.Button(transaction_window, text="Deposit Money", font=self.button_font,
                 bg=self.BUTTON_PRIMARY_BG, fg=self.BUTTON_PRIMARY_FG,
                 command=open_deposit_window).pack(pady=10)
        
        tk.Button(transaction_window, text="Check Balance", font=self.button_font,
                 bg=self.BUTTON_PRIMARY_BG, fg=self.BUTTON_PRIMARY_FG,
                 command=check_balance_window).pack(pady=10)
        
        tk.Button(transaction_window, text="Logout", font=self.button_font,
                 bg=self.BUTTON_SECONDARY_BG, fg=self.BUTTON_SECONDARY_FG,
                 command=logout).pack(pady=10)

    def otp_verification(self, UserId, data):
        # Get user's phone number
        phone_number = "+916380825972"
        if not phone_number:
            messagebox.showerror("Error", "Phone number not found for this user.")
            return

        # Generate and send OTP
        try:
            otp = send_otp_sms(phone_number)
            if not otp:
                messagebox.showerror("Error", "Failed to generate OTP. Please try again.")
                return

            messagebox.showinfo("OTP Verification", f"An OTP has been sent to {phone_number}. Please enter it.")
            
            otp_window = tk.Toplevel(self.root)
            otp_window.title("OTP Verification")
            otp_window.geometry("300x200")
            otp_window.configure(bg=self.FRAME_BG)
            
            # Center the window
            otp_window.update_idletasks()
            width = otp_window.winfo_width()
            height = otp_window.winfo_height()
            x = (otp_window.winfo_screenwidth() // 2) - (width // 2)
            y = (otp_window.winfo_screenheight() // 2) - (height // 2)
            otp_window.geometry(f'{width}x{height}+{x}+{y}')
            
            tk.Label(otp_window, text="Enter OTP:", font=self.label_font,
                    bg=self.FRAME_BG, fg=self.TEXT_COLOR).pack(pady=10)
            
            otp_entry = tk.Entry(otp_window, font=self.entry_font, width=20,
                               bg=self.ENTRY_BG, fg=self.ENTRY_FG)
            otp_entry.pack(pady=10)
            
            def check_otp():
                entered_otp = otp_entry.get()
                if verify_otp(entered_otp):
                    messagebox.showinfo("Success", "OTP Verified Successfully!")
                    otp_window.destroy()
                    self.perform_transaction(UserId)  # Proceed with transaction after successful OTP verification
                else:
                    messagebox.showerror("Error", "Invalid OTP. Please try again.")
            
            tk.Button(otp_window, text="Verify", font=self.button_font,
                     bg=self.BUTTON_PRIMARY_BG, fg=self.BUTTON_PRIMARY_FG,
                     command=check_otp).pack(pady=10)
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to send OTP: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = ATMApp(root)
    root.mainloop()