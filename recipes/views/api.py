from rest_framework.decorators import api_view # importando um decoreto - para decorar minha api views
from rest_framework.response import Response # importando uma resposta do django rest framework

@api_view() 
def recipe_api_list(request):
    return Response({
        'name': 'fulano De Tal'
    })
