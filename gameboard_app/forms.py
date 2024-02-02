from django import forms
from . models import Question

class UploadFileForm(forms.ModelForm):
    class Meta:
        model = Question
        # fields = ['file', 'pic']
        fields = ['pic']