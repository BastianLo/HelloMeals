import graphene
from graphene import relay
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from django.db.models import Q
from Apps.MealManager.models import Recipe
from django.contrib.postgres.search import TrigramSimilarity
from django_filters import FilterSet, CharFilter

class RecipeNode(DjangoObjectType):
    similarity = graphene.Float()  # Add the similarity field

    class Meta:
        model = Recipe
        filter_fields = {
            'name': ['exact', 'icontains'],
            'description': ['exact', 'icontains'],
            'difficulty': ['exact'],
        }
        interfaces = (relay.Node, )

    def resolve_similarity(self, info):
        return self.similarity  # Return the similarity score

class BookQuery(graphene.ObjectType):
    recipe = relay.Node.Field(RecipeNode)
    all_recipes = DjangoFilterConnectionField(
        RecipeNode,
        filterset_class=FilterSet,
        search=graphene.String(description='Full-text search on name and description fields')
    )

    def resolve_all_recipes(self, info, search=None, **kwargs):
        queryset = Recipe.objects.all()

        if search:
            queryset = queryset.annotate(
                similarity=TrigramSimilarity('name', search) * 5 + TrigramSimilarity('description', search)
            ).filter(similarity__gt=0.005).order_by('-similarity')

        return queryset

schema = graphene.Schema(query=BookQuery)
