from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.template.defaultfilters import filesizeformat

from app.models import Profile, Question, Answer, Tag


class LoginForm(forms.Form):
    username = forms.CharField(label="Login")
    password = forms.CharField(min_length=8, widget=forms.PasswordInput, label="Password")

    def clean_username(self):
        username = self.cleaned_data['username']
        if ' ' in username:
            raise forms.ValidationError('Username includes spaces')
        return username

    def clean_password(self):
        password = self.cleaned_data['password']
        if ' ' in password:
            raise forms.ValidationError('Password includes spaces')
        return password


def size(img):
    max_size = 100 * 1024
    if img.size > max_size:
        raise forms.ValidationError('File so big (%s). Max filesize - %s' %
                                    (filesizeformat(img.size), filesizeformat(max_size)))


class RegisterForm(forms.ModelForm):
    username = forms.CharField(label="Login")
    email = forms.EmailField()
    first_name = forms.CharField(label="First name")
    last_name = forms.CharField(label="Last name")
    password = forms.CharField(widget=forms.PasswordInput, label="Password")
    password_repeat = forms.CharField(widget=forms.PasswordInput, label="Repeat password")
    avatar = forms.ImageField(label="Upload avatar", required=False, validators=[size])

    def clean_first_name(self):
        first_name = self.cleaned_data['first_name']
        if ' ' in first_name:
            raise forms.ValidationError('First name includes spaces')
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data['last_name']
        if ' ' in last_name:
            raise forms.ValidationError('Last name includes spaces')
        return last_name

    def clean_password_repeat(self):
        password_repeat = self.cleaned_data['password_repeat']
        if not password_repeat:
            raise forms.ValidationError('Input password repeatedly')
        return password_repeat

    def clean(self):
        super().clean()
        password = self.cleaned_data['password']
        password_repeat = self.cleaned_data['password_repeat']
        if ' ' in password:
            errors = {'password': ValidationError('Password includes space')}
            raise forms.ValidationError(errors)

        if password and password_repeat and password != password_repeat:
            errors = {'password_repeat': ValidationError('The entered passwords do not match'),
                      'password': ValidationError('')}
            raise ValidationError(errors)

    def save(self, commit=True):
        self.cleaned_data.pop('password_repeat')
        avatar = self.cleaned_data.get('avatar')
        self.cleaned_data.pop('avatar')
        user = User.objects.create_user(**self.cleaned_data)
        if avatar:
            return Profile.objects.create(user=user, image=avatar)
        else:
            return Profile.objects.create(user=user)

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password')


class SettingsForm(forms.ModelForm):
    password = forms.CharField(required=False, widget=forms.PasswordInput, label="Password")
    password_repeat = forms.CharField(required=False, widget=forms.PasswordInput, label="Repeat password")
    avatar = forms.ImageField(label="Upload avatar", required=False, validators=[size])

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'avatar')

    def save(self, commit=True):
        user = super().save()

        profile = user.profile
        profile.image = self.cleaned_data['avatar']
        profile.save()

        return user