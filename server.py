from flask import Flask, request, jsonify
import os

from upload_to_drive import upload_file  # Import the upload function

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/upload_to_drive", methods=["POST"])
def upload_to_drive():
    original_file = request.files["original_images"]
    watermarked_file = request.files["watermarked_images"]

    # Save temporarily
    original_path = os.path.join(UPLOAD_FOLDER, original_file.filename)
    watermarked_path = os.path.join(UPLOAD_FOLDER, watermarked_file.filename)

    original_file.save(original_path)
    watermarked_file.save(watermarked_path)

    # Upload to Google Drive
    original_link = upload_file(original_path, "YOUR_ORIGINALS_FOLDER_ID")
    watermarked_link = upload_file(watermarked_path, "YOUR_WATERMARKED_FOLDER_ID")

    # Remove temporary files
    os.remove(original_path)
    os.remove(watermarked_path)

    return jsonify({"original": original_link, "watermarked
