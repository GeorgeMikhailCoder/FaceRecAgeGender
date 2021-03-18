# posts/urls.py
from django.urls import path

from .views import *

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('add_person/', CreatePostView.as_view(extra_context={"messages": settings.MESSAGES}), name='add_person'),
    path('delete/<int:id>/', delete),

    path('hook/', catchHook, name='hook')
]