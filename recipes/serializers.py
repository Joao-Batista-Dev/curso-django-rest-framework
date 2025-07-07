from rest_framework import serializers # importando o serializers
from recipes.models import Category # importando meu models Category de recipes
from django.contrib.auth.models import User # importando models User do Django
from tag.models import Tag # importando meu models de Tag da minhas tags


class TagSerializers(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField(max_length=165)
    slug = serializers.SlugField() 


class RecipeSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField(max_length=65)
    description = serializers.CharField(max_length=165)
    public = serializers.BooleanField(source='is_published')
    preparation = serializers.SerializerMethodField()
    category = serializers.PrimaryKeyRelatedField(
        queryset = Category.objects.all(),
    ) # pegar uma Forenkey do nosso models, retorna o id = precisamos informar a queryset
    category_name = serializers.StringRelatedField(
        source='category',
    ) # pegar uma Forenkey do nosso models ,retorna a string = precisamos informar a source
    author = serializers.PrimaryKeyRelatedField(
        queryset= User.objects.all(),
    )
    tags = serializers.PrimaryKeyRelatedField(
        queryset= Tag.objects.all(),
        many=True,
    )
    tag_objects = TagSerializers(
        many=True,
        source='tags',
    ) # tranformar os dados da nossa tags em objetos = Já que tem varios dados


    def get_preparation(self, recipe):
        return f'{recipe.preparation_time}  {recipe.preparation_time_unit}'