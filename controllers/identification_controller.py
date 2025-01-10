from services.model import *

def identify_image_controller(img):
    return predict(img)

def identify_video_controller(img):
    return predict_video(img)