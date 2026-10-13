from decimal import Decimal

from rest_framework import serializers

from products.models import Product
from .models import Cart, CartItem


class AddToCartSerializer(serializers.Serializer):
    product = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all()
    )
    quantity = serializers.IntegerField(
        required=False,
        default=1,
        min_value=1,
    )


class UpdateCartItemSerializer(serializers.Serializer):
    quantity = serializers.IntegerField(min_value=1)


class CartItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(
        source='product.name',
        read_only=True,
    )

    product_price = serializers.DecimalField(
        source='product.price',
        max_digits=10,
        decimal_places=2,
        read_only=True,
    )

    product_image = serializers.ImageField(
        source='product.image',
        read_only=True,
    )

    class Meta:
        model = CartItem
        fields = [
            'id',
            'product',
            'product_name',
            'product_price',
            'product_image',
            'quantity',
        ]
        read_only_fields = [
            'id',
            'product_name',
            'product_price',
            'product_image',
        ]

    def validate_quantity(self, value):
        if value < 1:
            raise serializers.ValidationError(
                "Quantity must be at least 1."
            )
        return value


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = [
            'id',
            'user',
            'created_at',
            'items',
            'total_price',
        ]
        read_only_fields = [
            'id',
            'user',
            'created_at',
            'items',
            'total_price',
        ]

    def get_total_price(self, obj):
        return sum(
            (
                item.product.price * item.quantity
                for item in obj.items.select_related('product').all()
            ),
            Decimal('0.00'),
        )
        
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["created_at"] = instance.created_at.strftime("%Y-%m-%d %H:%M")
        return data