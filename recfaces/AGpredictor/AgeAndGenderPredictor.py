from age_and_gender import AgeAndGender
from time import time
from PIL import Image
from icecream import ic

st = time()
data = AgeAndGender()
data.load_shape_predictor('shape_predictor_5_face_landmarks.dat')
data.load_dnn_gender_classifier('dnn_gender_classifier_v1.dat')
data.load_dnn_age_predictor('dnn_age_predictor_v1.dat')
ic(time()-st)
image = Image.open('./images/1.jpeg').convert("RGB")
result = data.predict(image)
ic(result)
