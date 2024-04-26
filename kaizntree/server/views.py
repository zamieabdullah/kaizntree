from django.http import HttpResponse
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime, timedelta
from rest_framework_simplejwt.tokens import AccessToken
from jwt.exceptions import InvalidTokenError

from .models import User, Category, Item
from .serializer import UserSerializer, CategorySerializer, ItemSerializer

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
            access_token = AccessToken()
            access_token['user_id'] = user.id
            access_token['exp'] = access_token.current_time + timedelta(days=7)  # Custom expiration time (e.g., 7 days)

            # Create a response with the access token set as a cookie
            response = HttpResponse({'message': 'Login successful'})
            response.set_cookie('access_token', str(access_token), httponly=False)
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

            access_token = AccessToken()
            access_token['user_id'] = user.id
            access_token['exp'] = access_token.current_time + timedelta(days=7)  # Custom expiration time (e.g., 7 days)

            # Create a response with the access token set as a cookie
            response = HttpResponse({'message': 'Login successful'})
            response.set_cookie('access_token', str(access_token), httponly=False)
            return response


        return Response({'message': 'server error'},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class UserCategoryAPIView(APIView):
    def get_user_id_from_token(self, request):
        try:
            # Extract the JWT token from the request headers
            authorization_header = request.headers.get('CSRFToken')
            token = authorization_header.split()[1]  # Extract token from "Bearer <token>"
            
            # Decode the JWT token
            decoded_token = AccessToken(token)
            user_id = decoded_token['user_id']
            
            return user_id
        except (IndexError, InvalidTokenError, KeyError):
            # Handle token extraction or decoding errors
            return None

    def get(self, request):
         # Ensure that the user_id is present in the JWT token
        user_id = self.get_user_id_from_token(request)
        if not user_id:
            return Response({'error': 'User ID is missing in the JWT token'}, status=status.HTTP_400_BAD_REQUEST)

        # Retrieve categories for the authenticated user
        queryset = Category.objects.filter(user_id=user_id)
        serializer = CategorySerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        user_id = self.get_user_id_from_token(request)
        if not user_id:
            return Response({'error': 'User ID is missing in the JWT token'}, status=status.HTTP_400_BAD_REQUEST)
        category_name = request.data.get('name')
        queryset = Category.objects.filter(user=user_id, name=category_name)
        
        if queryset.exists():
            return Response({'error': 'Category already exists'}, status=status.HTTP_409_CONFLICT)

        new_category = Category(name=category_name, user=user_id)  
        new_category.save();  

        return Response({'message': 'Category added'}, status=status.HTTP_201_CREATED)
    
class UserItemsAPIView(APIView):
    def get_user_id_from_token(self, request):
        try:
            # Extract the JWT token from the request headers
            authorization_header = request.headers.get('CSRFToken')
            token = authorization_header.split()[1]  # Extract token from "Bearer <token>"
            
            # Decode the JWT token
            decoded_token = AccessToken(token)
            user_id = decoded_token['user_id']
            
            return user_id
        except (IndexError, InvalidTokenError, KeyError):
            # Handle token extraction or decoding errors
            return None
        
    def get(self, request):
        user_id = self.get_user_id_from_token(request)
        if not user_id:
            return Response({'error': 'User ID is missing in the JWT token'}, status=status.HTTP_400_BAD_REQUEST)
        
        queryset = Item.objects.filter(owner=user_id)
        serializer = ItemSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
        
    def post(self, request):
        user_id = self.get_user_id_from_token(request)
        if not user_id:
            return Response({'error': 'User ID is missing in the JWT token'}, status=status.HTTP_400_BAD_REQUEST)
        
        if Item.objects.filter(owner=user_id, sku=request.data["sku"]).exists():
            return Response({'error': 'This item already exists'}, status=status.HTTP_409_CONFLICT)
        
        data = request.data

        category_name = data.pop('category')
        category = Category.objects.get(name=category_name, user_id=user_id)
        item = Item(category=category, owner_id=user_id, **data)
        item.save()

        return Response(status=status.HTTP_201_CREATED)
        
