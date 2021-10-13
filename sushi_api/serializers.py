from rest_framework import serializers
from sushi.models import Sushi, Category, Ingredient


class CategorySerializer(serializers.ModelSerializer):
    categoryName = serializers.SerializerMethodField('get_category_name')

    def get_category_name(self, category):
        return {'en': category.category_name, 'ukr': category.category_name_ukr}

    class Meta:
        model = Category
        fields = ('categoryName',)


class IngredientSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField('get_name')
    image = serializers.SerializerMethodField()

    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'image',)

    def get_name(self, ingredient):
        return {'en': ingredient.name, 'ukr': ingredient.name_ukr}

    def get_image(self, obj):
        return str(obj.image.url)


class SushiSerializer(serializers.ModelSerializer):
    categoryName = serializers.SerializerMethodField('get_category_name')
    ingredients = IngredientSerializer(many=True, read_only=True)
    image = serializers.SerializerMethodField()

    name = serializers.SerializerMethodField('get_name')
    description = serializers.SerializerMethodField('get_description')
    next_slug = serializers.SerializerMethodField('get_next_slug')
    prev_slug = serializers.SerializerMethodField('get_prev_slug')

    def get_name(self, sushi):
        return {"en": sushi.name, "ukr": sushi.name_ukr}

    def get_description(self, sushi):
        return {"en": sushi.description, "ukr": sushi.description_ukr}

    def get_category_name(self, sushi):
        return {"en": sushi.category.category_name, "ukr": sushi.category.category_name_ukr}

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
        fields = ('id', 'slug', 'name', 'description', 'image', 'categoryName', 'ingredients',
                  'quantity', 'price', 'discount', 'next_slug', 'prev_slug',)
        read_only_fields = ('name', 'description', 'image', 'categoryNames', 'ingredients',
                            'quantity', 'price', 'discount', 'next_slug', 'prev_slug',)

    def get_image(self, obj):
        return str(obj.image.url)
