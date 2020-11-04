from django import forms
from django.contrib.auth.models import User
from django.core import validators

class LoginForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control form-control-sm wow animate__animated animate__fadeInUp',
            'data-wow-delay': '0.5s',
            'placeholder': 'ایمیل خود را وارد کنید'
        }),
        label='<b>ایمیل</b> خود را وارد کنید:',
        validators=[
            validators.MaxLengthValidator(limit_value=225, message='نام کاربری نباید بیش از <span class="number">225</span> کاراکتر باشد.'),
            validators.MinLengthValidator(limit_value=7, message='نام کاربری نباید کمتر از <span class="number">7</span> کاراکتر باشد.'),
        ]
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class':'form-control form-control-sm wow animate__animated animate__fadeInUp',
            'data-wow-delay':'0.8s',
            'placeholder':'رمز عبور خود را به صورت لاتین وارد کنید'
        }),
        label='<b>پسورد</b> خود را وارد کنید:',
        validators=[
            validators.MaxLengthValidator(limit_value=25, message='رمزعبور نباید بیش از <span class="number">25</span> کاراکتر باشد.'),
            validators.MinLengthValidator(limit_value=6, message='رمزعبور نباید کمتر از <span class="number">6</span> کاراکتر باشد.'),
        ]
    )

class RegisterForm(forms.Form):

    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control form-control-sm wow animate__animated animate__fadeIn',
            'data-wow-delay': '0.5s',
            'placeholder': 'نام کاربری خود را وارد کنید'
        }),
        label='<b>نام کاربری</b> خود را وارد کنید:',
        validators=[
            validators.MaxLengthValidator(limit_value=25, message='نام کاربری نباید بیش از <span class="number">25</span> کاراکتر باشد.'),
            validators.MinLengthValidator(limit_value=4, message='نام کاربری نباید کمتر از <span class="number">4</span> کاراکتر باشد.'),
        ]
    )
    email = forms.CharField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control form-control-sm wow animate__animated animate__fadeIn',
            'data-wow-delay': '0.7s',
            'placeholder': 'مانند: info@gmail.com'
        }),
        label='<b>ایمیل</b> خود را وارد کنید:',
        validators=[
            validators.MaxLengthValidator(limit_value=40, message='ایمیل نباید بیش از <span class="number">40</span> کاراکتر باشد.'),
            validators.MinLengthValidator(limit_value=7, message='ایمیل نباید کمتر از <span class="number">7</span> کاراکتر باشد.'),
        ]
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class':'form-control form-control-sm wow animate__animated animate__fadeIn',
            'data-wow-delay':'0.9s',
            'placeholder':'رمز عبور خود را به صورت لاتین وارد کنید'
        }),
        label='<b>پسورد</b> خود را وارد کنید:',
        validators=[
            validators.MaxLengthValidator(limit_value=25, message='رمزعبور نباید بیش از <span class="number">25</span> کاراکتر باشد.'),
            validators.MinLengthValidator(limit_value=6, message='رمزعبور نباید کمتر از <span class="number">6</span> کاراکتر باشد.'),
        ]
    )
    re_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class':'form-control form-control-sm wow animate__animated animate__fadeIn',
            'data-wow-delay':'1.1s',
            'placeholder':'رمز عبور خود را دوباره وارد کنید'
        }),
        label='<b>پسورد</b> خود را <b>دوباره</b> وارد کنید:',
    )
    def clean_username(self):
        username = self.cleaned_data.get('username')
        exist = User.objects.filter(username__iexact=username).first()
        if exist:
            raise forms.ValidationError('نام کاربری دیگری انتخاب کنید.')
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        exist = User.objects.filter(email__iexact=email).first()
        if exist:
            raise forms.ValidationError('ایمیل دیگری انتخاب کنید.')
        return email

    def clean_re_password(self):
        pass1 = self.cleaned_data.get('password')
        pass2 = self.cleaned_data.get('re_password')
        if pass1 != pass2:
            raise forms.ValidationError('رمزعبورها باید یکسان باشند.')
        return pass1

class Report_Spam(forms.Form):
    email = forms.CharField(
        widget=forms.HiddenInput()
    )
    username = forms.CharField(
        widget=forms.HiddenInput()
    )
    subject = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control form-control-sm wow animate__animated animate__fadeIn',
            'data-wow-delay': '0.6s',
            'placeholder': 'عنوان خطای خود را وارد کنید'
        }),
        label='<b>عنوان خطای</b> خود را وارد کنید:',
        validators=[
            validators.MaxLengthValidator(limit_value=25, message='عنوان خطا نباید بیش از <span class="number">25</span> کاراکتر باشد.'),
            validators.MinLengthValidator(limit_value=4, message='عنوان خطا نباید کمتر از <span class="number">4</span> کاراکتر باشد.'),
        ]
    )
    # fileImage = forms.FileField(
    #     widget=forms.FileInput(attrs={
    #         'class': 'wow animate__animated animate__fadeIn',
    #         'data-wow-delay': '1s',
    #     }),
    #     label='تصویر خطا را وارد کنید:'
    # )
    massage = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control form-control-sm wow animate__animated animate__fadeIn p-4',
            'data-wow-delay': '0.8s',
            'placeholder': 'متن پیام خود را وارد کنید'
        }),
        label='<b>متن پیام</b> خود را وارد کنید:',
        validators=[
            validators.MinLengthValidator(limit_value=4, message='متن پیام نباید کمتر از <span class="number">10</span> کاراکتر باشد.'),
        ]
    )