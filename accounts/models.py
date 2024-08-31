from django.contrib.auth.models import User
from course.models import Department
from .constants import USER_ROLES
from django.db import models
from .utils import get_upload_to

class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name="profile", on_delete=models.CASCADE)
    date_of_birth = models.DateField()
    profile_picture = models.ImageField(upload_to=get_upload_to, blank=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=12)
    role = models.CharField(max_length=10, choices=USER_ROLES)
    created_on = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.get_role_display()}"
