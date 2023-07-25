from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User as DjangoUser
from django.contrib.auth import authenticate, login
from .models import User
from .serializers import UserSerializer

@api_view(['POST'])
def register_user(request):
    username = request.data.get('username')
    password = request.data.get('password')
    email = request.data.get('email')
    roles = request.data.get('roles')  # Assuming roles are sent as a list of role IDs

    if not username or not password or not email or not roles:
        return Response({'error': 'Missing required fields'}, status=status.HTTP_400_BAD_REQUEST)

    # Create a new Django User object and associate it with the custom User model
    django_user = DjangoUser.objects.create_user(username=username, password=password, email=email)
    custom_user = User.objects.create(username=username, email=email)
    custom_user.roles.set(roles)  # Set the user's roles

    return Response({'message': 'User registered successfully'}, status=status.HTTP_201_CREATED)

@api_view(['POST'])
def user_login(request):
    username = request.data.get('username')
    password = request.data.get('password')

    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return Response({'message': 'Login successful'})
    else:
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['GET'])
def get_users(request):
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)

