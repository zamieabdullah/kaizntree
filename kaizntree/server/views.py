from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime
from rest_framework_simplejwt.views import TokenObtainPairView

from .utils import obtain_jwt_tokens
from .models import User, Category, Tag, Item
from .serializer import UserSerializer, CategorySerializer, TagSerializer, ItemSerializer

class UserInfoAPIView(APIView):
    def post(self, request):
        email_address = request.data.get('email_address')
        password = request.data.get('password')

        if not email_address or not password:
            return Response({'error': 'Both email address and password are required'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            # Retrieve the user object with the provided email address
            user = User.objects.get(email_address=email_address)
        except User.DoesNotExist:
            # User with the provided email address does not exist
            return Response({'error': 'Email address does not exist'}, status=status.HTTP_404_NOT_FOUND)

        # Check if the provided password is correct
        if user.validate_password(password):
            # Password is correct
            tokens = obtain_jwt_tokens(user)
            response = JsonResponse({'message': 'Login successful'})
            response.set_cookie('access_token', tokens['access'], httponly=True)
            return response
        else:
            # Password is incorrect
            return Response({'error': 'Invalid email address or password'}, status=status.HTTP_401_UNAUTHORIZED)

class UserRegisterAPIView(APIView):
    def post(self, request):
        new_user = request.data

        current_time = datetime.now()
        new_user['created_at'] = current_time.strftime("%Y-%m-%dT%H:%M:%S")

        if User.objects.filter(email_address=new_user['email_address']).exists():
            return Response({'error': 'User with this email address already exists'}, status=status.HTTP_409_CONFLICT)

        serializer = UserSerializer(data=new_user)
        
        if serializer.is_valid():
            valid_data = serializer.validated_data

            user = User.objects.create(
                email_address=valid_data['email_address'],
                created_at=valid_data['created_at']
            )
            user.set_password(valid_data['password'])  # Hash the password
            user.save()

            tokens = obtain_jwt_tokens(user)
            response = JsonResponse({'message': 'Login successful'})
            response.set_cookie('access_token', tokens['access'], httponly=True)

            return response


        return Response({'message': 'server error'},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
