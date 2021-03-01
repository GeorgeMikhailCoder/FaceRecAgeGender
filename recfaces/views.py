from django.http import HttpResponse
from .forms import loadImageForm
from .models import Person
from django.views.generic import ListView, CreateView
from django.urls import reverse_lazy
from django.conf import settings
from django.shortcuts import redirect

class HomePageView(ListView):
    model = Person
    template_name = 'homeEx2.html'

class CreatePostView(CreateView):
    model = Person
    form_class = loadImageForm
    template_name = 'addPersonEx.html'
    success_url = reverse_lazy('home')

def delete(request, id):
    from .RecogniseSQLExFunctions import mainRemovePerson
    mainRemovePerson(settings.DB_INFO, id, settings.PATH_IMAGES)
    return redirect('home')

# def edit(request, id):
#     try:
#         person = Person.objects.get(id=id)
#
#         if request.method == "POST":
#             person.name = request.POST.get("fio")
#             person.age = request.POST.get("age")
#             person.gender = request.POST.get("gender")
#             person.save()
#             return HttpResponseRedirect("/")
#         else:
#             return render(request, "edit.html", {"person": person})
#     except Person.DoesNotExist:
#         return HttpResponseNotFound("<h2>Person not found</h2>")


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
        # sendMessage(msg)

        # добавить сохранение фото в постоянном месте
        # if not isOld:
        #     from shutil import move, copy, copy2, rmtree
        #     print(f"try to copy:\n from {tmpFilePath}\nto {pathDBImages}")
        #     move(tmpFilePath, pathDBImages)



        return HttpResponse(f"Принято!\nРезультат:\n{msg}")
    return HttpResponse("Try to use POST")

