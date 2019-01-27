# Generated by Django 2.1.4 on 2019-01-27 01:23

import FitApp.models
from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import places.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0009_alter_user_last_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comments',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Forum_Post', models.CharField(max_length=1024)),
                ('Created_At', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Community',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Location', places.fields.PlacesField(max_length=255)),
                ('Required_Email', models.CharField(blank=True, max_length=64, null=True, unique=True, verbose_name='Is there a specific email address you wouldlike your members to have?')),
            ],
        ),
        migrations.CreateModel(
            name='CommunityAdmin',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Community', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='FitApp.Community')),
            ],
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Title', models.CharField(max_length=32)),
                ('Short_Description', models.TextField(max_length=500, verbose_name='Add a short (< 500 characters) description of your event')),
                ('Location', places.fields.PlacesField(max_length=255, verbose_name='Enter a location for your event.')),
                ('Event_Picture', models.ImageField(upload_to=FitApp.models.user_directory_path)),
                ('Start_Date', models.DateTimeField()),
                ('End_Date', models.DateTimeField()),
                ('Registration_Deadline', models.DateTimeField(verbose_name='Deadline for Regsitration')),
                ('Max_Registration', models.SmallIntegerField(default=4, validators=[django.core.validators.MinValueValidator(4, message='Minimum number of people per event is 4.'), django.core.validators.MaxValueValidator(50, message='Maximum number of people per event is 50.')])),
                ('Registration_Open', models.BooleanField(verbose_name='Open for Registration?')),
                ('Category', models.CharField(choices=[('Sports', 'Sports'), ('Yoga / Meditation', 'Yoga / Meditation'), ('Cardio', 'Cardio'), ('Weight-Lifting', 'Weight-Lifting'), ('Aerobics', 'Aerobics')], max_length=24)),
                ('Event_Details', models.TextField(blank=True, max_length=2000, verbose_name='(Optional) Please keep this to under 2000 characters.')),
            ],
            options={
                'verbose_name_plural': 'Events',
            },
        ),
        migrations.CreateModel(
            name='Member',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Bio', models.TextField(default='Hey, I am a member of FitCommunity', max_length=250, verbose_name='Biography: Please keep it under 250 characters')),
                ('Age', models.SmallIntegerField(default=12, validators=[django.core.validators.MinValueValidator(12, message='You have to be at least 12 years old to use FitCommunity.'), django.core.validators.MaxValueValidator(120, message='You cannot use FitCommunity if you are over 120 years old.')])),
                ('Gender', models.CharField(choices=[('Male', 'Male'), ('Female', 'Female'), ('Rather Not Say', 'Rather Not Say')], max_length=16)),
                ('Weight', models.SmallIntegerField(default=70, validators=[django.core.validators.MinValueValidator(12, message='Minimum weight must be 12 kg.'), django.core.validators.MaxValueValidator(400, message='Maximum weight is 400 kg.')], verbose_name='Please enter your weight in kilograms')),
                ('Height', models.SmallIntegerField(default=175, validators=[django.core.validators.MinValueValidator(100, message='Minimum height must be 100 cm'), django.core.validators.MaxValueValidator(300, message='Maximum height is 300 cm')], verbose_name='Please enter your height in centimeters')),
                ('BMI', models.SmallIntegerField(verbose_name='Body Mass Index')),
                ('Ethnicity', models.CharField(choices=[('Caucasian', 'Caucasian'), ('African-American', 'African-American'), ('Asian', 'Asian'), ('South Asian', 'South Asian'), ('Latin-American', 'Latin-American'), ('European', 'European'), ('Middle-Eastern', 'Middle-Eastern')], max_length=32)),
                ('Known_Conditions', models.TextField(default='Not Applicable', max_length=300, verbose_name='Are there any conditions you would like us to know? Please keep it under 300 characters')),
                ('is_approved', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Registrations',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='FitApp.Event', verbose_name='Event')),
                ('Member', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='FitApp.Member', verbose_name='Member')),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.AddField(
            model_name='member',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='member_profile', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='communityadmin',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='admin_profile', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='comments',
            name='Related_Event',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='FitApp.Event', verbose_name='Something to say?'),
        ),
    ]
