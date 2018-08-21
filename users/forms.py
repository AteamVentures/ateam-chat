
import re

from django import forms
from django.core import validators
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse, reverse_lazy
from django.contrib.auth import authenticate, get_user_model


User = get_user_model()


EMAIL_DOMAIN_CHOICES = (
    ('', '이메일 선택'),
    ('hanmail.net', 'hanmail.net'),
    ('daum.net', 'daum.net'),
    ('naver.com', 'naver.com'),
    ('gmail.com', 'gmail.com'),
)


class LoginForm(forms.Form):
    username = forms.CharField(label='ID',
                               max_length=254,
                               widget=forms.TextInput(attrs={
                                   'placeholder': 'ID',
                                   'class': 'form-control'
                               }),
                               error_messages={
                                   'required': 'ID를 입력해주세요.'})
    password = forms.CharField(label='비밀번호',
                               widget=forms.PasswordInput(attrs={
                                   'placeholder': '비밀번호',
                                   'class': 'form-control'
                               }),
                               error_messages={
                                   'required': '비밀번호를 입력해주세요.'})

    def __init__(self, request=None, *args, **kwargs):
        """
        The 'request' parameter is set for custom auth use by subclasses.
        The form data comes in via the standard 'data' kwarg.
        """
        self.request = request
        self.user_cache = None
        super(LoginForm, self).__init__(*args, **kwargs)

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        self.user_cache = authenticate(username=username, password=password)
        return self.cleaned_data

    def get_user_id(self):
        if self.user_cache:
            return self.user_cache.id
        return None

    def get_user(self):
        return self.user_cache


class SignupForm(forms.ModelForm):
    """
    회원가입 form
    """

    password1 = forms.CharField(required=True,
                                max_length=20,
                                label='비밀번호',
                                widget=forms.PasswordInput(
                                    attrs={
                                        'class': 'form-control',
                                        'placeholder': '비밀번호는 6~20자리'}))

    password2 = forms.CharField(required=True,
                                max_length=20,
                                label='비밀번호 재입력',
                                widget=forms.PasswordInput(
                                    attrs={
                                        'class': 'form-control',
                                        'placeholder': '비밀번호 재입력 6~20자리'}))
    email_name = forms.CharField(required=True,
                                 max_length=50,
                                 widget=forms.TextInput(
                                     attrs={
                                         'class': 'form-control',
                                         'placeholder': '이메일'
                                     }))
    email_domain = forms.CharField(required=True,
                                   max_length=50,
                                   widget=forms.TextInput(
                                       attrs={
                                           'class': 'form-control',
                                           'placeholder': '직접 입력'}))

    email_domain_choice = forms.ChoiceField(required=False,
                                            choices=EMAIL_DOMAIN_CHOICES,
                                            widget=forms.Select(
                                                attrs={
                                                    'class': 'form-control'}))

    class Meta:
        model = User
        fields = ('username', 'phone', 'name', 'display_name')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control',
                                               'placeholder': 'ID는 5자리 이상'}),
            'phone': forms.TextInput(attrs={'class': 'form-control',
                                            'placeholder': '연락처'}),
            'name': forms.TextInput(attrs={'class': 'form-control',
                                           'placeholder': '이름'}),
            'display_name': forms.TextInput(attrs={'class': 'form-control',
                                                   'placeholder': '닉네임 최대 20자리'})
        }

    def clean_username(self):
        """
        Checks for existing users with the supplied username.
        """
        username = self.cleaned_data['username']
        if User._default_manager.filter(username__iexact=username).exists():
            raise forms.ValidationError(
                'ID가 이미 존재합니다.'
            )
        return username

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        new_phone = re.sub('\D', '', phone)
        return new_phone

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 != password2:
            raise forms.ValidationError(
                '비밀번호가 일치하지 않습니다.')
        return password2

    def clean_redirect_url(self):
        url = self.cleaned_data['redirect_url'].strip()
        return reverse_lazy("account:signup_success")

    def clean(self):
        super(SignupForm, self).clean()
        email_name = self.cleaned_data.get('email_name')
        email_domain = self.cleaned_data.get('email_domain')
        email = "{0}@{1}".format(email_name, email_domain)

        try:
            validators.validate_email(email)
        except ValidationError:
            raise forms.ValidationError(
                self.add_error('email_name', '이메일 주소를 정확히 입력해주세요.'))

    def save(self, commit=True):
        user = super(SignupForm, self).save(commit=False)
        user.set_password(self.cleaned_data.get('password1'))
        user.country = self.cleaned_data.get('country')

        email_name = self.cleaned_data.get('email_name')
        email_domain = self.cleaned_data.get('email_domain')
        user.email = "{0}@{1}".format(email_name, email_domain)

        if commit:
            user.save()
        return user
