from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from archive.users.models import UserProfile
  
admin.site.unregister(User)
  
class UserProfileInline(admin.StackedInline):
    model = UserProfile
    max_num = 2

class UserProfileAdmin(UserAdmin):
    inlines = [UserProfileInline]
  
admin.site.register(User, UserProfileAdmin)
