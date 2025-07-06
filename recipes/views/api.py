from rest_framework.decorators import api_view # importando um decareto - para decorar minha api views
from rest_framework.response import Response # importando uma resposta do django rest framework

@api_view() # usando decorato do django rest framework
def recipe_api_list(request):
    return Response({
        'name': 'fulano De Tal'
    })
