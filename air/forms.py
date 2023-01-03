from django.forms import ModelForm, CharField, TextInput, PasswordInput, Select, DateTimeInput, NumberInput
from django.contrib.auth.forms import AuthenticationForm

from .models import *


class LoginUserForm(AuthenticationForm):
    username = CharField(label='Логін', widget=TextInput(attrs={'class': 'form-input'}))
    password = CharField(label='Пароль', widget=PasswordInput(attrs={'class': 'form-input'}))


class MyDataForm(ModelForm):

    class Meta:
        model = AirData
        fields = ('datetime', 'city', 'pollutant', 'concentration', 'sensor',)

        widgets = {
            'datetime': DateTimeInput(attrs={
                'type': 'text',
                'class': 'form-control',
                'required': '',
            }),
            'city': Select(attrs={
                'required': '',
                'class': 'form-select',
            }),
            'pollutant': Select(attrs={
                'required': '',
                'class': 'form-select',
            }),
            'concentration': TextInput(attrs={
                'class': 'form-control',
            }),
            'sensor': Select(attrs={
                'required': '',
                'class': 'form-select',
            }),
        }


class SensorDataForm(ModelForm):

    class Meta:
        model = AirData
        fields = ('city', 'pollutant')

        widgets = {
            'city': Select(attrs={
                'required': '',
                'class': 'form-select',
                'id': 'city'
            }),
            'pollutant': Select(attrs={
                'required': '',
                'class': 'form-select',
                'id': 'pollutant'
            })
        }


class YearReportForm(ModelForm):

    class Meta:
        model = AirData
        fields = ('city', 'pollutant')

        widgets = {
            'city': Select(attrs={
                'required': '',
                'class': 'form-select',
                'id': 'city'
            }),
            'pollutant': Select(attrs={
                'required': '',
                'class': 'form-select',
                'id': 'pollutant'
            })
        }