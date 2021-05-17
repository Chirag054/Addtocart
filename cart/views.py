from django.utils.translation import ugettext_lazy as _
from rest_framework import generics, serializers, status
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Cart, CartItem
from .serializers import CartSerializer, CartItemSerializer, CartItemDetailSerializer
# from .permissions import IsOwner, IsOwnerCart
from rest_framework.permissions import IsAuthenticated


class CartDetail(APIView):
    """Get a cart."""
    description = 'This route is used to get owner`s cart.'
    serializer_class = CartSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self, owner):
        try:
            return Cart.objects.get(owner=owner)
        except Cart.DoesNotExist as e:
            raise serializers.ValidationError({'not_found': _('You have no cart. Contact admin`s site.')})

    def get(self, request):
        cart = self.get_object(request.user)
        serializer = CartSerializer(cart)
        return Response(serializer.data)


class CartItemCreate(generics.CreateAPIView, generics.DestroyAPIView):

    description = 'This route is used to insert a product from user`s cart or clear the cart.'
    serializer_class = CartItemSerializer
    permission_classes = (IsAuthenticated,)
    queryset = CartItem.objects.all()

    def get_object(self):
        try:
            obj = Cart.objects.get(owner=self.request.user)
            self.check_object_permissions(self.request, obj)
            return obj
        except Cart.DoesNotExist as e:
            raise serializers.ValidationError({'not_found': _('This product does not exist.')})

    def get_serializer_context(self):
        return {'request': self.request}

    def post(self, request, format=None):
        self.get_object()
        serializer = CartItemSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        cart = self.get_object()
        cart.cartitem_set.all().delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CartItemDetail(APIView):

    description = 'This route is used to remove a single product from user`s cart.'
    serializer_class = CartItemDetailSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self, pk):
        try:
            obj = CartItem.objects.get(pk=pk, cart__owner=self.request.user)
            self.check_object_permissions(self.request, obj)
            return obj
        except Cart.DoesNotExist as e:
            raise serializers.ValidationError({'not_found': _('This product does not exist.')})

    def get(self, request, pk=None):
        cart_item = self.get_object(pk)
        serailizer = CartItemDetailSerializer(cart_item)
        return Response(serailizer.data)

    def put(self, request, pk=None):
        cart_item = self.get_object(pk)
        serializer = CartItemDetailSerializer(cart_item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk=None):
        cart_item = self.get_object(pk)
        cart_item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
