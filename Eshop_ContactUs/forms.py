from django import forms
from django.core import validators
from django.forms import ModelForm
from .models import OpinionModel
from django.utils.translation import gettext_lazy as _

class OpinionForm(ModelForm):
    class Meta:
        model = OpinionModel
        fields = ['opinion']
        labels = {
            'opinion': _(''),
        }

class ContactForm(forms.Form):
    email = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control form-control-sm mt-1',
            'placeholder':'ایمیل خود را وارد کنید:'
        }),
        validators=[
            validators.MaxLengthValidator(limit_value=40, message='ایمیل نباید بیش از <span class="number">40</span> کاراکتر باشد.'),
            validators.MinLengthValidator(limit_value=7, message='ایمیل نباید کمتر از <span class="number">7</span> کاراکتر باشد.'),
        ]
    )
    name = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control form-control-sm mt-1',
            'placeholder':'نام خود را وارد کنید:'
        }),
        validators=[
            validators.MaxLengthValidator(limit_value=25, message='نام نباید بیش از <span class="number">25</span> کاراکتر باشد.'),
            validators.MinLengthValidator(limit_value=4, message='نام نباید کمتر از <span class="number">4</span> کاراکتر باشد.'),
        ]
    )
    subject = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control form-control-sm mt-1',
            'placeholder':'موضوع پیام'
        }),
        validators=[
            validators.MaxLengthValidator(limit_value=25, message='عنوان پیام نباید بیش از <span class="number">25</span> کاراکتر باشد.'),
            validators.MinLengthValidator(limit_value=4, message='عنوان پیام نباید کمتر از <span class="number">4</span> کاراکتر باشد.'),
        ]
    )
    msg = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control form-control-sm mt-1',
            'placeholder':'متن پیام شما'
        }),
        validators=[
            validators.MinLengthValidator(limit_value=10, message='متن پیام نباید کمتر از <span class="number">10</span> کاراکتر باشد.'),
        ]
    )
