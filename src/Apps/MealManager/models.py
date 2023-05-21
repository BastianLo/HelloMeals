from tempfile import NamedTemporaryFile
from urllib.request import urlopen
from django.core.files.base import File

from django.db import models
import uuid


class Ingredient(models.Model):
    helloFreshId = models.TextField(primary_key=True, max_length=255, unique=True)

    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to="images/ingredients")


class Utensil(models.Model):
    helloFreshId = models.TextField(primary_key=True, max_length=255, unique=True)
    type = models.CharField(max_length=255)
    name = models.CharField(max_length=255)


class Nutrients(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    energyKj = models.IntegerField()
    energyKcal = models.IntegerField()
    fat = models.IntegerField()
    fatSaturated = models.IntegerField()
    carbs = models.IntegerField()
    sugar = models.IntegerField()
    protein = models.IntegerField()
    salt = models.IntegerField()


class Cuisine(models.Model):
    helloFreshId = models.TextField(primary_key=True, max_length=255, unique=True)
    type = models.CharField(max_length=255)
    name = models.CharField(max_length=255)


class Tag(models.Model):
    helloFreshId = models.TextField(primary_key=True, max_length=255, unique=True)
    type = models.CharField(max_length=255)
    name = models.CharField(max_length=255)


class Recipe(models.Model):
    helloFreshId = models.TextField(primary_key=True, max_length=255, unique=True)

    nutrients = models.ForeignKey(Nutrients, on_delete=models.CASCADE, blank=True, null=True)

    name = models.CharField(max_length=255)
    headline = models.CharField(max_length=255, blank=True, null=True)
    description = models.CharField(max_length=2000, blank=True, null=True)
    cardLink = models.CharField(max_length=2000, blank=True, null=True)
    websiteLink = models.CharField(max_length=2000, blank=True, null=True)
    prepTime = models.DurationField(blank=True, null=True)
    totalTime = models.DurationField(blank=True, null=True)
    difficulty = models.IntegerField(blank=True, null=True)
    createdAt = models.DateTimeField(blank=True, null=True)
    updatedAt = models.DateTimeField(blank=True, null=True)
    favoritesCount = models.IntegerField(blank=True, null=True)
    averageRating = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    ratingCount = models.IntegerField(blank=True, null=True)
    servings = models.IntegerField(blank=True, null=True)
    image = models.ImageField(upload_to="images/recipes", null=True)


class WorkSteps(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    relatedRecipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)

    index = models.IntegerField()
    description = models.CharField(max_length=1000)
    image = models.ImageField(upload_to="images/workSteps")


class RecipeIngredient(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)

    amount = models.DecimalField(max_digits=7, decimal_places=1)
    unit = models.CharField(max_length=255)


class RecipeTag(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)


class RecipeCuisine(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    cuisine = models.ForeignKey(Cuisine, on_delete=models.CASCADE)


class RecipeUtensil(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    utensil = models.ForeignKey(Utensil, on_delete=models.CASCADE)
