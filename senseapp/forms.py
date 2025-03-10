from django import forms

class weather_input(forms.Form):
    api_key = forms.CharField(max_length=50)
    city_code = forms.IntegerField()
    