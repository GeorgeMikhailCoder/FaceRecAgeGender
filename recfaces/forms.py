from django import forms
from .models import Person
from django.utils.translation import ugettext as _



class loadImageForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = ['fio', 'age', 'gender', 'imgPath']






