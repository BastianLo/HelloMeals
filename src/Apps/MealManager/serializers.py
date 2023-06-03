from rest_framework import serializers

from .models import *


### Cuisine ###
class TagBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = "__all__"


### Ingredient ###

class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = "__all__"


class RecipeIngredientSerializer(serializers.ModelSerializer):
    ingredient = IngredientSerializer()

    class Meta:
        model = RecipeIngredient
        exclude = ["recipe"]


### Utensil ###

class UtensilSerializer(serializers.ModelSerializer):
    class Meta:
        model = Utensil
        fields = "__all__"


class RecipeUtensilSerializer(serializers.ModelSerializer):
    utensil = UtensilSerializer()

    class Meta:
        model = RecipeUtensil
        exclude = ["recipe", "id"]


### Tag ###

class TagMergeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TagMerge
        fields = "__all__"


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = "__all__"


class TagGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = TagGroup
        fields = "__all__"


class TagGroupFullSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)

    class Meta:
        model = TagGroup
        exclude = []

    def get_tags(self, instance):
        tag_group_tags = Tag.objects.filter(tagGroup=instance)
        tag_serializer = TagSerializer(tag_group_tags, many=True)
        return tag_serializer.data

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['tags'] = self.get_tags(instance)
        return representation


class RecipeTagSerializer(serializers.ModelSerializer):
    tag = TagSerializer()

    class Meta:
        model = RecipeTag
        exclude = []


### Nutrients ###

class NutrientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Nutrients
        exclude = ["id"]


### WorkSteps ###

class WorkStepSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkSteps
        exclude = []


### Recipe ###

class RecipeBaseSerializer(serializers.ModelSerializer):
    ingredient_count = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        exclude = []
        fields = '__all__'

    similarity = serializers.SerializerMethodField()
    relevancy = serializers.SerializerMethodField()

    def get_similarity(self, obj):
        search = self.context.get('request').query_params.get('srch')
        if search:
            similarity = obj.similarity or obj.calculate_similarity(search)
            return similarity
        return None
    def get_relevancy(self, obj):
        search = self.context.get('request').query_params.get('srch')
        if search:
            relevancy = obj.relevancy or obj.calculate_similarity(search)
            return relevancy
        return None
    def get_ingredient_count(self, instance):
        ingredient_count = len(RecipeIngredient.objects.filter(recipe=instance))
        return ingredient_count


class RecipeFullSerializer(serializers.ModelSerializer):
    ingredients = RecipeIngredientSerializer(many=True, read_only=True)
    utensils = RecipeUtensilSerializer(many=True, read_only=True)

    class Meta:
        model = Recipe
        exclude = []

    def get_ingredients(self, instance):
        recipe_ingredients = RecipeIngredient.objects.filter(recipe=instance)
        ingredient_serializer = RecipeIngredientSerializer(recipe_ingredients, many=True)
        return ingredient_serializer.data

    def get_utensils(self, instance):
        recipe_utensils = RecipeUtensil.objects.filter(recipe=instance)
        utensil_serializer = RecipeUtensilSerializer(recipe_utensils, many=True)
        return utensil_serializer.data

    def get_nutrients(self, instance):
        recipe_nutrients = Nutrients.objects.filter(recipe=instance).first()
        utensil_serializer = NutrientSerializer(recipe_nutrients, many=False)
        return utensil_serializer.data

    def get_tag(self, instance):
        recipe_tag = RecipeTag.objects.filter(recipe=instance)
        tag_serializer = RecipeTagSerializer(recipe_tag, many=True)
        return tag_serializer.data

    def get_work_steps(self, instance):
        recipe_work_steps = WorkSteps.objects.filter(relatedRecipe=instance)
        tag_serializer = WorkStepSerializer(recipe_work_steps, many=True)
        return tag_serializer.data

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['ingredients'] = self.get_ingredients(instance)
        representation['utensils'] = self.get_utensils(instance)
        representation['nutrients'] = self.get_nutrients(instance)
        representation['cuisines'] = self.get_cuisine(instance)
        representation['tags'] = self.get_tag(instance)
        representation['work_steps'] = self.get_work_steps(instance)
        return representation
