import django_filters
from Apps.MealManager.models import Ingredient
from Apps.MealManager.serializers import IngredientSerializer
from django.db.models import F
from django_filters import rest_framework as filters
from rest_framework import generics
from rest_framework.decorators import permission_classes, api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from util.pagination import RqlPagination


class IngredientFilterSet(filters.FilterSet):
    srch = django_filters.CharFilter(method='filter_search')
    relevancy = django_filters.CharFilter(method='filter_relevancy')
    ordering = django_filters.OrderingFilter(fields=['name'])

    def filter_search(self, queryset, name, value):
        return queryset.filter(name__icontains=value)

    def filter_relevancy(self, queryset, name, value):
        return queryset.annotate(
            relevancy=F('rating') * F('ratingCount')
        ).order_by('-relevancy')

    class Meta:
        model = Ingredient
        fields = ['srch', 'relevancy']


@permission_classes([IsAuthenticated])
class IngredientList(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    pagination_class = RqlPagination
    filterset_class = IngredientFilterSet

    def get_serializer_class(self):
        if self.request.method == 'GET':
            fields = self.request.query_params.get('fields')
            if fields:
                fields = fields.split(',')
                meta = IngredientSerializer.Meta
                meta.exclude = None
                meta.fields = fields
                return type('DynamicRecipeBaseSerializer', (IngredientSerializer,), {'Meta': meta})
            else:
                return IngredientSerializer
        return IngredientSerializer

    def get_queryset(self):
        recipes = Ingredient.objects.filter(parent=None)
        return recipes


@api_view(['POST'])
def assign_ingredient_parent(request, helloFreshId, parentId=None):
    try:
        source = Ingredient.objects.get(helloFreshId=helloFreshId)
    except Ingredient.DoesNotExist:
        return Response({'error': 'Recipe not found'}, status=404)
    try:
        parent = Ingredient.objects.get(helloFreshId=parentId)
    except:
        parent = None
    if parent is not None and parent.parent is not None:
        return Response({'error': 'Can not assign a parent which is already a child'}, status=400)

    source.parent = parent
    source.save()
    response = {
        'message': 'Ingredient assigned successfully',
        'helloFreshId': helloFreshId,
    }

    return Response(response)
