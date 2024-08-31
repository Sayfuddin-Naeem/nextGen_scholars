from django.db import models
from .constants import STAR_CHOICES
from student.models import Student
from course.models import Course

# Create your models here.
class Review(models.Model):
    student = models.ForeignKey(Student, related_name="review", on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='course_review')
    body = models.TextField()
    on_created = models.DateTimeField(auto_now_add=True)
    rating = models.PositiveIntegerField(choices=STAR_CHOICES)
    
    def __str__(self):
        return f"Student: {self.reviewer.profile.user.first_name}; Course: {self.course.title}"