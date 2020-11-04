from django import forms
from django.core import validators


class EditForm(forms.Form):
    firstname = forms.CharField(label='<b class="text-muted">نام</b>', widget=forms.TextInput(attrs={'class':'form-control form-control-sm', 'placeholder':'نام خود را وارد کنید:'}),required=False)
    lastname = forms.CharField(label='<b class="text-muted">نام خانوادگی</b>', widget=forms.TextInput(attrs={'class':'form-control form-control-sm', 'placeholder':'نام خانوادگی خود را وارد کنید:'}), required=False)
    phone = forms.IntegerField(label='<b class="text-muted">شماره تماس</b>', widget=forms.NumberInput(attrs={'class':'form-control form-control-sm', 'placeholder':'شماره تماس خود را وارد کنید:'}), required=False)
    bio = forms.CharField(label='<b class="text-muted">بیوگرافی</b>', widget=forms.Textarea(attrs={'class':'form-control form-control-sm p-4', 'placeholder':'بیوگرافی خود را وارد کنید:'}),required=False)
    webName = forms.CharField(label='<b class="text-muted">نام وبسایت</b>', widget=forms.TextInput(attrs={'class':'form-control form-control-sm', 'placeholder':' نام وبسایت مربوطه را وارد کنید:'}),required=False)

class ChangePw(forms.Form):
    old_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class':'form-control form-control-sm wow animate__animated animate__fadeInUp',
            'data-wow-delay':'0.4s',
            'placeholder':'رمزعبور قدیم:'
        }),
        label='رمزعبور <b>فعلی</b> را وارد کنید:',
        validators=[
            validators.MaxLengthValidator(limit_value=25, message='رمزعبور نباید بیش از <span class="number">25</span> کاراکتر باشد.'),
            validators.MinLengthValidator(limit_value=6, message='رمزعبور نباید کمتر از <span class="number">6</span> کاراکتر باشد.'),
        ]
    )
    new_pw_1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class':'form-control form-control-sm wow animate__animated animate__fadeInUp',
            'data-wow-delay':'0.8s',
            'placeholder':'رمز عبور جدید:'
        }),
        label='رمزعبور <b>جدید</b> را وارد کنید:',
        validators=[
            validators.MaxLengthValidator(limit_value=25, message='رمزعبور نباید بیش از <span class="number">25</span> کاراکتر باشد.'),
            validators.MinLengthValidator(limit_value=6, message='رمزعبور نباید کمتر از <span class="number">6</span> کاراکتر باشد.'),
        ]
    )
    new_pw_2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class':'form-control form-control-sm wow animate__animated animate__fadeInUp',
            'data-wow-delay':'0.8s',
            'placeholder':'تکرار رمز عبور جدید:'
        }),
        label='رمزعبور <b>جدید</b> را <b>دوباره</b> وارد کنید:',
        validators=[
            validators.MaxLengthValidator(limit_value=25, message='رمزعبور نباید بیش از <span class="number">25</span> کاراکتر باشد.'),
            validators.MinLengthValidator(limit_value=6, message='رمزعبور نباید کمتر از <span class="number">6</span> کاراکتر باشد.'),
        ]
    )
    def clean(self):
        pw1 = self.cleaned_data.get('new_pw_1')
        pw2 = self.cleaned_data.get('new_pw_2')
        if pw1 != pw2:
            raise forms.ValidationError('باید دو رمز عبور جدید برابری داشته باشند !!')
        return pw2
