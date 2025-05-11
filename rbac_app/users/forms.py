# import form class from django
from django import forms

# import GeeksModel from models.py
from .models import *


# create a ModelForm
class RecordForm(forms.ModelForm):
    # specify the name of model to use
    class Meta:
        model = Record
        fields = "__all__"
