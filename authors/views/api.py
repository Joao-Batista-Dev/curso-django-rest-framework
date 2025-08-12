from rest_framework.viewsets import ReadOnlyModelViewSet
from ..serializers import AuthorSerializers
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action # action transformar meu metodo em uma url

class AuthorViewSet(ReadOnlyModelViewSet):
    serializer_class = AuthorSerializers
    permission_classes = [IsAuthenticated,]

    def get_queryset(self):
        User = get_user_model()
        qs = User.objects.filter(username=self.request.user.username)
        return qs

    @action(
            methods=['get',], # precisamos informar o metodo HTTP do nosso metodo
            detail=False, # se e um datail 
    )
    def me(self, request, *args, **kwargs):
        obj = self.get_queryset().first()
        serializer = self.get_serializer(
            instance=obj
        )
        return Response(serializer.data)