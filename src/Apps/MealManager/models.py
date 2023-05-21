from django.db import models
import uuid

class Ingredient(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    helloFreshId = models.CharField(max_length=255)

    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to="images/ingredients")


class Utensil(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    helloFreshId = models.CharField(primary_key=True, max_length=255)
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
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    helloFreshId = models.CharField(max_length=255)
    type = models.CharField(max_length=255)
    name = models.CharField(max_length=255)


class Tag(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    helloFreshId = models.CharField(max_length=255)
    type = models.CharField(max_length=255)
    name = models.CharField(max_length=255)


class Recipe(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    helloFreshId = models.CharField(max_length=255)

    nutrients = models.ForeignKey(Nutrients, on_delete=models.CASCADE)

    name = models.CharField(max_length=255)
    headline = models.CharField(max_length=255)
    description = models.CharField(max_length=2000)
    cardLink = models.CharField(max_length=2000)
    websiteLink = models.CharField(max_length=2000)
    prepTime = models.DurationField()
    totalTime = models.DurationField()
    difficulty = models.IntegerField()
    createdAt = models.DateTimeField()
    updatedAt = models.DateTimeField()
    favoritesCount = models.IntegerField()
    averageRating = models.DecimalField(max_digits=5, decimal_places=2)
    ratingCount = models.IntegerField()
    servings = models.IntegerField()
    image = models.ImageField(upload_to="images/recipes")


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
