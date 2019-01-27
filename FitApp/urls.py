from django.urls import path, include
from . import views
import django.contrib.auth
# from django.conf import settings

urlpatterns = [

    # public links
    path('', views.index, name='index'), # home page
    path('portal/', include('django.contrib.auth.urls')), # login link
    path('new_member_signup', views.new_member_signup, name='new_member_signup'), # sign-up link as member
    path('new_community_signup', views.new_community_signup, name='new_community_signup'), # sign-up link as comm admin
    # path('new_member_success', views.new_member_)


]

