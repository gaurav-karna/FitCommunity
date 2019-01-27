from django.urls import path, include
from . import views
import django.contrib.auth
# from django.conf import settings

urlpatterns = [

    # public links
    path('', views.index, name='index'), # home page
    path('portal/', include('django.contrib.auth.urls')), # login link

    path('new_member_signup/', views.new_member_signup, name='new_member_signup'), # sign-up link as member
    path('new_community_signup/', views.new_community_signup, name='new_community_signup'), # sign-up link as comm admin

    path('portal/login/admin', views.welcome_admin, name='welcome_admin'), # root page for admin upon login
    path('portal/login/member', views.welcome_member, name='welcome_member'), # root page for member upon login
    # Same view page for these welcome sights, will have button for all their registered events
    # root page itself will have tiles for all events, or filtered by category

    path('portal/login/diverge', views.diverge, name='diverge'), # diverger function
    path('logout_screen', views.logout_screen, name='logout_screen'), # Logout screen

    # path('portal/login/admin/all_members', views.all_members, name='all_members'), # see all members
    path('portal/login/admin/all_events', views.all_events, name='all_events'),
    path('portal/login/admin/confirm_event/<int:event_id>/<int:member_id>', views.confirm_event, name='confirm_event'),


    # path('portal/login/admin/create_event', views.admin_create_event, name='admin_create_event'), # admin create event
    # path('portal/login/member/create_event', views.member_create_event, name='member_create_event'), # member create event
    # emails sent to all people in community

    path('portal/login/member/my_events', views.my_events, name='my_events'),

    path('portal/login/admin/view_event/<int:event_id>', views.admin_view_event, name='admin_view_event'),
    # Admin will have universal delete / edit privileges

    # path('portal/login/member/view_event/<int:event_id>', views.member_view_event, name='member_view_event'),
    # Person will only have delete / edit privileges if the event is theirs

    path('portal/login/edit_event/int:<event_id>', views.edit_event, name='edit_event'),
    # form view to change details about the event

    # Both event views would need a comment thread, confirm registration button, how many seats left, location, etc.

    path('portal/login/admin/confirm_delete_event/<int:event_id>', views.admin_delete_confirm, name='admin_delete_confirm'),
    path('portal/login/admin/delete/<int:event_id>', views.admin_delete, name='admin_delete'),

    # path('portal/login/member/confirm_delete_event/<int:event_id>', views.member_delete_confirm, name='member_delete_confirm'),
    # path('portal/login/member/delete/<int:event_id>', views.member_delete, name='member_delete'),
    # delete confirmation, and true delete + redirect views
    #
    # path('portal/login/admin/view_member/<int:member_id>', views.admin_view_member, name='admin_view_member'), # admin views members
    # admin here also has privileges to unapprove (will get sent email)
    # admin can also see the progress of an individual via the fitbit graphs
    #
    # will use request.user.id to render correct profile and form
    path('portal/login/member/profile/', views.view_profile, name='view_profile'), # profile view + edit view
    # # this profile view would need to have fitbit records arranged in the same way that the event tiles were arranged

    # path('portal/login/member/add_personal_record', views.add_record, name='add_record'),
    # this edit view would need an option to add another CSV (can go in their media file)

    # error views
    path('403', views.shoot_403, name='403'),
    path('400', views.shoot_400, name='400'),
    path('404', views.shoot_404, name='404'),
    path('500', views.shoot_500, name='500'),




]

