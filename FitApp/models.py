from _datetime import datetime
from django.db import models
from django.core.validators import EmailValidator, MinValueValidator, MaxValueValidator
# from django.contrib.auth import get_user_model
from django.db import transaction
from django.conf import settings

from places.fields import PlacesField

from django.contrib.auth.models import AbstractUser, BaseUserManager

from django.contrib.auth.models import User

# from django.utils import timezone

# Create your models here.

# Event Class - what users will create to invite people to

class User(AbstractUser):
    pass

# This is what will be in each Event

categories = (
    ('Sports', 'Sports'),
    ('Yoga / Meditation', 'Yoga / Meditation'),
    ('Cardio', 'Cardio'),
    ('Weight-Lifting', 'Weight-Lifting'),
    ('Aerobics', 'Aerobics')
)

ethnicities = (
    ('Caucasian', 'Caucasian'),
    ('African-American', 'African-American'),
    ('Asian', 'Asian'),
    ('South Asian', 'South Asian'),
    ('Latin-American', 'Latin-American'),
    ('European', 'European'),
    ('Middle-Eastern', 'Middle-Eastern'),
)

genders = (
    ('Male', 'Male'),
    ('Female', 'Female'),
    ('Rather Not Say', 'Rather Not Say'),
)

### Method to return path for image upload per user

def user_directory_path(instance, filename):
    return 'user_{0}/{1}'.format(instance.user.id, filename)

class Event(models.Model):
    class Meta:
        verbose_name_plural = 'Events'

    Created_At = models.DateTimeField(auto_now=False, auto_now_add=True, editable=False)

    File_Path = models.CharField(max_length=256, default=user_directory_path)

    Title = models.CharField(max_length=32)

    Short_Description = models.TextField(max_length=500, verbose_name='Add a short (< 500 characters) description of your event')

    Location = PlacesField(verbose_name='Enter a location for your event.')

    Event_Picture = models.ImageField(upload_to=user_directory_path)

    Start_Date = models.DateTimeField()

    End_Date = models.DateTimeField()

    Registration_Deadline = models.DateTimeField(verbose_name='Deadline for Registration', null=False)

    Max_Registration = models.SmallIntegerField(default=4, validators=[
        MinValueValidator(4, message='Minimum number of people per event is 4.'),
        MaxValueValidator(50, message='Maximum number of people per event is 50.'),
    ])

    Registration_Open = models.BooleanField(verbose_name='Open for Registration?', null=False)

    Category = models.CharField(choices=categories, max_length=24)

    Event_Details = models.TextField(max_length=2000, verbose_name='(Optional) Please keep this to under 2000 characters.', blank=True)

    # The 'comments_set' queryset will return each of the comments of an event. At the bottom of the event page, and at the top via
    # a button, a comment form will be rendered so that people can add to the discussion.
    # The view function will save the comment, and then refresh the same page (and the new comment will be added to the queryset)

    ''' All registered guests available via registrations_set'''

# Comment box will be rendered at the bottom of each event page
class Comments (models.Model):
    class Meta:
        verbose_name_plural = 'Comments'
    Forum_Post = models.CharField(max_length=1024, verbose_name='Something to say?')
    # created_at will be initialized when the comment is saved
    Created_At = models.DateTimeField(auto_now=False, auto_now_add=True, editable=False)

    # Foreign key to an Event (one event can have multiple comments, but one comment can only have one event)
    # This is on_delete, as there is no point maintaining comments if the event is deleted.
    Related_Event = models.ForeignKey(Event, on_delete=models.CASCADE, null=False)

### AUXILIARY METHODS ###
def check_registration(event):
    current = datetime.now()
    if (current > event.End_Date) or (current > event.Start_Date) or (current > event.Registration_Deadline):
        return False
    else:
        return True

class Community (models.Model):
    class Meta:
        verbose_name_plural = 'Communities'
    Location = PlacesField(unique=True)
    # Access details of the location from commands on: https://github.com/oscarmcm/django-places

    Required_Email = models.CharField(max_length=64, unique=True, null=True, blank=True, verbose_name='Is there a specific email address you would'
                                                                                           ' like your members to have? (format like @example.tld')

    # Administrators would have a Foreign Key to this class, since there can be many admins to one community, but only
    # one community per admin

    def __str__(self):
        return str(self.id)

class CommunityAdmin (models.Model):
    class Meta:
        verbose_name_plural = 'Community Administrators'

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='admin_profile')

    # Form for editing community will be INACCESSIBLE to Admins, and only editable by the SuperAdmin
    Community = models.ForeignKey(Community, on_delete=models.SET_NULL, null=True)

    # backend-attribute
    is_approved = models.BooleanField(default=False)

class Member (models.Model):
    class Meta:
        verbose_name_plural = 'Members'

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='member_profile')

    Bio = models.TextField(max_length=250, verbose_name='Biography: Please keep it under 250 characters',
                           default = "Hey, I am a member of FitCommunity", blank=False)

    Age = models.SmallIntegerField(default=12, validators=[
        MinValueValidator(12, message="You have to be at least 12 years old to use FitCommunity."),
        MaxValueValidator(120, message="You cannot use FitCommunity if you are over 120 years old.")
    ])

    Gender = models.CharField(max_length=16, choices=genders)

    Community = models.ForeignKey(Community, on_delete=models.SET_NULL, null=True)

    Weight = models.SmallIntegerField(verbose_name='Please enter your weight in kilograms', default=70, validators= [
        MinValueValidator(12, message="Minimum weight must be 12 kg."),
        MaxValueValidator(400, message="Maximum weight is 400 kg.")
    ])

    Height = models.SmallIntegerField(verbose_name='Please enter your height in centimeters', default=175, validators= [
        MinValueValidator(100, message="Minimum height must be 100 cm"),
        MaxValueValidator(300, message="Maximum height is 300 cm")
    ])

    BMI = models.SmallIntegerField(verbose_name='Body Mass Index')

    Ethnicity = models.CharField(max_length=32, choices=ethnicities)

    Known_Conditions = models.TextField(max_length=300, verbose_name='Are there any conditions you would like us to know? '
                                                                     'Please keep it under 300 characters', default='Not Applicable')

    # Displaying a member's events, is going to be accessed by a queryset:
    ''' registrations_set '''

    ## Backend Attributes ##

    # Community admin must approve the applicant
    is_approved = models.BooleanField(default=False)
    # Max number of registered events is 3
    event_limit = 3

class Registrations (models.Model):
    class Meta:
        verbose_name_plural = 'Registrations'

    ''' simply an intermediary model to connect members to events, but also allows for members to have multiple events
     - upon saving, decrease the event_limit by 1. '''

    Member = models.ForeignKey(Member, on_delete=models.CASCADE, verbose_name='Member', null=False)
    Event = models.ForeignKey(Event, on_delete=models.CASCADE, verbose_name='Event', null=False)








