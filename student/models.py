from django.db import models

class Student(models.Model):
    profile = models.OneToOneField('accounts.UserProfile', related_name="student", on_delete=models.CASCADE)
    student_id = models.PositiveIntegerField(unique=True)  # Unique student id
    year_of_study = models.IntegerField()  # Current year of study (e.g., 1, 2, 3, 4)
    
    def __str__(self):
        return f"{self.profile.user.username} - {self.student_id}"
    