from django import forms

class OrderForm(forms.Form):
    productId = forms.IntegerField(
        widget=forms.HiddenInput()
    )
    count = forms.IntegerField(
        widget=forms.NumberInput(attrs={
            'class':'form-control form-control-sm form-size-small number',
        }),
        initial=1,
        label='<b>تعداد و رنگ</b> محصول خود را وارد کنید:'
    )
