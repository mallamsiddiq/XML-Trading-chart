import django
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

User = django.contrib.auth.get_user_model()

class RegistrationForm(UserCreationForm):
    # print(4567)
    email = forms.EmailField(max_length=100, required=True, help_text="Required. Enter a valid email address.")

    class Meta:
        model = User
        fields = ['email', 'password1', 'password2']

    # def clean_email(self):
    #     email = self.cleaned_data.get("email")
    #     if User.objects.filter(email__iexact=email).exists():
    #         self.add_error("email", _("A user with this email already exists."))
    #     return email


class LoginForm(forms.Form):
    remember_me = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
    )

    email = forms.EmailField(max_length=100, required=True, help_text="Required. Enter a valid email address.")
    password = forms.CharField(max_length=50, required=True, help_text="Required. Enter your password.")

    class Meta:
        model = User
        fields = ['email', 'password', 'remember_me']

class BaseLoginForm(AuthenticationForm):
    remember_me = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
    )
    email = forms.EmailField(max_length=100, required=True, help_text="Required. Enter a valid email address.")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'username' in self.fields:
            del self.fields['username']

    class Meta:
        model = User  # Use your custom User model
        fields = ('email', 'password')