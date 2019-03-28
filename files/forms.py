from django import forms

from .models import FCSFiles


class FCSForm(forms.ModelForm):
    class Meta:
        model = FCSFiles
        fields = ( 'pdf' )
