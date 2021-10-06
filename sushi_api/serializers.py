from rest_framework import serializers
from sushi.models import Sushi, Category, Ingredient


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

    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'nameRus', 'nameUkr', 'image',)


class SushiSerializer(serializers.ModelSerializer):
    categoryNames = CategorySerializer(source='category', read_only=True)
    ingredients = IngredientSerializer(many=True, read_only=True)
    image = serializers.ImageField(
        max_length=None, use_url=True, read_only=True
    )

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
