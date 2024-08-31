from django.contrib import admin
from .models import Student

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['Student_Name', 'student_id', 'year_study']
    
    def Student_Name(self, obj):
        return f"{obj.profile.user.first_name} {obj.profile.user.last_name}"
    Student_Name.short_description = 'Student Name'
    
    def student_id(self, obj):
        return obj.student_id
    student_id.short_description = 'Student Id'
    
    def year_study(self, obj):
        suffix = ""
        if obj.year_of_study == 1:
            suffix = "st year"
        elif obj.year_of_study == 2:
            suffix = "nd year"
        elif obj.year_of_study == 3:
            suffix = "rd year"
        else:
            suffix = "th year"
        return f"{obj.year_of_study}{suffix}"

    year_study.short_description = 'Year of Study'
