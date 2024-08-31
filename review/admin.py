from django.contrib import admin
from .models import Review

# Register your models here.
@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['reviewer', 'course', 'body', 'on_created', 'rating']
    
    def reviewer(self, obj):
        return obj.reviewer.profile.user.username
    reviewer.short_description = 'Review By'
    
    def course(self, obj):
        return obj.course.title
    course.short_description = 'Course Name'
    
    def body(self, obj):
        return obj.body
    body.short_description = 'Review'
    
    def on_created(self, obj):
        return obj.on_created
    on_created.short_description = 'Review Time'

    def rating(self, obj):
        return obj.rating
    rating.short_description = 'Course Rating'