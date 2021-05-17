from rest_framework import serializers
from rest_framework.relations import PrimaryKeyRelatedField
from .models import Cart, CartItem
from product.models import Product
from product.serializers import ProductResumeSerializer


class CartSerializer(serializers.ModelSerializer):

    created_at = serializers.DateTimeField(format="%d/%m/%Y %H:%M:%S", read_only=True)
    updated_at = serializers.DateTimeField(format="%d/%m/%Y %H:%M:%S", read_only=True)
    items = serializers.SerializerMethodField()
    total = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        exclude = ('owner', 'item',)

    def get_items(self, obj):
        return CartItemResumeSerializer(obj.cartitem_set.all(), many=True).data

    def get_total(self, obj):
        return obj.get_total()


class CartItemResumeSerializer(serializers.ModelSerializer):

    product = ProductResumeSerializer()

    class Meta:
        model = CartItem
        exclude = ('cart',)


class CartItemSerializer(serializers.ModelSerializer):
 
    class Meta:
        model = CartItem
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(CartItemSerializer, self).__init__(*args, **kwargs)
        user = self.context['request'].user
        # overriding field to Browsable API show only user's cart in option
        self.fields['cart'] = PrimaryKeyRelatedField(queryset=Cart.objects.filter(owner=user), required=True)
        self.fields['product'] = PrimaryKeyRelatedField(queryset=Product.objects.filter(is_active=True), required=True)


class CartItemDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = CartItem
        fields = '__all__'
        # exclude = ('cart',)
        extra_kwargs = {
            'cart': {'read_only': True},
            'product': {'read_only': True},
        }
