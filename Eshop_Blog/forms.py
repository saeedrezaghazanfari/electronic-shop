from django import forms
from .models import Comment
from django.utils.translation import gettext_lazy as _

class msgForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['msg']
        labels = {
            'msg': _(''),
        }