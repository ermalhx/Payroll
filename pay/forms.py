from django import forms

class PayrollUploadForm(forms.Form):
    file = forms.FileField(required=True, label="Ngarko file ne excel")


class PagaForm(forms.Form):
    gross_salary = forms.IntegerField(
        max_value=9999999999,  # Set a reasonable max value for the salary
        widget=forms.NumberInput(attrs={'class': 'form-control d-inline-block w-auto'}),
        label="Paga Bruto",
    )
    deklarata = forms.BooleanField(
        required=False, 
        initial=False, 
        label="Ke plotesuar deklaraten",
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input d-inline-block'}),
    )

    # Customizing the labels with a CSS class to make them inline
    def __init__(self, *args, **kwargs):
        super(PagaForm, self).__init__(*args, **kwargs)
        self.fields['gross_salary'].label_tag = forms.widgets.TextInput(attrs={'class': 'form-label d-inline-block me-2'})
        self.fields['deklarata'].label_tag = forms.widgets.TextInput(attrs={'class': 'form-label d-inline-block me-2'})