from flask import Flask, request, jsonify 
from flask_cors import CORS
from config.app_config import CORS_ALLOWED_ORIGINS, DEBUG_MODE
from dotenv import load_dotenv
from controllers.identification_controller import *

load_dotenv()

app = Flask(__name__, static_folder='wwwroot')
CORS(app, origins=CORS_ALLOWED_ORIGINS, supports_credentials=True)

@app.post('/identifications')
def create_identification():
    return jsonify(create_identification_controller(request.get_data()))

if __name__ == '__main__':
    app.run(debug=DEBUG_MODE, port=8000, host='0.0.0.0')