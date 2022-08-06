from django.shortcuts import render
from django.db.models import Q

from rest_framework import viewsets, mixins

from chat.serializers import ChatSerializer
from .models import Chat

# Create your views here.

class ChatViewset(mixins.CreateModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = ChatSerializer
    
    def get_queryset(self):
        user = self.request.user
        return Chat.objects.filter(Q(sender=user)|Q(receiver=user)).order_by('-id')

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({'user': self.request.user})
        return context