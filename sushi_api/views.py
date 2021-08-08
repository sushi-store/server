from rest_framework.response import Response
from rest_framework.views import APIView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import rest_framework.status as status
from sushi.models import Sushi, Category
from .serializers import SushiSerializer, CategorySerializer
from itertools import chain
from django.db.models import Max, Min, Q


class SushiDetailId(APIView):

    def get(self, request, pk):
        try:
            sushi = Sushi.objects.get(pk=pk)
        except Sushi.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = SushiSerializer(sushi, context={'request': request})
        return Response(serializer.data)


class SushiDetailSlug(APIView):

    def get(self, request, slug):
        try:
            sushi = Sushi.objects.get(slug=slug)
        except Sushi.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = SushiSerializer(sushi, context={'request': request})
        return Response(serializer.data)


class SushiList(APIView):

    def execute_query(self, sort_by, is_discount, category, price_min, price_max):

        fields = ('id', 'name', 'category__category_name',
                  'quantity', 'price',)

        if sort_by in ['category', '-category']:
            if '-' in sort_by:
                sort_by = '-category__category_name'
            else:
                sort_by = 'category__category_name'

        if sort_by not in list(chain.from_iterable([['-' + field, field] for field in fields])):
            sort_by = 'name'

        sushi = Sushi.objects.filter(Q(category__category_name=category) if category else Q(
            category__category_name__isnull=False), discount__gt=0 if is_discount == 'true' else -1, price__range=(price_min, price_max)).order_by(sort_by)

        return sushi

    def get(self, request):
        data = []
        nextPage = 1
        previousPage = 1
        sort_by = request.GET.get('sort', 'id')
        is_discount = request.GET.get('discount', 'false')
        category = request.GET.get('category')
        exclude = request.GET.getlist('exclude')
        try:
            limit = int(request.GET.get('limit', Sushi.objects.all().count()))
        except:
            limit = Sushi.objects.all().count()
        price_max = request.GET.get(
            'price_max', Sushi.objects.aggregate(Max('price'))['price__max'])
        price_min = request.GET.get(
            'price_min', Sushi.objects.aggregate(Min('price'))['price__min'])

        sushi = self.execute_query(
            sort_by, is_discount, category, price_min, price_max)

        if exclude:
            for slug in exclude:
                sushi = sushi.exclude(slug=slug)

        page = request.GET.get('page', 1)
        paginator = Paginator(sushi, limit)
        try:
            data = paginator.page(page)
        except PageNotAnInteger:
            data = paginator.page(1)
        except EmptyPage:
            data = paginator.page(paginator.num_pages)

        serializer = SushiSerializer(
            data, context={'request': request}, many=True)
        if data.has_next():
            nextPage = data.next_page_number()
        if data.has_previous():
            previousPage = data.previous_page_number()

        return Response(serializer.data)


class CategoryList(APIView):

    def get(self, request):
        data = []
        nextPage = 1
        previousPage = 1
        try:
            limit = int(request.GET.get('limit', 12))
        except ValueError:
            limit = Category.objects.all().count()

        categories = Category.objects.all()

        page = request.GET.get('page', 1)
        paginator = Paginator(categories, limit)
        try:
            data = paginator.page(page)
        except PageNotAnInteger:
            data = paginator.page(1)
        except EmptyPage:
            data = paginator.page(paginator.num_pages)

        serializer = CategorySerializer(
            data, context={'request': request}, many=True)
        if data.has_next():
            nextPage = data.next_page_number()
        if data.has_previous():
            previousPage = data.previous_page_number()

        return Response(serializer.data)
