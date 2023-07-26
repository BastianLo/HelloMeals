from Apps.MealManager.models import InviteToken
from Apps.MealManager.serializers import InviteTokenSerializer
from django.contrib.auth.models import User
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics
from rest_framework import serializers
from rest_framework import status
from rest_framework.decorators import permission_classes, api_view
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


class ObtainTokenPairView(TokenObtainPairView):
    serializer_class = TokenObtainPairSerializer


class RefreshTokenView(TokenRefreshView):
    serializer_class = TokenRefreshSerializer


@api_view(['GET'])
def current_user(request):
    user = request.user
    return Response({
        'username': user.username,
        'email': user.email,
        'firstName': user.first_name,
        'lastName': user.last_name,
        'permissions': [perm.pk for perm in user.user_permissions.all()],
    })


class RegisterSerializer(serializers.Serializer):
    token = serializers.CharField(required=True)
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)


class RegisterView(APIView):
    @swagger_auto_schema(
        request_body=RegisterSerializer,
    )
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        token = serializer.validated_data['token']
        username = serializer.validated_data['username']
        password = serializer.validated_data['password']

        try:
            invite_token = InviteToken.objects.get(id=token)
            User.objects.create_user(username=username, email=None, password=password)
        except InviteToken.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        invite_token.delete()
        return Response(status=status.HTTP_200_OK)


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
