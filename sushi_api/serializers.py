from rest_framework import serializers
from sushi.models import Sushi, Category, Ingredient
from django.conf import settings
import os


class CategorySerializer(serializers.ModelSerializer):
    categoryName = serializers.CharField(source='category_name')
    categoryNameRus = serializers.CharField(
        source='category_name_rus')
    categoryNameUkr = serializers.CharField(
        source='category_name_ukr')

    class Meta:
        model = Category
        fields = ('categoryName', 'categoryNameRus', 'categoryNameUkr',)


class IngredientSerializer(serializers.ModelSerializer):
    nameRus = serializers.CharField(source='name_rus')
    nameUkr = serializers.CharField(source='name_ukr')
    image = serializers.SerializerMethodField()

    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'nameRus', 'nameUkr', 'image',)

    def get_image(self, obj):
        request = self.context.get('request')
        img_url = request.build_absolute_uri(obj.image.url).replace(
            '/' + obj.image.name, settings.STATIC_URL + os.path.basename(obj.image.name))
        return img_url


class SushiSerializer(serializers.ModelSerializer):
    categoryNames = CategorySerializer(source='category', read_only=True)
    ingredients = IngredientSerializer(many=True, read_only=True)
    image = serializers.SerializerMethodField()

    next_slug = serializers.SerializerMethodField('get_next_slug')
    prev_slug = serializers.SerializerMethodField('get_prev_slug')

    def get_next_slug(self, sushi):
        try:
            slug = Sushi.objects.get(pk=sushi.id + 1).slug
        except Sushi.DoesNotExist:
            slug = Sushi.objects.order_by('id').first().slug
        return slug

    def get_prev_slug(self, sushi):
        try:
            slug = Sushi.objects.get(pk=sushi.id - 1).slug
        except Sushi.DoesNotExist:
            slug = Sushi.objects.order_by('id').last().slug
        return slug

    class Meta:
        model = Sushi
        fields = ('id', 'slug', 'name', 'description', 'image', 'categoryNames', 'ingredients',
                  'quantity', 'price', 'discount', 'next_slug', 'prev_slug',)
        read_only_fields = ('name', 'description', 'image', 'categoryNames', 'ingredients',
                            'quantity', 'price', 'discount', 'next_slug', 'prev_slug',)

    def get_image(self, obj):
        request = self.context.get('request')
        img_url = request.build_absolute_uri(obj.image.url).replace(
            '/' + obj.image.name, settings.STATIC_URL + os.path.basename(obj.image.name))
        return img_url
