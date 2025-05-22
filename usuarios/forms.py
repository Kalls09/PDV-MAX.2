from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm as BaseUserCreationForm, UserChangeForm as BaseUserChangeForm
from django.core.validators import RegexValidator
from .models import Users

# Validador para senha forte
strong_password_validator = RegexValidator(
    regex=r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$',
    message="A senha deve conter ao menos 8 caracteres, incluindo uma letra maiúscula, uma minúscula, um número e um caractere especial."
)

class VendedorForm(forms.ModelForm):
    senha = forms.CharField(
        widget=forms.PasswordInput,
        label="Senha",
        validators=[strong_password_validator]
    )

    class Meta:
        model = Users
        fields = ['first_name', 'last_name', 'email', 'senha']
        labels = {
            'first_name': 'Nome',
            'last_name': 'Sobrenome',
            'email': 'Email',
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if Users.objects.filter(email=email).exists():
            raise ValidationError("Email já cadastrado.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data['email']
        user.set_password(self.cleaned_data['senha'])
        user.cargo = "V"
        if commit:
            user.save()
        return user

class UserCreationForm(BaseUserCreationForm):
    class Meta(BaseUserCreationForm.Meta):
        model = Users
        fields = ('username', 'email', 'first_name', 'last_name')

class UserChangeForm(BaseUserChangeForm):
    class Meta(BaseUserChangeForm.Meta):
        model = Users
        fields = ('username', 'email', 'first_name', 'last_name')
