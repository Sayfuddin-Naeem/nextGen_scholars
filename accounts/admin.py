from django.contrib import admin
from .models import UserProfile

admin.site.site_header = "NextGen Scholars Administration"
admin.site.site_title = "NextGen Scholars Admin Portal"
admin.site.index_title = "Welcome to NextGen Scholars Admin"

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'date_of_birth', 'profile_picture', 'department', 'phone_no', 'role', 'created_on']
    
    def user(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name}"
    user.short_description = 'Full Name'
    
    def profile_picture(self, obj):
        return obj.profile_picture
    profile_picture.short_description = 'Profile Photo'
    
    def department(self, obj):
        return obj.department.name
    department.short_description = 'Department Name'
    
    def phone_no(self, obj):
        return obj.phone_number
    phone_no.short_description = 'Phone No'
    
    def created_on(self, obj):
        return obj.created_on
    created_on.short_description = 'Created On'
    
    def role(self, obj):
        return obj.get_role_display()