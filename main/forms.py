from .models import *

from django import forms

class LinkForm(forms.ModelForm):
    class Meta:
        model=Rank
        fields = ['Alink','Flink']