from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError
import datetime
from .models import *


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Логін', widget=forms.TextInput(attrs={'class': 'form-input'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))


class MyDataForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['city'].empty_label = "Не обрано"
        self.fields['pollutant'].empty_label = "Не обрано"
        self.fields['sensor'].empty_label = "Не обрано"

    class Meta:
        model = AirData
        fields = ('datetime', 'city', 'pollutant', 'concentration', 'sensor')

        widgets = {
            'datetime': forms.DateTimeInput(attrs={'type': 'text', 'class': 'form-control'}),
            'city': forms.Select(attrs={'class': 'form-select'}),
            'pollutant': forms.Select(attrs={'class': 'form-select'}),
            'concentration': forms.TextInput(attrs={'class': 'form-control'}),
            'sensor': forms.Select(attrs={'class': 'form-select'}),
        }

    def clean_concentration(self):
        concentration = self.cleaned_data['concentration']
        if not isinstance(concentration, int | float):
            raise ValidationError('Введіть число')
        return concentration

    def clean_datetime(self):
        date_time = self.cleaned_data['datetime']
        try:
            datetime.datetime.strptime(date_time, '%m/%d/%Y %H:%M:%S')
        except ValidationError:
            raise ValidationError('Введіть дату та час в форматі "DD/MM/YYYY HH:MI:SS"')
        finally:
            return date_time


class SensorDataForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['city'].empty_label = "Не обрано"
        self.fields['pollutant'].empty_label = "Не обрано"

    class Meta:
        model = AirData
        fields = ('city', 'pollutant')

        widgets = {
            'city': forms.Select(attrs={'class': 'form-select','id': 'city'}),
            'pollutant': forms.Select(attrs={'class': 'form-select','id': 'pollutant'})
        }


class YearReportForm(forms.Form):
    city = forms.ModelChoiceField(queryset=City.objects.all(), label="Місто", empty_label="Не обрано",
                                  widget=forms.Select(attrs={'class': 'form-select'}))
    pollutant = forms.ModelChoiceField(queryset=Pollutant.objects.all(), label="Забрудник", empty_label="Не обрано",
                                       widget=forms.Select(attrs={'class': 'form-select'}))
    year = forms.IntegerField(min_value=1980, max_value=datetime.datetime.now().year, label="Рік",
                              widget=forms.NumberInput(attrs={'class': 'form-input'}))
