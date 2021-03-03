from django.db import models
from .RecogniseSQLExFunctions import encodeImageToBin
from .RecogniseSQLExFunctions import genTempName, mainCheckImageInBase, replacePhoto, removePhoto
from .AGpredictor.predict_AG import mainPredictAG
from django.conf import settings
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import os
from icecream import ic


class Person(models.Model):
    fio = models.CharField(max_length=50, default="unknown")
    gender = models.CharField(max_length=1, choices=[(settings.DEFAULT_AG["gender"], '?'), ('M', 'Male'), ('F', 'Female')], default=settings.DEFAULT_AG["gender"])
    age = models.SmallIntegerField(default=settings.DEFAULT_AG["age"])
    imgPath = models.ImageField(max_length=200, default="None")
    binImg = models.BinaryField(max_length=2048, default=None)

    # работает верно!
    def save(self, *args, **kwargs):
        tempImage =self.imgPath
        if tempImage=="None":
            print("There is no photo to add")
            return # доделать
        tempName = "face" + genTempName() + ".jpg"
        path = default_storage.save(os.path.join("tmp",tempName), ContentFile(tempImage.read()))
        tmpFilePath = os.path.join(settings.MEDIA_ROOT, path)
        isOld = mainCheckImageInBase(tmpFilePath, settings.DB_INFO)

        if not isOld:
            replacePhoto(tmpFilePath, settings.PATH_IMAGES)
            newImgPath = os.path.join(settings.PATH_IMAGES, tempName)
            self.binImg = encodeImageToBin(newImgPath)
            self.imgPath = newImgPath

            print(f"fio = {self.fio}")
            print(f"age = {self.age}")
            print(f"gender = {self.gender}")
            print(f"image file full path: {self.imgPath.__str__()}")
            print(f"encoding face length = {len(self.binImg)}")
            # ic(settings.PATH_IMAGES)

            if self.age == settings.DEFAULT_AG["age"] or self.gender == settings.DEFAULT_AG["gender"]:
                age, gender = mainPredictAG(self.imgPath.__str__(), settings.PREDICT_ACCURACY, settings.DEFAULT_AG)

                if self.age == settings.DEFAULT_AG["age"] and age != settings.DEFAULT_AG["age"]:
                    self.age = age


                if self.gender == settings.DEFAULT_AG["gender"] and gender != settings.DEFAULT_AG["gender"]:
                    self.gender = gender


            super().save(*args, **kwargs)
        else:
            print(f"Photo already exists in DB")
            removePhoto(tmpFilePath)

    def delete(self):
        removePhoto(self.imgPath.__str__())
        super().delete()

    def __str__(self):
        return self.name
