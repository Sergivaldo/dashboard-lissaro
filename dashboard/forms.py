from django import forms

from .models import BlingUser


class LoginForm(forms.Form):
    username = forms.CharField(label="Usuário")
    password = forms.CharField(label="Senha",
                               widget=forms.PasswordInput()
                               )


class RegisterForm(forms.ModelForm):
    class Meta:
        model = BlingUser
        fields = ['user_name', 'password', 'api_key']
        labels = {
            'user_name': 'Usuário ou e-mail',
            'password': 'Senha',
            'api_key': 'Chave da API'
        }
        widgets = {
            'password': forms.PasswordInput(render_value=True),
            'api_key': forms.PasswordInput(render_value=True)
        }
