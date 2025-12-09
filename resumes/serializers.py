from rest_framework import serializers
from .models import Resume

class ResumeUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resume
        fields = ['id', 'file', 'text', 'skills', 'created_at']
        read_only_fields = ['text', 'skills', 'created_at']

class ResumeSerializer(serializers.ModelSerializer):
    owner_username = serializers.CharField(source='owner.username', read_only=True)
    
    class Meta:
        model = Resume
        fields = ['id', 'owner', 'owner_username', 'file', 'text', 'skills', 'embeddings', 'created_at']
        read_only_fields = ['owner', 'text', 'skills', 'embeddings', 'created_at']