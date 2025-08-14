from flask import Flask, send_from_directory
import os

app = Flask(__name__)

# Use absolute path for reliability
UPLOAD_FOLDER = os.path.abspath("Unknown_Face_Captures")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)  # Ensure folder exists
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Route to serve uploaded images
@app.route("/uploads/<filename>")
def uploaded_file(filename):
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)

if __name__ == "__main__":
    # Run server on all interfaces so it's accessible externally
    app.run(host="0.0.0.0", port=5000)

