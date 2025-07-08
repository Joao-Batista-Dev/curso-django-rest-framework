from rest_framework import serializers
from recipes.models import Category
from django.contrib.auth.models import User 
from tag.models import Tag 
from .models import Recipe


class TagSerializers(serializers.ModelSerializer):
    # criamos uma meta class
    class Meta:
        model = Tag # precisamos informar o models
        fields = ['id', 'name', 'slug',] # precisamos informar o campos que queremos - podemos usar o __all__ - pegar todos os dados do nosso model, sem dizer o campo. Mais não é recomendavel pois pode vazar dados.


class RecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = ['id', 'title', 'description', 'public', 'author', 'category', 'tags', 'preparation', 'category_name', 'tag_objects', 'tag_links',]

    public = serializers.BooleanField(
        source='is_published',
        read_only=True, # informar que o campo e somente de leitura
    )
    preparation = serializers.SerializerMethodField(
        read_only=True,
    )
    category = serializers.PrimaryKeyRelatedField(
        read_only=True,
    )
    category_name = serializers.StringRelatedField(
        source='category',
        read_only=True,
    )
    tag_objects = TagSerializers(
        many=True,
        source='tags',
        read_only=True,
    )
    tag_links = serializers.HyperlinkedRelatedField(
        many=True,
        source='tags',
        view_name = 'recipes:recipes_api_v2_tag',
        read_only=True,  
    ) 


    def get_preparation(self, recipe):
        return f'{recipe.preparation_time}  {recipe.preparation_time_unit}'