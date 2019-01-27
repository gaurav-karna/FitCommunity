from django import forms
# from django.contrib.auth.forms import UserCreationForm, UserChangeForm
# from django.db import transaction

from .models import Event, CommunityAdmin, Community, User, Member, Comments

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

    def save(self, *args, **kwargs):
        data = self.cleaned_data
        user = User(username=data['email'], email=data['email'], first_name=data['first_name'],
                    last_name=data['last_name'], password=data['password'], )
        user.set_password(data['password'])
        user.member_profile = None
        user.admin_profile = None
        user.save()
        return user

class MemberSignupForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = [
            'Bio',
            'Age',
            'Gender',
            'Weight',
            'Height',
            'Ethnicity',
            'Known_Conditions'
        ]

# class CommunityAdminForm(forms.ModelForm):
#     class Meta:
#         model = CommunityAdmin
#         fields = [
#             'Community'
#         ]

class CommunityForm (forms.ModelForm):
    class Meta:
        model = Community
        fields = [
            'Required_Email',
            'Location'
        ]

class EventForm (forms.ModelForm):
    class Meta:
        model = Event
        fields = [
            'Title',
            'Start_Date',
            'End_Date',
            'Category',
            'Registration_Deadline',
            'Short_Description',
            'Location',
            'Event_Picture',
            'Max_Registration',
            'Registration_Open',
            'Event_Details'
        ]

class CommentsForm(forms.ModelForm):
    class Meta:
        model = Comments
        fields = [
            'Forum_Post'
        ]