from tensorflow.keras.models import load_model
from PIL import Image
import numpy as np
import cv2
import io
import os
from uuid import uuid4
from config.object_entities import *
from models.Response import *
from config.app_config import *

model = load_model('lib/model.h5')

def preprocess_image(image):
    image = image.resize((640, 640))
    image = np.array(image)
    image = image / 255.0
    image = np.expand_dims(image, axis=0)
    return image

def predict(img):
    try:
        img = Image.open(io.BytesIO(img))
        processed_image = preprocess_image(img)
        predictions = model.predict(processed_image)
        predicted_class = np.argmax(predictions, axis=-1)
        confidence = float(np.max(predictions) * 100)
        return Response[dict](data={
            "entity": object_entities[int(predicted_class[0])],
            "confidence_score": confidence
        }, is_success=True).model_dump()
    except Exception as e:
        return Response[str](error=str(e), is_success=False, data="").model_dump()
    
def predict_frame(frame, id, idx):
    try:
        img = Image.fromarray(frame)
        processed_image = preprocess_image(img)
        predictions = model.predict(processed_image)
        predicted_class = np.argmax(predictions, axis=-1)
        confidence = float(np.max(predictions) * 100)
        return {
            "confidence_score": confidence,
            "url": f"{HOST}:{PORT}/wwwroot/{id}/frame_{idx}.jpg", 
            "entity": object_entities[int(predicted_class[0])]
        }
    
    except Exception as e:
        return None

def predict_video(file):
    try:
        folder_name = str(uuid4())
        os.makedirs(f"wwwroot/{folder_name}")
        filename = f"video_{folder_name}.mp4"
        
        file_path = os.path.join(f"wwwroot/{folder_name}", filename)
        with open(file_path, 'wb') as f:
            f.write(file)

        cap = cv2.VideoCapture(file_path)

        frame_predictions = []
        idx = 1
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            prediction = predict_frame(frame, folder_name, idx)
            if prediction != None:
                frame_filename = os.path.join(f"wwwroot/{folder_name}", f'frame_{idx}.jpg')
                cv2.imwrite(frame_filename, frame)

                frame_predictions.append(prediction)
                idx += 1

        cap.release()
        return Response[dict](is_success=True, data={"frames": frame_predictions, "video_url": f"{HOST}:{PORT}/wwwroot/{folder_name}/{filename}"}).model_dump()

    except Exception as e:
        return Response[str](error=str(e), is_success=False, data="").model_dump()