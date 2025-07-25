from rest_framework.viewsets import ReadOnlyModelViewSet
from ..serializers import AuthorSerializers
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated


class AuthorViewSet(ReadOnlyModelViewSet):
    serializer_class = AuthorSerializers
    permission_classes = [IsAuthenticated,]

    def get_queryset(self):
        User = get_user_model()
        qs = User.objects.filter(username=self.request.user.username)
        return qs
