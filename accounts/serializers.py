from rest_framework import serializers
from django.contrib.auth.models import User
from .models import ContactUs


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)

    def validate(self, data):
        # Custom Validation
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            raise serializers.ValidationError("Both username and password are required.")

        return data

class PasswordUpdateSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    new_password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    confirm_password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})

    def validate(self, data):
        old_password = data.get('old_password')
        new_password = data.get('new_password')
        confirm_password = data.get('confirm_password')
        
        # Get the user instance from the context
        user = self.context['request'].user
        
        # Check if the old password is correct
        if not user.check_password(old_password):
            raise serializers.ValidationError("Old password is incorrect.")
        
        # Check if new password and confirm password match
        if new_password != confirm_password:
            raise serializers.ValidationError("New passwords do not match.")
        
        return data

    def update(self, instance, validated_data):
        # Set the new password
        new_password = validated_data['new_password']
        instance.set_password(new_password)
        instance.save()
        return instance

class ContactUsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactUs
        fields = '__all__'
