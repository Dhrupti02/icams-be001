from rest_framework import serializers
from django.contrib.auth.models import User
from . import models

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(required=True)

    class Meta:
        model = models.UserProfile
        fields = '__all__'

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = UserSerializer.create(UserSerializer(), validated_data=user_data)
        user.set_password(user_data['password'])
        user.save()
        user_profile = models.UserProfile.objects.create(user=user, **validated_data)
        return user_profile

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Course
        fields = ['id', 'course_name', 'time_duration', 'description', 'created_date', 'last_update_date', 'instructor']

class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Document
        fields = '__all__'  # You can specify the fields you want to include here

class DocumentFilesSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.DocumentFiles
        fields = '__all__'  # You can specify the fields you want to include here

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Task
        fields = '__all__'