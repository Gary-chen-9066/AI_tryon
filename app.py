from flask import Flask, render_template, request
import os
import uuid

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png", "webp"}

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        image = request.files.get("user_image")

        if image:
            extension = os.path.splitext(image.filename)[1].lower().lstrip(".")

            if extension not in ALLOWED_EXTENSIONS:
                return "不支援的圖片格式", 400

            filename = str(uuid.uuid4()) + "." + extension
            filepath = os.path.join(UPLOAD_FOLDER, filename)

            image.save(filepath)

    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)