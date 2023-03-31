from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from users.models import User
from users.models import Profile

class UserCreateForm(forms.ModelForm):
    confirm_password = forms.CharField(widget=forms.widgets.PasswordInput(),validators=[validate_password])
    
    def clean(self):
        cleaned_data = super().clean()
        print(cleaned_data)
        if cleaned_data['confirm_password'] != cleaned_data['password']:
            raise ValidationError({
                'confirm_password': "Passwords don't match",
                'password': "Passwords don't match",
            })
        
        return cleaned_data

    class Meta:
        model = User
        fields = ['username', 'password', 'confirm_password']
        widgets = {
            'password': forms.PasswordInput(),
        }
    
    def save(self, commit: bool = False):
        user: User = super().save(False)
        user.set_password(user.password)
        user.save(commit)
        return user
        
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'avatar', 'bio']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs.update({'class': 'form-control'})
        self.fields['last_name'].widget.attrs.update({'class': 'form-control'})
        self.fields['bio'].widget.attrs.update({'class': 'form-control'})
        self.fields['avatar'].widget.attrs.update({'class': 'form-control-file'})
