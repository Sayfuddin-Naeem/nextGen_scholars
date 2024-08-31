from django.db import models

class Specialization(models.Model):
    name = models.CharField(max_length=30, unique=True)
    slug = models.SlugField(max_length=40)
    
    def __str__(self) -> str:
        return self.name
    
class Designation(models.Model):
    name = models.CharField(max_length=30, unique=True)
    slug = models.SlugField(max_length=40)
    
    def __str__(self) -> str:
        return self.name

class Teacher(models.Model):
    profile = models.OneToOneField('accounts.UserProfile', related_name="teacher", on_delete=models.CASCADE)
    designation = models.ForeignKey(Designation, on_delete=models.SET_NULL, null=True, blank=True)
    bio = models.TextField(blank=True)
    specializations = models.ManyToManyField(Specialization)

    def __str__(self):
        return f"{self.profile.user.username} - {self.designation}"