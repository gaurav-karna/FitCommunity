from _datetime import datetime
from django.db import models
# from django.core.validators import EmailValidator, MinValueValidator, MaxValueValidator
# from django.contrib.auth import get_user_model
from django.db import transaction
from django.conf import settings

from django.contrib.auth.models import AbstractUser, BaseUserManager

from django.contrib.auth.models import User

# from django.utils import timezone

# Create your models here.

# Event Class - what users will create to invite people to

class User(AbstractUser):
    pass

# This is what will be in each Event
# Comment box will be rendered at the bottom of each event page
class Comment (models.Model):
    Forum_Post = models.CharField(max_length=1024)
    # created_at will be initialized when the comment is saved
    Created_At = models.DateTimeField(auto_now=False, auto_now_add=True, editable=False)

categories = (
    ('Sports', 'Sports'),
    ('Yoga / Meditation', 'Yoga / Meditation'),
    ('Cardio', 'Cardio'),
    ('Weight-Lifting', 'Weight-Lifting'),
    ('Aerobics', 'Aerobics')
)

class Event(models.Model):
    class Meta:
        verbose_name_plural = 'Events'

    Start_Date = models.DateTimeField()
    End_Date = models.DateTimeField()

    Registration_Deadline = models.DateTimeField(verbose_name='Deadline for Regsitration', null=False)
    Registration_Open = models.BooleanField(verbose_name='Open for Registration?', null=False)

    Category = models.CharField(choices=categories, max_length=24)


### AUXILIARY METHODS ###
def check_registration(start_date, end_date, deadline):
    current = datetime.now()
    if (current > end_date) or (current > start_date) or (current > deadline):
        return False
    else:
        return True





