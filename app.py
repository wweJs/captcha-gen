from flask import Flask, request, send_file
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import io
import random

app = Flask(__name__)

def generate_captcha(text):
    width, height = 400, 200
    
    image = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(image)
    
    font_size = 80
    try:
        font = ImageFont.truetype("arial.ttf", font_size)
    except:
        font = ImageFont.load_default()
    
    x, y = 50, 50
    for char in text:
        draw.text((x, y + random.randint(-15, 15)), char, font=font, fill="black")
        x += 60
    
    image = image.filter(ImageFilter.GaussianBlur(1))
    
    for _ in range(5):
        image = image.transform(image.size, Image.AFFINE, 
                                (1, random.uniform(-0.5, 0.2), 0, 0, 1, random.uniform(-2, 2)))
    img_io = io.BytesIO()
    image.save(img_io, "PNG")
    img_io.seek(0)
    return img_io

@app.route("/cap")
def generate_captcha_route():
    text = request.args.get("text", "CAPTCHA")
    img_io = generate_captcha(text)
    return send_file(img_io, mimetype="image/png")

@app.route("/randomcap")
def generate_random_cap():
    img_io = generate_captcha(str(random.randint(0, 3000)))
    return send_file(img_io, mimetype="image/png")

@app.route("/dev/status")
def status():
    return "DEV_STATUS_WORKING"

if __name__ == "__main__":
    app.run(debug=True, port=3848)