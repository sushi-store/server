from rest_framework.response import Response
from rest_framework.views import APIView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import rest_framework.status as status
from order.models import Order
from .serializers import OrderSerializer
from rest_framework.permissions import IsAuthenticated
import re


class OrderDetailUserId(APIView):

    def get(self, request, pk):
        try:
            orders = Order.objects.filter(user_id=pk)
        except Order.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = OrderSerializer(
            orders, context={'request': request}, many=True)

        return Response(serializer.data)


class OrderDetailUUId(APIView):

    def get(self, request, uuid):
        try:
            orders = Order.objects.filter(uuid=uuid)
        except Order.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = OrderSerializer(
            orders, context={'request': request}, many=True)

        return Response(serializer.data)


class CreateOrder(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        request.data.update({"userId": request.user.id, "uuid": None})
        order_serializer = OrderSerializer(data=request.data)
        if order_serializer.is_valid():
            order = order_serializer.save()
            if order:
                return Response(status=status.HTTP_201_CREATED)
        return Response(order_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CreateTempOrder(APIView):

    def post(self, request):
        request.data.update({"userId": None})
        if not re.match(r"[a-zA-Z0-9]{8}-[a-zA-Z0-9]{4}-[a-zA-Z0-9]{4}-[a-zA-Z0-9]{4}-[a-zA-Z0-9]{12}", request.data.get("uuid", "")):
            return Response("UUId not matches a format.", status=status.HTTP_400_BAD_REQUEST)
        order_serializer = OrderSerializer(data=request.data)
        if order_serializer.is_valid():
            order = order_serializer.save()
            if order:
                return Response(status=status.HTTP_201_CREATED)
        return Response(order_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OrdersList(APIView):

    def get(self, request):
        orders = Order.objects.all()
        page = request.GET.get('page', 1)
        paginator = Paginator(orders, 10)
        try:
            data = paginator.page(page)
        except PageNotAnInteger:
            data = paginator.page(1)
        except EmptyPage:
            data = paginator.page(paginator.num_pages)

        serializer = OrderSerializer(
            data, context={'request': request}, many=True)

        return Response(serializer.data)
