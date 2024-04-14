from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Image, Product, Toxicant


def validate_email_unique(value):
    result = User.objects.filter(email=value).exists()
    if result:
        raise forms.ValidationError(f"Email address {value} already exists, must be unique!")


class SignupForm(UserCreationForm):
    email = forms.EmailField(required=True, validators=[validate_email_unique])

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")


class LoginForm(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)

class SelectLanguageForm(forms.Form):
    ENGLISH = "en"
    POLISH = "pl"
    LANGUAGES_CHOICES = (
        (ENGLISH, "English"),
        (POLISH, "Polish"))
    language = forms.ChoiceField(choices=LANGUAGES_CHOICES)

def validate_space_between_words(name):
    if " " in name.strip():
        if len(name.strip()) - len(name.strip().replace(" ", "")) != 1:
            raise forms.ValidationError("Food additive name should have only one space between words!")

class SearchAdditiveForm(SelectLanguageForm):
    additive_name = forms.CharField(required=True, max_length=50, validators=[validate_space_between_words],
                                    error_messages={"required": "Food additive name cannot be an empty string!"})


def validate_comma_empty_name_space_between_words(names):
    if "," not in names:
        raise forms.ValidationError("Food additive names must be separated by commas!")
    for name in names.split(","):
        if len(name.strip()) == 0:
            raise forms.ValidationError("Food additive name cannot be an empty string!")
        validate_space_between_words(name)


class SearchAdditivesForm(SelectLanguageForm):
    additive_names = forms.CharField(required=True, max_length=2000, validators=[validate_comma_empty_name_space_between_words],
                                     error_messages={"required": "Food additive names cannot be an empty string!"})


class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = "__all__"


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ("name", "manufacturer", "toxicants")

    def __init__(self, *args, **kwargs):
        toxicants_ids = kwargs.pop("toxicants_ids", None)
        super().__init__(*args, **kwargs)

        if toxicants_ids:
            self.fields["toxicants"].queryset = Toxicant.objects.filter(id__in=toxicants_ids)
            self.fields["toxicants"].initial = self.fields["toxicants"].queryset





