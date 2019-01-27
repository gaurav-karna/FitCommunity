from django.contrib import admin

# Register your models here.

from .models import *
from django.contrib.auth.admin import UserAdmin as OGAdmin

admin.site.register(Member)
admin.site.register(Event)
admin.site.register(CommunityAdmin)
admin.site.register(Community)
admin.site.register(Registrations)
admin.site.register(Comments)

admin.site.register(User, OGAdmin)
