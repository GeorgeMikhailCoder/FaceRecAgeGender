import os
from.settings import BASE_DIR
from icecream import ic
def getVar(name, var):
    if os.environ.get(name) != None:
        var = os.environ.get(name)
        print(f"Set environment variable {name} = {var}")
    return var


PATH_IMAGES = os.path.join(BASE_DIR, "media", "facesImages", "facesImages")
KOEF_FACE_COMPARATION = 0.4
# насколько большую разницу между лицами можно считать одним лицом
# 0.99 - разные люди воспринимаются как один
# 0.01 - один человек воспринимается как разные
# по умолчанию 0.6

DB_NAME = "db_test"
DB_USER = "test_user"
DB_PASSWORD = "secpass"
DB_HOST = "localhost"
DB_PORT = "3306"

envVar = True
if envVar:
    PATH_IMAGES = getVar("PATH_IMAGES", PATH_IMAGES)
    KOEF_FACE_COMPARATION = float(getVar("KOEF_FACE_COMPARATION", KOEF_FACE_COMPARATION))
    DB_NAME = getVar("DB_NAME", DB_NAME)
    DB_USER = getVar("DB_USER", DB_USER)
    DB_PASSWORD = getVar("DB_PASSWORD", DB_PASSWORD)
    DB_HOST = getVar("DB_HOST", DB_HOST)
    DB_PORT = getVar("DB_PORT", DB_PORT)



DB_INFO = {
    'NAME': DB_NAME,
    "USER": DB_USER,
    "PASSWORD": DB_PASSWORD,
    "HOST": DB_HOST,
    "PORT": DB_PORT,
}

