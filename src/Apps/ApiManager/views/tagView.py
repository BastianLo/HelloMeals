from django_filters import rest_framework as filters
from rest_framework import generics
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated

from Apps.MealManager.serializers import TagMergeSerializer, TagSerializer
from Apps.MealManager.models import TagMerge

from util.pagination import RqlPagination


### Views ###

@permission_classes([IsAuthenticated])
class TagMergeListCreate(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    pagination_class = RqlPagination

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return TagMergeSerializer
        return TagMergeSerializer

    def get_queryset(self):
        recipes = TagMerge.objects.all()
        return recipes

