from django import forms
from .models import User
from django.contrib.auth.forms import AuthenticationForm

class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for each in self.visible_fields():
            each.field.widget.attrs['class'] = 'form-control'


class UserForm(forms.ModelForm):
    # email = forms.EmailField()
    password = forms.CharField(label='密碼',widget=forms.PasswordInput)
    confirm_password = forms.CharField(label='密碼確認',widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = User.REQUIRED_FIELDS

class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='密碼', widget=forms.PasswordInput)
    password2 = forms.CharField(label='密碼確認', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = [User.USERNAME_FIELD, 'password1', 'password2'] + User.REQUIRED_FIELDS
        # fields += ['gender', 'daily_disposable', 'was_green_tableware']
        # fields = '__all__'

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user
