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

### Method to return path for image upload per user

def user_directory_path(instance, filename):
    return 'user_{0}/{1}'.format(instance.user.id, filename)

class Event(models.Model):
    class Meta:
        verbose_name_plural = 'Events'

    Title = models.CharField(max_length=32)

    Short_Description = models.TextField(max_length=500, verbose_name='Add a short (< 500 characters) description of your event')

    Location = PlacesField(verbose_name='Enter a location for your event.')

    Event_Picture = models.ImageField(upload_to=user_directory_path)

    Start_Date = models.DateTimeField()

    End_Date = models.DateTimeField()

    Registration_Deadline = models.DateTimeField(verbose_name='Deadline for Regsitration', null=False)

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

# Comment box will be rendered at the bottom of each event page
class Comments (models.Model):
    Forum_Post = models.CharField(max_length=1024)
    # created_at will be initialized when the comment is saved
    Created_At = models.DateTimeField(auto_now=False, auto_now_add=True, editable=False)

    # Foreign key to an Event (one event can have multiple comments, but one comment can only have one event)
    # This is on_delete, as there is no point maintaining comments if the event is deleted.
    Related_Event = models.ForeignKey(Event, on_delete=models.CASCADE, null=False, verbose_name='Something to say?')

### AUXILIARY METHODS ###
def check_registration(event):
    current = datetime.now()
    if (current > event.End_Date) or (current > event.Start_Date) or (current > event.Registration_Deadline):
        return False
    else:
        return True







