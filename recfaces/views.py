from django.http import HttpResponse
from .forms import loadImageForm
from .models import Person
from django.views.generic import ListView, CreateView
from django.urls import reverse_lazy
from django.conf import settings
from django.shortcuts import redirect
from icecream import ic

class HomePageView(ListView):
    model = Person
    template_name = 'homeEx2.html'

    def get_context_data(self, **kwargs):
        context = super(HomePageView, self).get_context_data(**kwargs)
        context["messages"] = settings.MESSAGES
        settings.MESSAGES = ""
        return context

class CreatePostView(CreateView):
    model = Person
    form_class = loadImageForm
    template_name = 'addPersonEx.html'
    success_url = reverse_lazy('home')

def delete(request, id):
    from .RecogniseSQLExFunctions import mainRemovePerson
    mainRemovePerson(settings.DB_INFO, id, settings.PATH_IMAGES)
    return redirect('home')

# работает верно!
from django.views.decorators.csrf import csrf_exempt
@csrf_exempt
def catchHook(request):
    import os
    from django.core.files.storage import default_storage
    from django.core.files.base import ContentFile
    from .RecogniseSQLExFunctions import mainCheckAndAddImageToBase, genTempName, sendMessage
    from django.http import JsonResponse
    from .ExtraFunctions import checkPost

    print("hook catched")

    if request.method == "POST":
        isCorrect, msgErr = checkPost(request)
        if not isCorrect:
            return JsonResponse({"message": msgErr})
        else:
            tempImage = request.FILES['face']
            idSource = request.POST["idSource"]

            tempName = "face" + genTempName() + ".jpg"
            path = default_storage.save(os.path.join("tmp", tempName), ContentFile(tempImage.read()))
            tmpFilePath = os.path.join(settings.MEDIA_ROOT, path)

            DB_ObjectInfo = {
                "id": None,
                "gender": "?",
                "age": 0,
                "idSource": idSource,
                "imgPath": tmpFilePath,
            }
            DB_ObjectInfo, isOld = mainCheckAndAddImageToBase(DB_ObjectInfo, settings.DB_INFO, settings.PATH_IMAGES)
            msg = settings.MESSAGES
            msg = msg.split("\\n")
            msg = "\n".join(msg)
            settings.MESSAGES = ""

            answer = DB_ObjectInfo
            answer.pop("imgPath")
            answer["message"] = msg
            return JsonResponse(answer)
    return JsonResponse({"message": "Try to use POST"})

