from rest_framework.decorators import api_view # importando um decoreto - para decorar minha api views
from rest_framework.response import Response # importando uma resposta do django rest framework
from ..models import Recipe
from ..serializers import RecipeSerializer
from django.shortcuts import get_object_or_404
from tag.models import Tag
from ..serializers import TagSerializers
from rest_framework import status # importando status code HTTP no  DRF
from rest_framework.views import APIView # importando minha CLASS BASED VIEWS
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView # importando CLASS BASED VIEW GENERICS
from rest_framework.pagination import PageNumberPagination
from rest_framework.viewsets import ModelViewSet # criando viewset 


class RecipeAPIv2Pagination(PageNumberPagination):
    page_size = 2


class RecipeApiv2ViewSet(ModelViewSet):
    queryset = Recipe.objects.get_published()
    serializer_class = RecipeSerializer
    pagination_class = RecipeAPIv2Pagination


    def partial_update(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        recipe = self.get_queryset().filter(pk=pk).first()

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
