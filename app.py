from flask import Flask, render_template, request, send_from_directory
import os
import uuid
from PIL import Image

app = Flask(__name__)

def save_image(image):
    extension = os.path.splitext(image.filename)[1].lower().lstrip(".")

    if extension not in ALLOWED_EXTENSIONS:
        return None

    try:
        img = Image.open(image)
        img.verify()
        image.seek(0)
    except Exception:
        return None

    filename = str(uuid.uuid4()) + "." + extension
    filepath = os.path.join(UPLOAD_FOLDER, filename)

    image.save(filepath)

    return filepath

app.config["MAX_CONTENT_LENGTH"] = 10 * 1024 * 1024

UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png", "webp"}
MAX_CONTENT_LENGTH = 10 * 1024 * 1024

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        user_image = request.files.get("user_image")
        clothes_image = request.files.get("clothes_image")

        if user_image and clothes_image:
            user_path = save_image(user_image)
            clothes_path = save_image(clothes_image)

            return render_template(
                "index.html",
                user_image=user_path,
                clothes_image=clothes_path
            )

    return render_template("index.html")

@app.route("/uploads/<filename>")
def uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

@app.errorhandler(413)
def too_large(error):
    return "圖片太大，請選擇 10 MB 以下的圖片", 413    


if __name__ == "__main__":
    app.run(debug=True)