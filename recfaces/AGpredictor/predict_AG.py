from age_and_gender import AgeAndGender
from time import time
from PIL import Image
from icecream import ic
import os


data = AgeAndGender()
data.load_shape_predictor(os.path.join("recfaces","AGpredictor",'shape_predictor_5_face_landmarks.dat'))
data.load_dnn_gender_classifier(os.path.join("recfaces","AGpredictor",'dnn_gender_classifier_v1.dat'))
data.load_dnn_age_predictor(os.path.join("recfaces","AGpredictor",'dnn_age_predictor_v1.dat'))

def predictAG(imgPath):
    image = Image.open(imgPath).convert("RGB")
    prediction = data.predict(image)
    if len(prediction) == 0:
        res = None
    else:
        res = prediction[0]
        age = res["age"]["value"]
        ageAc = res["age"]["confidence"]
        gender = res["gender"]["value"]
        genderAc = res["gender"]["confidence"]
        print(f"predicted age = {age} (accuracy = {ageAc}%)")
        print(f"predicted gender = \"{gender}\" (accuracy = {genderAc}%)")
    return res

def applyPredictionAG(prediction, poss, defaults):
    # ic(prediction)
    if prediction==None:
        print(f"Fail to predict age/gender of the photo")
        age = defaults["age"]
        gender = defaults["gender"]
    else:
        if prediction["age"]["confidence"]>poss:
            age = prediction["age"]["value"]
        else:
            age = defaults["age"]

        if prediction["gender"]["confidence"]>poss:
            if prediction["gender"]["value"] == "male":
                gender = "M"
            else:
                gender = "F"
        else:
            gender = defaults["gender"]

    return age, gender

def mainPredictAG(imgPath, poss, defaults):
    return applyPredictionAG(predictAG(imgPath), poss, defaults)

if __name__=="__main__":
    print(mainPredictAG('./images/1.jpeg', 0.7, {"age": 0, "gender": "?"}))