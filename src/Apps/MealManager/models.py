from tempfile import NamedTemporaryFile
from urllib.request import urlopen
from django.core.files.base import File

from django.db import models
import uuid


class Ingredient(models.Model):
    helloFreshId = models.TextField(primary_key=True, max_length=255, unique=True)

    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to="images/ingredients")
    HelloFreshImageUrl = models.CharField(max_length=255, null=True)

    def __str__(self):
        return f"{self.name} ({self.helloFreshId})"


class Utensil(models.Model):
    helloFreshId = models.TextField(primary_key=True, max_length=255, unique=True)
    type = models.CharField(max_length=255, null=True, blank=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.name} ({self.helloFreshId})"


class Nutrients(models.Model):
    id = models.TextField(primary_key=True, max_length=255, unique=True)
    energyKj = models.IntegerField()
    energyKcal = models.IntegerField()
    fat = models.IntegerField()
    fatSaturated = models.IntegerField()
    carbs = models.IntegerField()
    sugar = models.IntegerField()
    protein = models.IntegerField()
    salt = models.IntegerField()

    def __str__(self):
        return self.id


class Cuisine(models.Model):
    helloFreshId = models.TextField(primary_key=True, max_length=255, unique=True)
    type = models.CharField(max_length=255)
    name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.name} ({self.helloFreshId})"


class Tag(models.Model):
    helloFreshId = models.TextField(primary_key=True, max_length=255, unique=True)
    type = models.CharField(max_length=255)
    name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.name} ({self.helloFreshId})"


class Recipe(models.Model):
    helloFreshId = models.TextField(primary_key=True, max_length=255, unique=True)

    nutrients = models.ForeignKey(Nutrients, on_delete=models.CASCADE, blank=True, null=True)

    name = models.CharField(max_length=255)
    helloFreshActive = models.BooleanField(default=True)
    highlighted = models.BooleanField(blank=True, null=True)
    isAddon = models.BooleanField(blank=True, null=True)
    isComplete = models.BooleanField(blank=True, null=True)
    isDinnerToLunch = models.BooleanField(blank=True, null=True)
    isExcludedFromIndex = models.BooleanField(blank=True, null=True)
    isPremium = models.BooleanField(blank=True, null=True)
    author = models.CharField(max_length=255, blank=True, null=True)
    headline = models.CharField(max_length=255, blank=True, null=True)
    description = models.CharField(max_length=10000, blank=True, null=True)
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
    HelloFreshImageUrl = models.CharField(max_length=255, null=True)

    def __str__(self):
        return f"{self.name} ({self.helloFreshId})"


class WorkSteps(models.Model):
    id = models.TextField(primary_key=True, max_length=255, unique=True)
    relatedRecipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)

    index = models.IntegerField()
    description = models.CharField(max_length=10000)
    image = models.ImageField(upload_to="images/workSteps")
    HelloFreshImageUrl = models.CharField(max_length=255, null=True)

    def __str__(self):
        return self.id


class RecipeIngredient(models.Model):
    id = models.TextField(primary_key=True, max_length=255, unique=True)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)

    amount = models.DecimalField(max_digits=7, decimal_places=1, null=True, blank=True)
    unit = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"{self.ingredient} ({self.recipe})"


class RecipeTag(models.Model):
    id = models.TextField(primary_key=True, max_length=255, unique=True)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.recipe} ({self.tag})"


class RecipeCuisine(models.Model):
    id = models.TextField(primary_key=True, max_length=255, unique=True)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    cuisine = models.ForeignKey(Cuisine, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.recipe} ({self.cuisine})"


class RecipeUtensil(models.Model):
    id = models.TextField(primary_key=True, max_length=255, unique=True)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    utensil = models.ForeignKey(Utensil, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.recipe} ({self.utensil})"
