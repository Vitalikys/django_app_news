from django import forms
from django.contrib.auth.models import User # default django Model in admin-user
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from captcha.fields import CaptchaField

from .models import News, Reviews
import re
# https://djbook.ru/rel3.0/topics/forms/index.html

class UserLoginForm(AuthenticationForm):
    username = forms.CharField(label='User Name', widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'}))


# rename default fields,  не обовязково
class UserRegisterForm(UserCreationForm):
    username = forms.CharField(label='User Name', help_text='підказка для всіх', widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(label='фамилия', widget=forms.TextInput(attrs={'class': 'form-control'})),
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='Пароль ще раз', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label='E-mail', widget=forms.EmailInput(attrs={'class': 'form-control'}))
    # class Meta(UserCreationForm.Meta):
    class Meta:
        model = User   # default django Model in admin-user
        fields = ('username', 'last_name', 'password1', 'password2', 'email')

class NewsForm(forms.ModelForm):
    class Meta:
        model = News
        fields = 'title', 'content', 'category' #'__all__'рекомендується прописати всі =[ 'title', 'content', 'category']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows':6}),
            'category': forms.Select(attrs={'class': 'form-control'})
        }

    # def clean_title(self):
    #     title = self.cleaned_data['title']
    #     if re.match(r'\d',title):
    #         raise ValidationError('назва статті не повинна починатися з цифри')


class ContactFormMail(forms.Form):
    subject = forms.CharField(label='Тема', widget=forms.TextInput(attrs={'class': 'form-control'}))
    content = forms.CharField(label='Текст повідомлення', widget=forms.Textarea(attrs={'class':'form-control', "rows":3}))
    captcha = CaptchaField()  #https://django-simple-captcha.readthedocs.io/en/latest/usage.html

'''
def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.pop('autofocus')
уберёт автофокус'''

class ReviewForm(forms.ModelForm):
    """Форма Відгуків"""
    class Meta:
        model = Reviews
        fields = ("name", "email", "text")
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "text": forms.Textarea(attrs={"class": "form-control border", 'rows':3})
        }