from django.forms import forms
from .models import EmailModel,CodeModel

class EmailForm(forms.Form):

    class Meta:
        model = EmailModel
        fields = '__all__'


class CodeField(forms.Form):

    class Meta:
        model = CodeModel
        fields = '__all__'