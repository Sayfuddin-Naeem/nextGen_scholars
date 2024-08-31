from django.contrib import admin
from .models import *

# Register your models here.
@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ['profile', 'designation', 'bio', 'specializations']
    
    def profile(self, obj):
        return f"{obj.profile.user.first_name} {obj.profile.user.last_name}"
    profile.short_description = 'Teacher Name'
    
    def designation(self, obj):
        return obj.designation
    designation.short_description = 'Designation'
    
    def specializations(self, obj):
        return obj.specializations
    specializations.short_description = 'Specializations'

@admin.register(Designation)
class DesignationAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',),}
    list_display = ['name', 'slug']

@admin.register(Specialization)
class SpecializationAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',),}
    list_display = ['name', 'slug']
    