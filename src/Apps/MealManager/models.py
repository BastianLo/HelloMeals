from cached_property import cached_property_with_ttl
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import pre_delete, post_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _


class IngredientManager(models.Manager):
    def update_or_create(self, **kwargs):
        name = kwargs["defaults"]["name"]
        existing_object = self.get_queryset().filter(name=name).first()
        if existing_object:
            return existing_object, False
        return super().update_or_create(**kwargs)


class Ingredient(models.Model):
    helloFreshId = models.TextField(primary_key=True, max_length=255, unique=True)

    objects = IngredientManager()

    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to="images/ingredients", null=True, blank=True)
    HelloFreshImageUrl = models.CharField(max_length=255, null=True, blank=True)
    parent = models.ForeignKey("Ingredient", on_delete=models.SET_NULL, null=True, blank=True)

    @cached_property_with_ttl(ttl=60)
    def get_usage_count(self):
        count = RecipeIngredient.objects.filter(ingredient=self).count()
        return count

    def get_related_recipes(self):
        ingredients = [self]
        if self.parent is not None:
            ingredients += self.parent.get_descendants(include_self=True)

        recipe_ingredients = RecipeIngredient.objects.filter(ingredient__in=ingredients).values_list(
            'ingredient_group_id', flat=True)
        related_recipes = Recipe.objects.filter(ingredient_groups__id__in=recipe_ingredients).distinct()
        return related_recipes

    def get_descendants(self, include_self=True):
        descendants = []
        if include_self:
            descendants.append(self)
        for child in Ingredient.objects.filter(parent=self):
            descendants.extend(child.get_descendants(include_self=True))
        return descendants

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
    energyKj = models.IntegerField(blank=True, null=True)
    energyKcal = models.IntegerField(blank=True, null=True)
    fat = models.IntegerField(blank=True, null=True)
    fatSaturated = models.IntegerField(blank=True, null=True)
    carbs = models.IntegerField(blank=True, null=True)
    sugar = models.IntegerField(blank=True, null=True)
    protein = models.IntegerField(blank=True, null=True)
    salt = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.id


class TagGroup(models.Model):
    name = models.CharField(primary_key=True, max_length=255, unique=True)


class TagMergeManager(models.Manager):
    def create(self, **kwargs):
        source = Tag.objects.filter(helloFreshId=kwargs["source"]).first()
        target = Tag.objects.filter(helloFreshId=kwargs["target"]).first()
        delete = kwargs["delete"]
        if source is not None and (target is not None or delete):
            for t in RecipeTag.objects.filter(tag=source):
                if delete:
                    t.delete()
                    continue
                try:
                    t.tag = target
                    t.save()
                except:
                    print("Could not merge tags")
                    t.delete()
            source.delete()
        return super().create(**kwargs)


class TagMerge(models.Model):
    source = models.CharField(max_length=255, unique=True)
    target = models.CharField(max_length=255, null=True)
    delete = models.BooleanField(default=False)
    objects = TagMergeManager()


class TagQuerySet(models.query.QuerySet):
    def update_or_create(self, defaults=None, **kwargs):
        id = kwargs["helloFreshId"]
        tagMerge = TagMerge.objects.filter(source=id).first()
        while tagMerge:
            if tagMerge.delete:
                return None
            if TagMerge.objects.filter(source=tagMerge.target).first() is None:
                return Tag.objects.get_or_create(helloFreshId=tagMerge.target)
            tagMerge = TagMerge.objects.filter(source=tagMerge.target).first()

        return super().update_or_create(defaults=defaults, **kwargs)

    def get(self, **kwargs):
        id = kwargs["helloFreshId"]
        tagMerge = TagMerge.objects.filter(source=id).first()
        while tagMerge:
            if tagMerge.delete:
                return None
            if TagMerge.objects.filter(source=tagMerge.target).first() is None:
                return Tag.objects.get_or_create(helloFreshId=tagMerge.target)[0]
            tagMerge = TagMerge.objects.filter(source=tagMerge.target).first()
        return super().get(**kwargs)


class TagManager(models.Manager):
    def get_queryset(self):
        return TagQuerySet(self.model)


class Tag(models.Model):
    helloFreshId = models.TextField(primary_key=True, max_length=255, unique=True)
    type = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    tagGroup = models.ForeignKey(TagGroup, on_delete=models.SET_NULL, blank=True, null=True)

    objects = TagManager()

    def __str__(self):
        return f"{self.name} ({self.helloFreshId})"


class IngredientGroup(models.Model):
    id = models.TextField(primary_key=True, max_length=255, unique=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    related_recipe = models.ForeignKey("Recipe", on_delete=models.CASCADE, null=True, related_name='ingredient_groups')


class Recipe(models.Model):
    helloFreshId = models.TextField(primary_key=True, max_length=255, unique=True)

    # Source: 1 = HelloFresh, 2 = KitchenStories
    source = models.IntegerField(default=1)

    nutrients = models.ForeignKey(Nutrients, on_delete=models.SET_NULL, blank=True, null=True)

    favoriteBy = models.ManyToManyField(User, related_name='favorite_recipes')

    class RecipeTypes(models.IntegerChoices):
        main = 0, _("Hauptgericht")
        breakfast = 1, _("Frühstück")
        dessert = 2, _("Dessert")
        baking = 3, _("Backen")
        drink = 4, _("Getränke")

    recipeType = models.IntegerField(
        choices=RecipeTypes.choices,
        default=RecipeTypes.main,
    )

    ### Shared ###
    # All
    name = models.CharField(max_length=255)
    author = models.CharField(max_length=255, blank=True, null=True)
    websiteLink = models.CharField(max_length=2000, blank=True, null=True)
    prepTime = models.DurationField(blank=True, null=True)
    totalTime = models.DurationField(blank=True, null=True)
    difficulty = models.IntegerField(blank=True, null=True)
    createdAt = models.DateTimeField(blank=True, null=True)
    updatedAt = models.DateTimeField(blank=True, null=True)
    averageRating = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    ratingCount = models.IntegerField(blank=True, null=True)
    servings = models.IntegerField(blank=True, null=True)
    image = models.ImageField(upload_to="images/recipes", null=True)
    HelloFreshImageUrl = models.CharField(max_length=255, null=True)
    # HelloFresh & Chefkoch
    isPremium = models.BooleanField(blank=True, null=True)
    headline = models.CharField(max_length=255, blank=True, null=True)
    videoLink = models.CharField(max_length=2000, blank=True, null=True)
    isExcludedFromIndex = models.BooleanField(blank=True, null=True)
    # HelloFresh & KitchenStories
    description = models.CharField(max_length=10000, blank=True, null=True)
    favoritesCount = models.IntegerField(blank=True, null=True)

    # HelloFresh Only
    helloFreshActive = models.BooleanField(default=True, blank=True, null=True)
    cardLink = models.CharField(max_length=2000, blank=True, null=True)
    clonedFrom = models.CharField(max_length=255, blank=True, null=True)
    highlighted = models.BooleanField(blank=True, null=True)
    isAddon = models.BooleanField(blank=True, null=True)
    isComplete = models.BooleanField(blank=True, null=True)
    isDinnerToLunch = models.BooleanField(blank=True, null=True)

    # KitchenStories Only

    # Chefkoch Only
    viewCount = models.IntegerField(blank=True, null=True)
    isPlus = models.BooleanField(blank=True, null=True)

    # EatSmarter only
    healthScore = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return f"{self.name} ({self.helloFreshId})"

    def delete(self, *args, **kwargs):
        # Delete related ingredient groups before deleting the recipe
        self.ingredient_groups.all().delete()
        super().delete(*args, **kwargs)


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
    ingredient_group = models.ForeignKey(IngredientGroup, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)

    amount = models.DecimalField(max_digits=7, decimal_places=1, null=True, blank=True)
    unit = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"{self.ingredient} ({self.ingredient_group})"


class RecipeTag(models.Model):
    id = models.TextField(primary_key=True, max_length=255, unique=True)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)

    # class Meta:
    #    unique_together = ('recipe', 'tag',)
    def __str__(self):
        return f"{self.recipe} ({self.tag})"


class RecipeUtensil(models.Model):
    id = models.TextField(primary_key=True, max_length=255, unique=True)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    utensil = models.ForeignKey(Utensil, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.recipe} ({self.utensil})"


@receiver(pre_delete, sender=Recipe)
def delete_related_ingredient_groups(sender, instance, **kwargs):
    instance.ingredient_groups.all().delete()


class Stock(models.Model):
    ingredients = models.ManyToManyField(Ingredient, blank=True)
    name = models.CharField(max_length=255)

    def add(self, ingredient: Ingredient):
        while ingredient.parent is not None:
            ingredient = ingredient.parent
        if self.ingredients.filter(helloFreshId=ingredient.helloFreshId).exists():
            return False
        self.ingredients.add(ingredient)
        return True

    def remove(self, ingredient: Ingredient):
        while ingredient.parent is not None:
            ingredient = ingredient.parent
        if not self.ingredients.filter(helloFreshId=ingredient.helloFreshId).exists():
            return False
        self.ingredients.remove(ingredient)
        return True

    def __str__(self):
        return f"Stock {self.name}"


class ShoppingList(models.Model):
    ingredients = models.ManyToManyField(Ingredient, blank=True)
    stock = models.OneToOneField(Stock, on_delete=models.CASCADE)

    def add(self, ingredient: Ingredient):
        while ingredient.parent is not None:
            ingredient = ingredient.parent
        if self.ingredients.filter(helloFreshId=ingredient.helloFreshId).exists():
            return False
        self.ingredients.add(ingredient)
        return True

    def remove(self, ingredient: Ingredient):
        while ingredient.parent is not None:
            ingredient = ingredient.parent
        if not self.ingredients.filter(helloFreshId=ingredient.helloFreshId).exists():
            return False
        self.ingredients.remove(ingredient)
        return True

    def __str__(self):
        return f"Shopping List {self.stock.name}"


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    stock = models.ForeignKey(Stock, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"Profile {self.user}"


@receiver(post_save, sender=Stock)
def create_shopping_list(sender, instance, created, **kwargs):
    if created:
        ShoppingList.objects.create(stock=instance)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
