from django import forms
from django.contrib.auth.forms import AuthenticationForm

class BootstrapAuthForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(BootstrapAuthForm, self).__init__(*args, **kwargs)

        widgets = {
            'username': forms.TextInput(attrs={'class': 'span4'}),
            'password': forms.PasswordInput(attrs={'class': 'span4'}),
        }
        for name in self.fields:
            if name in widgets:
                self.fields[name].widget = widgets[name]
