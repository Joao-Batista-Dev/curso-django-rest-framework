from rest_framework.decorators import api_view # importando um decoreto - para decorar minha api views
from rest_framework.response import Response # importando uma resposta do django rest framework
from ..models import Recipe
from ..serializers import RecipeSerializer
from django.shortcuts import get_object_or_404




@api_view() 
def recipe_api_list(request):
    recipes = Recipe.objects.get_published()[:10]
    serializer = RecipeSerializer(instance=recipes, many=True)

    return Response(serializer.data)


@api_view() 
def recipe_api_detail(request, pk):
    recipe = get_object_or_404(
        Recipe.objects.get_published(),
        pk=pk
    )
    serializer = RecipeSerializer(instance=recipe, many=False)

    return Response(serializer.data)
