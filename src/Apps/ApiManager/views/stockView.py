from Apps.MealManager.models import Stock, Profile
from Apps.MealManager.serializers import StockSerializer
from rest_framework import generics
from rest_framework.decorators import permission_classes, api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


@permission_classes([IsAuthenticated])
class StockListCreate(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return StockSerializer
        return StockSerializer

    def get_queryset(self):
        tag_merges = Stock.objects.all()
        return tag_merges


@api_view(['POST'])
def change_membership(request, id):
    old_stock = request.user.profile.stock
    new_stock = Stock.objects.get(id=id)
    if old_stock == new_stock:
        return Response({"successful": False})
    if request.method == 'POST':
        if old_stock is not None:
            request.user.profile.stock = None
            request.user.profile.save()
            if len(Profile.objects.filter(stock=old_stock)) == 0:
                old_stock.delete()
            pass
        request.user.profile.stock = new_stock
        request.user.profile.save()

    response = {
        "successful": True
    }
    return Response(response)


@api_view(['DELETE', 'GET'])
def remove_membership(request):
    response = None
    old_stock = request.user.profile.stock
    if request.method == 'DELETE':
        if old_stock is not None:
            request.user.profile.stock = None
            request.user.profile.save()
            if len(Profile.objects.filter(stock=old_stock)) == 0:
                old_stock.delete()
        response = {
            "successful": True
        }
    elif request.method == 'GET':
        response = {
            "stockId": old_stock.id if old_stock else None,
            "members": [profile.user.username for profile in Profile.objects.filter(stock=old_stock).all()]
        }
    return Response(response)
