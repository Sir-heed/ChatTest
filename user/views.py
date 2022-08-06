from django.shortcuts import render
from rest_framework.permissions import AllowAny
from rest_framework import mixins, viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from user.models import User

# Create your views here.
from .serializers import LoginSerializer, UserSerializer

class UserViewset(mixins.CreateModelMixin, viewsets.GenericViewSet):
    permission_classes = [AllowAny]
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        return Response({
            'status': True,
            'token': str(refresh.access_token),
            'refresh': str(refresh),
            'user': UserSerializer(user).data
        }, status=status.HTTP_201_CREATED)


class LoginView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            try:
                user = User.objects.get(email=email)
                if user.is_active:
                    if user.check_password(password):
                        refresh = RefreshToken.for_user(user)
                        return Response({
                            'status': True,
                            'token': str(refresh.access_token),
                            'refresh': str(refresh),
                            'user': UserSerializer(user).data
                        }, status=status.HTTP_200_OK)
                    else:
                        return Response({
                            'status': False,
                            'message': 'Incorrect password'
                        }, status=status.HTTP_400_BAD_REQUEST)
                return Response({
                    'status': False,
                    'message': 'User account is deactivated'
                }, status=status.HTTP_400_BAD_REQUEST)
            except User.DoesNotExist:
                return Response({
                    'status': False,
                    'message': 'User does not exist'
                }, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


