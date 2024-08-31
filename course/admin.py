from django.contrib import admin
from .models import *

# Register your models here.

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',),}
    list_display = ['name', 'slug']

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['title', 'description', 'department', 'instructor', 'course_image', 'created_at', 'is_active']
    
    def title(self, obj):
        return obj.title
    title.short_description = 'Course Name'
    
    def course_image(self, obj):
        return obj.course_image
    course_image.short_description = 'Course Photo'
    
    def created_at(self, obj):
        return obj.created_at
    created_at.short_description = 'Added Date'
    
    def is_active(self, obj):
        return "Running" if obj.is_active else "Closed"
    is_active.short_description = 'Active Status'

@admin.register(CourseEnrollment)
class CourseEnrollmentAdmin(admin.ModelAdmin):
    list_display = ['student', 'course', 'enrollment_date', 'progress', 'is_completed', 'grade']
    
    def student(self, obj):
        return obj.student.profile.user.username
    student.short_description = 'Course Name'
    
    def course(self, obj):
        return obj.course.title
    course.short_description = 'Course Name'
    
    def enrollment_date(self, obj):
        return obj.enrollment_date
    enrollment_date.short_description = 'Enrollment Date'
    
    def progress(self, obj):
        return f"{obj.progress} %"
    progress.short_description = 'Progress'
    
    def is_completed(self, obj):
        return "Completed" if obj.is_completed else "Running"
    is_completed.short_description = 'Complete Status'
    
    def grade(self, obj):
        return obj.grade
    grade.short_description = 'Grade'