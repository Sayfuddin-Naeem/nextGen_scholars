from django.db import models
from teacher.models import Teacher
from student.models import Student
from .utils import get_upload_to

# Create your models here.

class Department(models.Model):
    name = models.CharField(max_length=30, unique=True)
    slug = models.SlugField(max_length=40)
    
    def __str__(self) -> str:
        return self.name

class Course(models.Model):
    title       = models.CharField(max_length=150)
    description = models.TextField()
    department  = models.ForeignKey(Department, on_delete=models.CASCADE)
    instructor  = models.ForeignKey(Teacher, related_name='courses', on_delete=models.CASCADE)
    course_image= models.ImageField(upload_to=get_upload_to, blank=True)
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)
    is_active   = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.title} by {self.instructor.profile.user.username}"

    class Meta:
        ordering = ['-created_at']

class CourseEnrollment(models.Model):
    student         = models.ForeignKey(Student, related_name='enrolled_course', on_delete=models.CASCADE)
    course          = models.ForeignKey(Course, related_name='enrolled_student', on_delete=models.CASCADE)
    enrollment_date = models.DateTimeField(auto_now_add=True)
    progress        = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)  # Percentage progress (e.g., 75.50)
    is_completed    = models.BooleanField(default=False)
    grade           = models.CharField(max_length=5, blank=True)  # Optional, store grades like A+, B, etc.
    
    def __str__(self):
        return f"{self.student.profile.user.username} enrolled in {self.course.title}"

    class Meta:
        unique_together = ('student', 'course')
        ordering        = ['-enrollment_date']

