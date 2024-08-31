from rest_framework  import serializers
from django.contrib.auth.models import User
from accounts.models import UserProfile
from course.models import Department
from accounts.constants import TEACHER
from .models import *


class DesignationSerializer(serializers.ModelSerializer):
    class Meta:
        model   = Designation
        fields  = ['id', 'name']

class SpecializationSerializer(serializers.ModelSerializer):
    class Meta:
        model   = Specialization
        fields  = ['id', 'name']

class TeacherSerializer(serializers.ModelSerializer):
    confirm_password    = serializers.CharField(write_only=True, required=True, max_length=30, style={'input_type': 'password'})
    date_of_birth       = serializers.DateField(required=True, source='profile.date_of_birth')
    profile_picture     = serializers.ImageField(required=False, source='profile.profile_picture')
    department          = serializers.SlugRelatedField(queryset=Department.objects.all(), slug_field='name', required=True, source='profile.department')
    phone_number        = serializers.CharField(max_length=12, source='profile.phone_number')
    designation         = serializers.SlugRelatedField(queryset=Designation.objects.all(), slug_field='name', required=True, source='profile.teacher.designation')
    specializations     = serializers.SlugRelatedField(queryset=Specialization.objects.all(), slug_field='name', many=True, source='profile.teacher.specializations')
    bio                 = serializers.CharField(required=False, source='profile.teacher.bio')

    class Meta:
        model   = User
        fields  = [
            'id', 'username', 'first_name', 'last_name', 'email', 'password', 'confirm_password', 'date_of_birth', 'department', 'phone_number', 'profile_picture', 'designation', 'specializations', 'bio'
        ]

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError("Passwords do not match.")
        if 'email' in data and User.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError("Email already exists.")
        return data

    def create(self, validated_data):
        profile_data = validated_data.pop('profile')
        teacher_data = profile_data.pop('teacher')
        validated_data.pop('confirm_password')

        user = User(
            username    = validated_data['username'],
            first_name  = validated_data['first_name'],
            last_name   = validated_data['last_name'],
            email       = validated_data['email']
        )
        user.set_password(validated_data['password'])
        user.is_active = False
        user.save()

        profile = UserProfile(
            user            = user,
            date_of_birth   = profile_data['date_of_birth'],
            department      = profile_data['department'],
            profile_picture = profile_data.get('profile_picture', None),
            phone_number    = profile_data['phone_number'],
            role            = TEACHER,
        )
        profile.save()

        teacher = Teacher(
            profile     = profile,
            bio         = teacher_data.get('bio', ''),
            designation = teacher_data.get('designation', None),
        )
        teacher.save()
        teacher.specializations.set(teacher_data['specializations'])

        return user
    
    def update(self, instance, validated_data):
        profile_data = validated_data.pop('profile')
        teacher_data = profile_data.pop('teacher')

        instance.username   = validated_data.get('username', instance.username)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name  = validated_data.get('last_name', instance.last_name)
        instance.email      = validated_data.get('email', instance.email)
        instance.save()

        profile                 = instance.profile
        profile.date_of_birth   = profile_data.get('date_of_birth', profile.date_of_birth)
        profile.department      = profile_data.get('department', profile.department)
        profile.profile_picture = profile_data.get('profile_picture', profile.profile_picture)
        profile.phone_number    = profile_data.get('phone_number', profile.phone_number)
        profile.save()

        teacher                 = profile.teacher
        teacher.designation     = teacher_data.get('designation', teacher.designation)
        teacher.bio             = teacher_data.get('bio', teacher.bio)
        if 'specializations' in teacher_data:
            teacher.specializations.set(teacher_data['specializations'])
        teacher.save()

        return instance

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if 'password' in data:
            data.pop('password', None)
        return data




