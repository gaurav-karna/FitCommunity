from django import forms
# from django.contrib.auth.forms import UserCreationForm, UserChangeForm
# from django.db import transaction

from .models import Event, CommunityAdmin, Community, User



class UserForm(forms.ModelForm):

    # from the User class
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(max_length=254, required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)

    class Meta():
        model = User
        fields = [
            'first_name',
            'last_name',
            'email',
            'password',
        ]

    def clean_email(self, *args, **kwargs):
        email = self.cleaned_data.get("email")
        email_qs = User.objects.filter(email=email)
        if email_qs.exists():
            raise forms.ValidationError("This email already exists.")
        return email