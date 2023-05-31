import graphene
from Apps.MealManager.models import Recipe, RecipeIngredient, Ingredient
from django.contrib.postgres.search import TrigramSimilarity
from graphene import relay
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField

from .filters import RecipeFilterSet


class IngredientNode(DjangoObjectType):
    class Meta:
        model = Ingredient
        fields = "__all__"
        interfaces = (relay.Node,)


class RecipeIngredientNode(DjangoObjectType):
    class Meta:
        model = RecipeIngredient
        fields = "__all__"
        interfaces = (relay.Node,)


class RecipeNode(DjangoObjectType):
    similarity = graphene.Float()  # Add the similarity field
    ingredients = graphene.List(RecipeIngredientNode)

    class Meta:
        model = Recipe
        filter_fields = {
            'difficulty': ['exact'],
        }
        interfaces = (relay.Node,)

    def resolve_similarity(self, info):
        return self.similarity

    def resolve_ingredients(self, info):
        return self.recipeingredient_set.all()

    def resolve_id(self, info):
        return self.helloFreshId


class RecipeQuery(graphene.ObjectType):
    recipe = graphene.Field(RecipeNode, id=graphene.ID(required=True))
    all_recipes = DjangoFilterConnectionField(
        RecipeNode,
        filterset_class=RecipeFilterSet,
        search=graphene.String(description='Full-text search on name and description fields')
    )

    def resolve_recipe(self, info, id):
        try:
            # Retrieve the recipe by its helloFreshId
            recipe = Recipe.objects.get(helloFreshId=id)
            return recipe
        except Recipe.DoesNotExist:
            return None

    def resolve_all_recipes(self, info, search=None, **kwargs):
        queryset = Recipe.objects.all()

        if search:
            queryset = queryset.annotate(
                similarity=TrigramSimilarity('name', search) * 5 + TrigramSimilarity('description', search)
            ).filter(similarity__gt=0.005).order_by('-similarity')

        return queryset


schema = graphene.Schema(query=RecipeQuery)
