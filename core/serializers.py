from rest_framework import serializers
from .models import Client, Project
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']

class ClientSerializer(serializers.ModelSerializer):
    created_by = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Client
        fields = ['id', 'client_name', 'created_by', 'created_at', 'updated_at']

class ProjectSerializer(serializers.ModelSerializer):
    client = serializers.IntegerField(write_only=True)  # client_id is write-only
    users = UserSerializer(many=True, read_only=True)
    user_ids = serializers.ListField(write_only=True, child=serializers.IntegerField())

    class Meta:
        model = Project
        fields = ['id', 'project_name', 'client', 'client_id', 'users', 'user_ids', 'created_by', 'created_at']

    def create(self, validated_data):
        user_ids = validated_data.pop('user_ids', [])
        client = validated_data.pop('client', None)  # Get the client_id from the request data

        # Ensure the client_id is provided and associate the client object with the project
        if client:
            validated_data['client'] = Client.objects.get(id=client)

        # Create the project instance
        project = super().create(validated_data)

        # Fetch the User instances and associate them with the project
        users = User.objects.filter(id__in=user_ids)
        project.users.set(users)  # Set the related users for the project

        return project
