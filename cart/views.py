from django.db import transaction
from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from drf_spectacular.utils import extend_schema

from products.models import Product
from .models import Cart, CartItem
from .serializers import (
    AddToCartSerializer,
    UpdateCartItemSerializer,
    CartSerializer,
)


class CartView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        cart, _ = Cart.objects.get_or_create(user=request.user)

        cart = Cart.objects.prefetch_related(
            'items__product'
        ).get(pk=cart.pk)

        return Response(CartSerializer(cart).data)

    @extend_schema(
        request=AddToCartSerializer,
        responses={200: CartSerializer},
    )
    def post(self, request):
        input_serializer = AddToCartSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)

        product_id = input_serializer.validated_data['product'].pk
        quantity = input_serializer.validated_data['quantity']

        with transaction.atomic():
            product = get_object_or_404(
                Product.objects.select_for_update(),
                pk=product_id,
            )

            cart, _ = Cart.objects.get_or_create(user=request.user)

            item = (
                CartItem.objects.select_for_update()
                .filter(cart=cart, product=product)
                .first()
            )

            current_quantity = item.quantity if item else 0
            new_quantity = current_quantity + quantity

            if new_quantity > product.stock:
                return Response(
                    {'error': 'Not enough product in stock.'},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            if item:
                item.quantity = new_quantity
                item.save(update_fields=['quantity'])
            else:
                CartItem.objects.create(
                    cart=cart,
                    product=product,
                    quantity=quantity,
                )

        cart = Cart.objects.prefetch_related(
            'items__product'
        ).get(pk=cart.pk)

        return Response(
            CartSerializer(cart).data,
            status=status.HTTP_200_OK,
        )


class CartItemView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        request=UpdateCartItemSerializer,
        responses={200: CartSerializer},
    )
    def patch(self, request, item_id):
        input_serializer = UpdateCartItemSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)
        quantity = input_serializer.validated_data['quantity']

        with transaction.atomic():
            item = get_object_or_404(
                CartItem.objects.select_for_update(),
                pk=item_id,
                cart__user=request.user,
            )

            product = get_object_or_404(
                Product.objects.select_for_update(),
                pk=item.product_id,
            )

            if quantity > product.stock:
                return Response(
                    {'error': 'Not enough product in stock.'},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            item.quantity = quantity
            item.save(update_fields=['quantity'])
            cart_id = item.cart_id

        cart = Cart.objects.prefetch_related(
            'items__product'
        ).get(pk=cart_id)

        return Response(CartSerializer(cart).data)

    def delete(self, request, item_id):
        with transaction.atomic():
            item = get_object_or_404(
                CartItem.objects.select_for_update(),
                pk=item_id,
                cart__user=request.user,
            )

            cart_id = item.cart_id
            item.delete()

        cart = Cart.objects.prefetch_related(
            'items__product'
        ).get(pk=cart_id)

        return Response(CartSerializer(cart).data)


class ClearCartView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        cart, _ = Cart.objects.get_or_create(user=request.user)

        with transaction.atomic():
            cart.items.all().delete()

        cart = Cart.objects.prefetch_related(
            'items__product'
        ).get(pk=cart.pk)

        return Response(CartSerializer(cart).data)