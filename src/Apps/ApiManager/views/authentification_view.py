from Apps.MealManager.models import InviteToken
from Apps.MealManager.serializers import InviteTokenSerializer
from rest_framework import generics
from rest_framework import status
from rest_framework.decorators import permission_classes, api_view
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView


class ObtainTokenPairView(TokenObtainPairView):
    serializer_class = TokenObtainPairSerializer


@api_view(['POST'])
def api_login(request):
    serializer = TokenObtainPairSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    return Response(serializer.validated_data, status=status.HTTP_200_OK)


@permission_classes([IsAuthenticated, IsAdminUser])
class InviteListCreate(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return InviteTokenSerializer
        return InviteTokenSerializer

    def get_queryset(self):
        inviteTokens = InviteToken.objects.all()
        return inviteTokens

    def create(self, request, *args, **kwargs):
        request.data['issuer'] = request.user.pk
        return super().create(request, *args, **kwargs)


@permission_classes([IsAuthenticated, IsAdminUser])
class InviteDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = InviteTokenSerializer
    lookup_field = 'id'

    def get_queryset(self):
        return InviteToken.objects.all()
