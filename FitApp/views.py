from django.shortcuts import render, redirect

from django.http import HttpResponse, Http404

from .forms import *

from .models import Registrations, CommunityAdmin

# Email
from django.core.mail import send_mail, send_mass_mail
from django.template.loader import render_to_string
from django.conf import settings

# Create your views here.

def index(request):
    return render(request, 'home.html', {})

def new_member_signup(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        m_form = MemberSignupForm(request.POST)
        if user_form.is_valid() and m_form.is_valid():
            new_user = user_form.save()
            new_member = m_form.save()
            if new_member.Community.Required_Email:
                if not new_user.email.endswith(new_member.Community.Required_Email):
                    new_user.delete()
                    new_member.delete()
                    return render(request, 'new_member_signup.html', {'custom_message':'You do not have the correct email address to join'
                                                                                       'the community you selected'})
            new_member.user = new_user
            if new_user.member_profile == new_member:
                new_member.BMI = calc_bmi(new_member.Weight, new_member.Height)
                new_member.save()
                shoot_email(render_to_string('emails/welcome_member.html', {'user': new_user}),
                            render_to_string('emails/welcome_member.txt', {'user': new_user}),
                            'Welcome to DeltaFit!', [new_user.email])
            else:
                raise Http404
            return render(request, 'signup_success.html', {'user':new_user})
        raise Http404
    else:
        context = {
            'user_form':UserForm(),
            'm_form':MemberSignupForm(),
        }
        return render(request, 'new_member_signup.html', context)

def new_community_signup(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        comm_form = CommunityForm(request.POST)
        if user_form.is_valid() and comm_form.is_valid():
            new_user = user_form.save()
            new_community = comm_form.save()
            new_community_admin = CommunityAdmin().objects.create(user=new_user, Community=new_community, is_approved=False)
            new_community_admin.save()
            return render(request, 'signup_success.html', {'user':new_user})
        raise Http404
    else:
        context = {
            'user_form':UserForm(),
            'comm_form':CommunityForm(),
        }
        return render(request, 'new_community_signup.html', context)

# Function that redirects based on status
def diverge(request):
    if check_admin(request.user):
        return redirect('/portal/login/admin', {'user':request.user})
    elif not check_admin(request.user):
        return redirect('/portal/login/member', {'user':request.user})
    else:
        return render(request, '400.html', {'custom_message': "CODE 2 - Diverger Failure"})

def logout_screen(request):
    return render(request, 'logout_screen.html', {})


# Root page for admin
def welcome_admin(request):
    if not check_admin(request.user):
        return shoot_403(request)
    else:
        return render(request, 'welcome_admin.html', {'user':request.user})

def all_events (request, filter_id):
    if filter_id == 6:
        queryset = Event.objects.all()
    elif filter_id == 5:
        queryset = Event.objects.filter(Category='Yoga / Meditation')
    elif filter_id == 4:
        queryset = Event.objects.filter(Category='Weight-Lifting')
    elif filter_id == 3:
        queryset = Event.objects.filter(Category='Sports')
    elif filter_id == 2:
        queryset = Event.objects.filter(Category='Cardio')
    else:
        queryset = Event.objects.filter(Category='Aerobics')
    return render(request, 'all_events.html', {'set':queryset})

def admin_view_event (request, event_id):
    if request.method == 'POST':
        new_comment = CommentsForm(request.POST)
        if new_comment.is_valid():
            new_comment.save()
        event = Event.objects.get(id=event_id)
        context = {
            'event': event,
            'comments': event.comments_set,
            'comments_form': CommentsForm(),
            'custom_message': 'Your comment was saved successfully.'

        }
        return render (request, 'admin_event_view.html', context)
    event = Event.objects.get(id=event_id)
    context = {
        'event':event,
        'comments':event.comments_set,
        'comments_form':CommentsForm()
    }
    return (request, 'admin_event_view.html', context)

# universal method for admins and members
def confirm_event (request, event_id, member_id):
    # new_registration = Registrations.objects.create(Member=Member.objects.get(id=member_id), Event=Event.objects.get(id=event_id))
    pass

def admin_delete_confirm(request, event_id):
    return render(request, 'confirm_event_delete.html', {'event':Event.objects.get(id=event_id)})

def admin_delete (request, event_id):
    event = Event.objects.get(id=event_id)
    event.delete()
    return render(request, 'all_events.html', {'custom_message':'Event has been successfully deleted'})

def edit_event(request, event_id):
    event = Event.objects.get(id=event_id),
    context = {
        'event': event,
        'event_form':EventForm(instance=event)
    }
    return render(request, 'edit_event.html', context)

# Authority Checker - returns true if user is an admin (does not have a member profile)
def check_admin(user):
    if user.admin_profile:
        return True
    return False

def check_signed_user(user, url_id):
    if (user.id != url_id):
        return redirect('/403')

# Email functions
def shoot_email(html_message, text_message, subject, recipient_list):
    send_mail(subject, text_message, from_email=settings.EMAIL_HOST_USER
              , recipient_list=recipient_list, html_message=html_message)

# BMI Algorithm
def calc_bmi(weight, height):
    return (int)(weight/(height*height))

# Custom Error Views
def shoot_404(request):
    return render(request, '404.html', status=404)

def shoot_500 (request):
    return render(request, '500.html', status=500)

def shoot_403 (request):
    return render(request, '403.html', status=403)

def shoot_400 (request):
    return render(request, '400.html', status=400)