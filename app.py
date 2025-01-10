from flask import Flask, request, jsonify 
from flask_cors import CORS
from config.app_config import CORS_ALLOWED_ORIGINS, DEBUG_MODE
from dotenv import load_dotenv
from controllers.identification_controller import *

load_dotenv()

app = Flask(__name__, static_folder='wwwroot')
CORS(app, origins=CORS_ALLOWED_ORIGINS, supports_credentials=True)

@app.post('/identifications/image')
def identify_image():
    return jsonify(identify_image_controller(request.get_data()))

@app.post('/identifications/video')
def identify_video():
    return jsonify(identify_video_controller(request.get_data()))

if __name__ == '__main__':
    app.run(debug=DEBUG_MODE, port=PORT, host='0.0.0.0')