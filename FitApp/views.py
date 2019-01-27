from django.shortcuts import render

from django.http import HttpResponse, Http404

from .forms import *

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
            new_member.user = new_user
            if new_user.member_profile == new_member:
                new_member.BMI = calc_bmi(new_member.Weight, new_member.Height)
                new_member.save()
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



# BMI Algorithm
def calc_bmi(weight, height):
    return (int)(weight/(height*height))