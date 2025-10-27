from flask import Flask, render_template, jsonify, request
from io import BytesIO
import requests
import base64
from dotenv import load_dotenv
load_dotenv()
from os import getenv

API_KEY: str = str(getenv("HUGGINGFACE_API_KEY")) # replace this with your own hugging face api key

web = Flask(__name__, static_folder="assets\\")

@web.route("/")
def index():
    return render_template("index.html")

@web.route("/generate", methods=["POST"])
def generate():
     res: requests.Response = requests.post("https://router.huggingface.co/hf-inference/models/stabilityai/stable-diffusion-3-medium-diffusers" , headers={"Authorization": f"Bearer {API_KEY}"}, json={"inputs": request.get_json()["prompt"]})
     if res.status_code != 200:
        return jsonify({"error": f"yo smthing went wrong again :(((; error code: {res.status_code}"})
     img: str = base64.b64encode(BytesIO(res.content).getvalue()).decode("utf-8")
     print(img)
     return jsonify({
         "imgid": img
     })


if __name__ == "__main__":
    web.run(debug=True, port=5004)