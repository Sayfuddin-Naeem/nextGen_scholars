from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Student
from accounts.models import UserProfile
from course.models import Department
from accounts.constants import STUDENT
from django.db import transaction


class StudentSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True, required=True, max_length=30, style={'input_type': 'password'})
    date_of_birth    = serializers.DateField(required=True, source='profile.date_of_birth')
    profile_picture  = serializers.ImageField(required=False, source='profile.profile_picture')
    department       = serializers.SlugRelatedField(queryset=Department.objects.all(), slug_field='name', required=True, source='profile.department')
    phone_number     = serializers.CharField(max_length=12, source='profile.phone_number')
    year_of_study    = serializers.IntegerField(required=True, source='profile.student.year_of_study')

    class Meta:
        model   = User
        fields  = [
            'id', 'username', 'first_name', 'last_name', 'email', 'password', 'confirm_password', 'date_of_birth', 'department', 'phone_number', 'profile_picture', 'year_of_study'
        ]

    def validate(self, data):
        # Custom validation logic
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError("Passwords do not match.")
        if 'email' in data and User.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError("Email already exists.")
        return data

    @transaction.atomic
    def create(self, validated_data):
        # Using transaction.atomic to ensure atomicity
        try:
            # Extract profile and student data from validated_data
            profile_data = validated_data.pop('profile')
            student_data = profile_data.pop('student')
            
            # Remove confirm_password from the data since it's not a model field
            validated_data.pop('confirm_password')

            # User creation
            user = User(
                username    = validated_data['username'],
                first_name  = validated_data['first_name'],
                last_name   = validated_data['last_name'],
                email       = validated_data['email']
            )
            user.set_password(validated_data['password'])
            user.is_active = False  # Set to False until email verification
            user.save()

            # UserProfile creation
            profile = UserProfile(
                user            = user,
                date_of_birth   = profile_data['date_of_birth'],
                department      = profile_data['department'],
                profile_picture = profile_data.get('profile_picture', None),
                phone_number    = profile_data['phone_number'],
                role            = STUDENT,
            )
            profile.save()

            # Student creation
            student = Student(
                profile      = profile,
                student_id   = 10000 + user.id,
                year_of_study= student_data['year_of_study']
            )
            student.save()

            return user

        except Exception as e:
            # If any error occurs during the transaction, it will roll back
            raise serializers.ValidationError(f"Error occurred during user creation: {str(e)}")
    
    def update(self, instance, validated_data):
        # Extract profile and student data from validated_data
        profile_data = validated_data.pop('profile')
        student_data = profile_data.pop('student')

        # Update User fields
        instance.username   = validated_data.get('username', instance.username)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name  = validated_data.get('last_name', instance.last_name)
        instance.email      = validated_data.get('email', instance.email)
        instance.save()

        # Update UserProfile fields
        profile                 = instance.profile  # Access the UserProfile related to the User
        profile.date_of_birth   = profile_data.get('date_of_birth', profile.date_of_birth)
        profile.department      = profile_data.get('department', profile.department)
        profile.profile_picture = profile_data.get('profile_picture', profile.profile_picture)
        profile.phone_number    = profile_data.get('phone_number', profile.phone_number)
        profile.save()

        # Update Student fields
        student               = profile.student  # Access the Student related to the UserProfile
        student.year_of_study = student_data.get('year_of_study', student.year_of_study)
        student.save()

        return instance
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        # Conditionally exclude 'password' from the response
        if 'password' in data:
            data.pop('password', None)

        return data
