from rest_framework.serializers import ModelSerializer

from .models import User, Category, Tag, Item

class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'email_address',
            'password',
            'created_at',
        )
        
class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = (
            'id',
            'name',
            'user',
        )
        
class TagSerializer(ModelSerializer):
    class Meta:
        model = Tag
        fields = (
            'id',
            'name',
        )
        
class ItemSerializer(ModelSerializer):
    class Meta:
        model = Item
        fields = (
            'id',
            'sku',
            'category',
            'tags',
            'in_stock',
            'available_stock',
            'owner',
            'units',
            'minimum_stock',
            'desired_stock',
            'cost',
            'created_at',
            'updated_at',
        )