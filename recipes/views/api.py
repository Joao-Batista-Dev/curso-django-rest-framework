from rest_framework.decorators import api_view # importando um decoreto - para decorar minha api views
from rest_framework.response import Response # importando uma resposta do django rest framework
from recipes.models import Recipe
from recipes.serializers import RecipeSerializer
from django.shortcuts import get_object_or_404
from tag.models import Tag
from recipes.serializers import TagSerializers
from rest_framework import status # importando status code HTTP no  DRF
from rest_framework.views import APIView # importando minha CLASS BASED VIEWS
from rest_framework.pagination import PageNumberPagination
from rest_framework.viewsets import ModelViewSet # criando viewset 
from rest_framework.permissions import IsAuthenticatedOrReadOnly # importando nossa autenticacao
from recipes.permissions import IsOwner # importando minha autenticacao modificada


class RecipeAPIv2Pagination(PageNumberPagination):
    page_size = 2


class RecipeApiv2ViewSet(ModelViewSet):
    queryset = Recipe.objects.get_published()
    serializer_class = RecipeSerializer
    pagination_class = RecipeAPIv2Pagination
    permission_classes = [IsAuthenticatedOrReadOnly,]
    http_method_names = ['get', 'options', 'head', 'post', 'delete']

    def get_object(self):
        pk = self.kwargs.get('pk', '')

        obj = get_object_or_404(
            self.get_queryset(),
            pk=pk,
        )

        self.check_object_permissions(self.request, obj)

    # usando minha permissao criada
    def get_permissions(self):
        if self.request.method in ['PATCH', 'DELETE']:
            return [IsOwner(), ]
        return super().get_permissions()

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    def create(self, request, *args, **kwargs): # POST
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(author=request.user)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, 
            status=status.HTTP_201_CREATED, 
            headers=headers
        )

    def partial_update(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        recipe = self.get_object()

        serializer = RecipeSerializer(
            instance=recipe, 
            data=request.data,
            many=False,
            context={
                'request': request,
            },
            partial=True
        )

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data,)


@api_view() 
def tag_api_detail(request, pk):
    tag = get_object_or_404(
        Tag.objects.all(),
        pk=pk
    )
    serializer = TagSerializers(
        instance=tag, 
        many=False,
        context={
            'request': request,
        },
    )

    return Response(serializer.data)
