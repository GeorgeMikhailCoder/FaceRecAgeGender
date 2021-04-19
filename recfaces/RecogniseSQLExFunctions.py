import face_recognition
import MySQLdb
import numpy as np
import pickle
import os
from shutil import move
from django.conf import settings
import logging.config

def mysqlConnect(DB_INFO):
    try:
        con = MySQLdb.connect(
            db=DB_INFO["NAME"],
            user=DB_INFO["USER"],
            passwd=DB_INFO["PASSWORD"],
            host=DB_INFO["HOST"],
        )
    except:
        settings.MESSAGES += f"Fail to connect to database \n DB_INFO = {DB_INFO} \n"
        logger = logging.getLogger("main_logger.RecogniseSQLExFunctions.mysqlConnect")
        logger.error(f"Fail to connect to database \n DB_INFO = {DB_INFO}")
        con = None
    finally:
        return con

def genTempName():
    from time import time
    s = time().__str__()
    res = s.split(".")
    res = res[0]+res[1]
    return res

def sendMessage(msg):
    url = "https://enkrie5ea41stk5.m.pipedream.net" # мой адрес
    print(msg)
    print(f"Send to {url}")
    from requests import post
    try:
        post(url, data={"message": msg})
    except Exception:
        print("Error in connection to server")

def encodeImageToBin(pathImage):
    img = face_recognition.load_image_file(pathImage)
    imgRect = (0, img.shape[1], img.shape[0], 0)
    imgEnc = face_recognition.face_encodings(img, [imgRect])[0]
    binImg = pickle.dumps(imgEnc)
    return binImg

def defImgageEncoding(img):
    imgRect = (0, img.shape[1], img.shape[0], 0)
    imgEnc = face_recognition.face_encodings(img, [imgRect])[0]
    return imgEnc

def getListEnc(DBcursor):
    # using bytes
    DBcursor.execute('SELECT binImg FROM recfaces_person')
    encodes = [pickle.loads(enc[0]) for enc in DBcursor.fetchall()]
    return encodes

def getListEnc2(DBcursor):
    # using strings
    DBcursor.execute('SELECT binImg FROM recfaces_person')
    encodes = [np.fromstring(enc[0]) for enc in DBcursor.fetchall()]
    return encodes

def isInBase(imgEnc, encodes):
    faceDistances = face_recognition.face_distance(encodes, imgEnc)
    if len(faceDistances) == 0:
        return False, None

    bestIndex = np.argmin(faceDistances)
    match = face_recognition.compare_faces([encodes[bestIndex], ], imgEnc, settings.KOEF_FACE_COMPARATION)[0]

    logger = logging.getLogger("main_logger.RecogniseSQLExFunctions.isInBase")
    logger.info(f"Comparing faces: distance = {faceDistances[bestIndex]}, KOEF_FACE_COMPARATION = {settings.KOEF_FACE_COMPARATION}, isInBase = {match}")
    settings.MESSAGES += f"Comparing faces: distance = {faceDistances[bestIndex]}, KOEF_FACE_COMPARATION = {settings.KOEF_FACE_COMPARATION}, isInBase = {match}, best index in mass = {bestIndex}\\n"

    return match, bestIndex

def addToBase(DBcursor, name, age, gender,idSource ,imgPath, imgEnc=np.empty(0)):
    if(len(imgEnc)==0):
        img = face_recognition.load_image_file(imgPath)
        imgEnc = defImgageEncoding(img)

    binImg = pickle.dumps(imgEnc)

    DBcursor.execute('INSERT INTO recfaces_person (fio, age, gender, idSource, imgPath, binImg)'
                     ' VALUES (%s,%s,%s,%s,%s,%s)',
                     (name, age, gender, idSource, imgPath, binImg)
                     )

def replacePhoto(imgPath, pathTo):
    try:
        move(imgPath, pathTo)
    except:
        settings.MESSAGES += f"Fail to replace file: \n path from = {imgPath} ,\n path to = {pathTo} \n"
        logger = logging.getLogger("main_logger.RecogniseSQLExFunctions.removePhoto")
        logger.error(f"Fail to replace file: \n path from = {imgPath} ,\n path to = {pathTo}")

def removePhoto(imgPath):
    logger = logging.getLogger("main_logger.RecogniseSQLExFunctions.removePhoto")
    try:
        os.remove(imgPath)
    except Exception:
        logger.error(f"Fail to remove file: {imgPath}")
        logger.error("Also an object in base will be removed")

def showBase(DBcursor):
    for row in DBcursor.execute('SELECT id, fio, gender, age FROM recfaces_person'):
        print(row)

def createTable(DBcursor):
    DBcursor.execute("""CREATE TABLE recfaces_person
                    (
                    id INTEGER PRIMARY KEY,
                    fio varchar(50),
                    gender varchar(1),
                    age smallint,
                    imgPath varchar(100),
                    binImg bytes(1024)
                    )
                    """)

def removeTable(DBcursor):
    DBcursor.execute("""DROP TABLE recfaces_person""")

def clearTable(DBcursor):
    DBcursor.execute("""DELETE FROM recfaces_person""")

def getFirstIndex(DBcursor):
    DBcursor.execute("""SELECT id FROM recfaces_person ORDER BY id LIMIT 1""")

    res = DBcursor.fetchone()
    if res:
        return int(res[0])
    else:
        return None

def DB_answer2ObjectInfo(DB_answer):
    return {
            "id": DB_answer[0],
            "fio": DB_answer[1],
            "age": DB_answer[2],
            "gender": DB_answer[3],
            "idSource": DB_answer[4],
            "imgPath": DB_answer[5],
        }

def checkImageInBase(imgPath, DBcursor):
    img = face_recognition.load_image_file(imgPath)
    imgEnc = defImgageEncoding(img)
    encodes = getListEnc(DBcursor)
    res, indexMass = isInBase(imgEnc, encodes)
    firstID = getFirstIndex(DBcursor)

    if not indexMass==None:
        logger = logging.getLogger("main_logger.RecogniseSQLExFunctions.checkImageInBase")
        logger.info(f"Best id = {firstID + indexMass}")
        settings.MESSAGES += f"Best id = {firstID + indexMass}\\n"

    if res:
        resID = firstID + indexMass
    else:
        resID = None



    return res, resID

def checkAndAddImageInBase(DB_ObjectInfo, DBcursor, pathDBImages):
    logger = logging.getLogger("main_logger.RecogniseSQLExFunctions.checkAndAddImageInBase")
    imgPath = DB_ObjectInfo["imgPath"]
    img = face_recognition.load_image_file(imgPath)
    imgEnc = defImgageEncoding(img)
    encodes = getListEnc(DBcursor)
    isOld, index = isInBase(imgEnc, encodes)

    if isOld:
        binImg = pickle.dumps(encodes[index])
        DBcursor.execute("SELECT id, fio, age, gender, idSource, imgPath  FROM recfaces_person WHERE binImg=%s", (binImg,))
        DB_answer = DBcursor.fetchone()
        DB_ObjectInfo = DB_answer2ObjectInfo(DB_answer)

        removePhoto(imgPath)

        id = DB_ObjectInfo["id"]
        logger.info(f"Face exists in database, id = {id}")
        settings.MESSAGES += f"Face exists in database, id = {id}\\n"
    else:
        imgName = os.path.split(imgPath)[1]
        imgNewPath = os.path.join(pathDBImages, imgName)
        replacePhoto(imgPath, imgNewPath)

        from .AGpredictor.predict_AG import mainPredictAG
        age, gender = mainPredictAG(imgNewPath, settings.PREDICT_ACCURACY, settings.DEFAULTS)

        idSource = DB_ObjectInfo["idSource"]

        addToBase(DBcursor, "unknown", age, gender, idSource, imgNewPath, imgEnc)
        binImg = pickle.dumps(imgEnc)

        DBcursor.execute("SELECT id, fio, age, gender, idSource, imgPath  FROM recfaces_person WHERE binImg=%s", (binImg,))
        DB_answer = DBcursor.fetchone()
        DB_ObjectInfo = DB_answer2ObjectInfo(DB_answer)

        id = DB_ObjectInfo["id"]
        logger.info(f"Face doesn't exists in database, added, id = {id}")
        settings.MESSAGES += f"Face doesn't exists in database, added, id = {id}\\n"
    return DB_ObjectInfo, isOld

def mainCheckAndAddImageToBase(DB_ObjectInfo, DB_Info, pathDBImages):
    try:
        dbConnection = mysqlConnect(DB_Info)
    except:
        return DB_ObjectInfo, True

    db = dbConnection.cursor()

    DB_ObjectInfo, isOld = checkAndAddImageInBase(DB_ObjectInfo, db, pathDBImages)

    dbConnection.commit()
    dbConnection.close()
    return DB_ObjectInfo, isOld

def mainCheckImageInBase(pathImage, DB_INFO):
    db = MySQLdb.connect(
                     db=DB_INFO["NAME"],
                     user=DB_INFO["USER"],
                     passwd=DB_INFO["PASSWORD"],
                     host=DB_INFO["HOST"],
                     )
    cursor = db.cursor()
    res, index = checkImageInBase(pathImage, cursor)
    db.commit()
    db.close()
    return res, index

def mainRemovePerson(DB_Info, id, mediaRoot):
    dbConnection = mysqlConnect(DB_Info)
    db = dbConnection.cursor()

    db.execute("SELECT imgPath FROM recfaces_person WHERE id=%s", (id,))
    imgPath = db.fetchone()[0]
    pathToRemove = os.path.join(mediaRoot, imgPath)
    removePhoto(pathToRemove)

    db.execute("DELETE FROM recfaces_person WHERE id=%s", (id,))

    dbConnection.commit()
    dbConnection.close()

if __name__=="__main__":
    # pathDB = ":memory:"
    pathDB = "testDB1.sqlite3"
    pathImage = "4zxc.jpg"

    dbConnection = sqlite3.connect(pathDB)
    db = dbConnection.cursor()

    removeTable(db)
    createTable(db)
    addToBase(db, "4class", 10, "M", "4zxc.jpg")
    addToBase(db, "14age", 14, "M", "qwe.jpg")
    showBase(db)

    dbConnection.commit()
    dbConnection.close()



