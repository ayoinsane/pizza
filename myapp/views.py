from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.shortcuts import get_object_or_404
from django.db import transaction
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from .models import Category, Product, Cart, CartItem, Order, OrderItem
from .serializers import (
    CategorySerializer, ProductSerializer, 
    CartSerializer, CartItemSerializer, 
    OrderSerializer
)

class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]

class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.filter(is_available=True)
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]

@method_decorator(csrf_exempt, name='dispatch')
class CartViewSet(viewsets.ModelViewSet):
    serializer_class = CartSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Cart.objects.filter(user=self.request.user)
        user = User.objects.first()
        if user:
            cart, _ = Cart.objects.get_or_create(user=user)
            return Cart.objects.filter(user=user)
        return Cart.objects.none()

    @action(detail=False, methods=['post'])
    def add_item(self, request):
        user = request.user
        if not user.is_authenticated:
            user = User.objects.first()
            if not user:
                return Response({'error': 'Нет пользователей в базе'}, status=status.HTTP_400_BAD_REQUEST)

        cart, _ = Cart.objects.get_or_create(user=user)
        product_id = request.data.get('product_id')
        quantity = int(request.data.get('quantity', 1))
        
        product = get_object_or_404(Product, id=product_id)
        
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        if not created:
            cart_item.quantity += quantity
        else:
            cart_item.quantity = quantity
        cart_item.save()

        return Response({'status': 'Товар добавлен в корзину'}, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['post'])
    def remove_item(self, request):
        user = request.user
        if not user.is_authenticated:
            user = User.objects.first()
            
        cart, _ = Cart.objects.get_or_create(user=user)
        item_id = request.data.get('item_id')
        
        item = get_object_or_404(CartItem, id=item_id, cart=cart)
        item.delete()
        return Response({'status': 'Товар удален'}, status=status.HTTP_204_NO_CONTENT)

class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Order.objects.filter(user=self.request.user).order_by('-created_at')
        user = User.objects.first()
        if user:
            return Order.objects.filter(user=user).order_by('-created_at')
        return Order.objects.none()

    def create(self, request, *args, **kwargs):
        user = request.user
        if not user.is_authenticated:
            user = User.objects.first()

        cart = get_object_or_404(Cart, user=user)
        cart_items = cart.items.all()

        if not cart_items:
            return Response({'error': 'Корзина пуста'}, status=status.HTTP_400_BAD_REQUEST)

        address = request.data.get('address')
        comment = request.data.get('comment', '')
        
        if not address:
            return Response({'error': 'Укажите адрес доставки'}, status=status.HTTP_400_BAD_REQUEST)

        total_price = sum([item.product.price * item.quantity for item in cart_items])

        with transaction.atomic():
            order = Order.objects.create(
                user=user,
                address=address,
                comment=comment,
                total_price=total_price,
                status='new'
            )

            for item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    quantity=item.quantity,
                    price=item.product.price
                )
            
            cart_items.delete()

        serializer = self.get_serializer(order)
        return Response(serializer.data, status=status.HTTP_201_CREATED)