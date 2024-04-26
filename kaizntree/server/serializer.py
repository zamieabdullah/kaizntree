from rest_framework.serializers import ModelSerializer, SerializerMethodField

from .models import User, Category, Item

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
        
class ItemSerializer(ModelSerializer):
    category_name = SerializerMethodField()

    class Meta:
        model = Item
        fields = (
            'id',
            'sku',
            'name',
            'category_name',
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

    def get_category_name(self, obj):
        return obj.category.name