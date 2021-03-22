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

    print("hook catched")
    if request.method == "POST":
        tempImage = request.FILES['face']
        if tempImage==None:
            print("There is no photo to add")
            return # доделать

        tempName = "face" + genTempName() + ".jpg"
        path = default_storage.save(os.path.join("tmp", tempName), ContentFile(tempImage.read()))
        tmpFilePath = os.path.join(settings.MEDIA_ROOT, path)

        id, isOld, msg = mainCheckAndAddImageToBase(tmpFilePath, settings.DB_INFO, settings.PATH_IMAGES)
        settings.MESSAGES = ""

        return HttpResponse(f"Принято!\nРезультат:\n{msg}")
    return HttpResponse("Try to use POST")

