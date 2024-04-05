from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


def validate_email_unique(value):
    result = User.objects.filter(email=value).exists()
    if result:
        raise forms.ValidationError(f"Email address {value} already exists, must be unique!")


class SignupForm(UserCreationForm):
    email = forms.EmailField(required=True, validators=[validate_email_unique])

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

        def save(self, commit=True):
            user = super(CustomUserCreationForm, self).save(commit=False)
            user.email = self.cleaned_data['email']
            if commit:
                user.save()
            return user


class LoginForm(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)


Languages = (
    (1, 'English'),
    (2, 'Polish')
)


class SearchAdditiveForm(forms.Form):
    additive_name = forms.CharField(required=True, max_length=50,
                                    error_messages={'required': "Food additive name cannot be an empty string!"})
    language = forms.ChoiceField(choices=Languages)


def validate_comma_and_empty_name(names):
    if ',' not in names:
        raise forms.ValidationError("Food additive names must be separated by commas!")
    for name in names.split(","):
        if len(name.strip()) == 0:
            raise forms.ValidationError("Food additive name cannot be an empty string!")

class SearchAdditivesForm(forms.Form):
    additive_names = forms.CharField(required=True, max_length=2000, validators=[validate_comma_and_empty_name],
                                     error_messages={'required': "Food additive name cannot be an empty string!"})
    language = forms.ChoiceField(choices=Languages)
