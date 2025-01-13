from django import forms

class PayrollUploadForm(forms.Form):
    file = forms.FileField(required=True, label="Ngarko file ne excel")