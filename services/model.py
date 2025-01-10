from tensorflow.keras.models import load_model
from PIL import Image
import numpy as np
import io
from config.object_entities import *
from models.Response import *

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
        return Response[str](data=object_entities[int(predicted_class[0])], is_success=True).model_dump()
    except Exception as e:
        return Response[str](error=str(e), is_success=False).model_dump()