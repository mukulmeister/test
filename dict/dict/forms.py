from django import forms
class InputForm(forms.Form):
    City = forms.CharField(max_length=200)