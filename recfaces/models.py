from django.db import models
from .RecogniseSQLExFunctions import encodeImageToBin
from .RecogniseSQLExFunctions import mainCheckAndAddImageToBase, genTempName, mainCheckImageInBase, replacePhoto, removePhoto
from django.conf import settings
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import os
from icecream import ic


class Person(models.Model):
    fio = models.CharField(max_length=50, default="unknown")
    gender = models.CharField(max_length=1, choices=[('M', 'Male'), ('F', 'Female')], default="M")
    age = models.SmallIntegerField(default="0")
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
        ic(settings.PATH_IMAGES)

        isOld = mainCheckImageInBase(tmpFilePath, settings.DB_INFO)

        if not isOld:
            ic(settings.PATH_IMAGES)
            replacePhoto(tmpFilePath, settings.PATH_IMAGES)
            newImgPath = os.path.join(settings.PATH_IMAGES, tempName)
            self.binImg = encodeImageToBin(newImgPath)
            self.imgPath = newImgPath

            # self.binImg = encodeImageToBin(self.imgPath.__str__())
            ic(self.fio)
            ic(self.age)
            ic(self.gender)
            ic(self.imgPath)
            ic(len(self.binImg))
            super().save(*args, **kwargs)
        else:
            print(f"Photo already exists in DB")
            removePhoto(tmpFilePath)

    def delete(self):
        removePhoto(self.imgPath.__str__())
        super().delete()

    def __str__(self):
        return self.name
