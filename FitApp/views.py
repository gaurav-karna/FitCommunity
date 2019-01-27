from django.shortcuts import render

from django.http import HttpResponse

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

    context = {
        'user_form':UserForm(),
        'm_form':MemberSignupForm(),
    }
    return render(request, 'new_member_signup.html', context)