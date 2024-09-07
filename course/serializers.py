from rest_framework  import serializers
from .models import *

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['id', 'title', 'description', 'department', 'course_image']

    def create(self, validated_data):
        # Access the request object through context
        instructor = self.context['request'].user.profile.teacher
        
        course = Course(
            title = validated_data['title'],
            description = validated_data['description'],
            department = validated_data['department'],
            instructor = instructor,
            course_image = validated_data.get('course_image', None),
        )
        course.save()
        return course

    def update(self, instance, validated_data):
        # Update instance with validated data
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.department = validated_data.get('department', instance.department)
        instance.course_image = validated_data.get('course_image', instance.course_image)
        
        instance.save()
        return instance
        
class CourseEnrollmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseEnrollment
        fields = '__all__'

    def create(self, validated_data):
        # Accessing the context data
        student = self.context['request'].user.profile.student
        course_id = self.context['course_id']
        if course_id:
            course = course = Course.objects.get(id=course_id)
        
        # Creating a new CourseEnrollment instance
        enrollment = CourseEnrollment.objects.create(
            student = student,
            course  = validated_data['course'],
        )
        return enrollment