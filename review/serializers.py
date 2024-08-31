from rest_framework  import serializers
from .models import Review
from course.models import Course


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'
    
    def create(self, validated_data):
        # Accessing the context data
        student = self.context['request'].user.profile.student
        course_id = self.context['course_id']

        # Ensure the course exists and get the course instance
        try:
            course = Course.objects.get(id=course_id)
        except Course.DoesNotExist:
            raise serializers.ValidationError("The course does not exist.")

        # Creating a new Review instance
        review = Review.objects.create(
            student=student,
            course=course,
            body=validated_data['body'],
            rating=validated_data['rating']
        )
        return review

    