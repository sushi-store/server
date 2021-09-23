from rest_framework.response import Response
from rest_framework.views import APIView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import rest_framework.status as status
from order.models import Order
from .serializers import OrderSerializer


class OrderDetailId(APIView):

    def get(self, request, pk):
        try:
            order = Order.objects.get(pk=pk)
        except Order.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = OrderSerializer(order, context={'request': request})
        return Response(serializer.data)


class CreateOrder(APIView):

    def post(self, request):
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
