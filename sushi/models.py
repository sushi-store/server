from django.db import models
from .slugify import slugify
from cloudinary.models import CloudinaryField


class Category(models.Model):
    category_name = models.CharField(max_length=100, null=False, unique=True)
    category_name_uk = models.CharField(max_length=100, null=False)

    def __str__(self) -> str:
        return self.category_name

    class Meta:
        verbose_name_plural = "Categories"


class Ingredient(models.Model):
    name = models.CharField(max_length=100, null=False, unique=True)
    name_uk = models.CharField(max_length=100, null=False)

    image = CloudinaryField(folder='ingredients_img')

    def __str__(self) -> str:
        return f'{self.name}'

    class Meta:
        verbose_name_plural = "Ingredients"


class Sushi(models.Model):
    name = models.CharField(max_length=100, null=False)
    name_uk = models.CharField(max_length=100, default='', null=False)
    image = CloudinaryField(folder='sushi_img')
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name='category')
    ingredients = models.ManyToManyField(
        Ingredient, through='SetOfIngredients')
    description = models.TextField(default='')
    description_uk = models.TextField(default='')
    quantity = models.PositiveSmallIntegerField(default=1)
    price = models.DecimalField(default=0.0, max_digits=6, decimal_places=2)
    discount = models.DecimalField(default=0.0, max_digits=3, decimal_places=2)
    slug = models.SlugField(max_length=255)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Sushi, self).save(*args, **kwargs)

    def is_discounted(self):
        if self.discount > 0:
            return True
        else:
            return False

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name_plural = "Sushi"


class SetOfIngredients(models.Model):
    sushi = models.ForeignKey(Sushi, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.ingredient.name
