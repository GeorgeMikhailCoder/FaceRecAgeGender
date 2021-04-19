from django.conf import settings
import logging.config

def ms(msg):

    print(msg)
    return msg+"\n"

def checkPost(request):
    # проверка на существование файла и idSource post запросе
    logger = logging.getLogger("main_logger.ExtraFunctions.checkPost")
    msg = ""
    try:
        tempImage = request.FILES['face']
    except Exception:
        msg += ms("There is no photo to add")
        msg += ms("Expected an image in 'request.FILES['face']', but there is no 'request.FILES['face']'")
        msg += ms("Output of 'request.FILES':")
        msg += ms(request.FILES.__str__())
        logger.error(f"There is no photo to add, expected an image in 'request.FILES['face']', but there is no 'request.FILES['face']', Output of 'request.FILES': {request.FILES.__str__()}")
        return False, msg
    if tempImage == None:
        msg += ms("File field of the post is none")
        msg += ms("There exists 'request.FILES['face']', but it is equal to 'None'")
        logger.error(f"File field of the post is none, there exists 'request.FILES['face']', but it is equal to 'None'")
        return False, msg
    return True, msg