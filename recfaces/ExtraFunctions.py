
def ms(msg):

    print(msg)
    return msg+"\n"

def checkPost(request):
    # проверка на существование файла и idSource post запросе
    msg = ""
    try:
        tempImage = request.FILES['face']
    except Exception:
        msg += ms("There is no photo to add")
        msg += ms("Expected an image in 'request.FILES['face']', but there is no 'request.FILES['face']'")
        msg += ms("Output of 'request.FILES':")
        msg += ms(request.FILES.__str__())
        return False, msg
    if tempImage == None:
        msg += ms("File field of the post is none")
        msg += ms("There exists 'request.FILES['face']', but it is equal to 'None'")
        return False, msg

    try:
        idSource = request.POST["idSource"]
    except Exception:
        msg += ms("There is no idSource in the body of post")
        msg += ms("Expected a number in 'request.POST['idSource']', but there is no 'request.POST['idSource']'")
        msg += ms("Output of 'request.POST':")
        msg += ms(request.POST.__str__())
        return False, msg
    if idSource == None:
        msg += ms("idSource field of the post is none")
        msg += ms("There exists 'request.POST['idSource']', but it is equal to 'None'")
        return False, msg
    return True, msg