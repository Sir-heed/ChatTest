from rest_framework import serializers

from .models import Chat
from user.models import User
from user.serializers import UserSerializer

class CustomUserSerializer(serializers.RelatedField):
    def to_representation(self, value):
        return UserSerializer(value).data
    
    def to_internal_value(self, data):
        try:
            receiver = User.objects.get(id=data)
        except User.DoesNotExist:
            raise serializers.ValidationError({
                'receiver': 'User does not exist'
            })
        return receiver

class ChatSerializer(serializers.ModelSerializer):
    receiver = CustomUserSerializer(queryset=User.objects.all(), required=True)

    class Meta:
        model = Chat
        fields = '__all__'
        read_only_fields = ['created_at']

    def create(self, validated_data):
        return Chat.objects.create(**validated_data, sender=self.context['user'])