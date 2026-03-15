from rest_framework import permissions, viewsets
from rest_framework.generics import CreateAPIView

from .models import User
from .serializers import RegisterSerializer, UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    """ViewSet для пользователя"""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class RegisterView(CreateAPIView):
    """Регистрация пользователя"""

    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]
