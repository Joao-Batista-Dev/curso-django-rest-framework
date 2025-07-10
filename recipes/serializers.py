from rest_framework import serializers
from recipes.models import Category
from django.contrib.auth.models import User 
from tag.models import Tag 
from .models import Recipe
from collections import defaultdict
from attr import attr
from authors.validators import AuthorRecipeValidator


class TagSerializers(serializers.ModelSerializer):
    # criamos uma meta class
    class Meta:
        model = Tag # precisamos informar o models
        fields = ['id', 'name', 'slug',] # precisamos informar o campos que queremos - podemos usar o __all__ - pegar todos os dados do nosso model, sem dizer o campo. Mais não é recomendavel pois pode vazar dados.


class RecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = [
            'id', 'title', 'description', 'public', 'author', 'category', 'tags',
            'preparation', 'category_name', 'tag_objects', 'tag_links', 'preparation_time', 
            'preparation_time_unit', 'servings', 'servings_unit', 
            'preparation_steps', 'cover',
        ]

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
    

    # metodo validate para validar dados
    def validate(self, attrs):
        if self.instance is not None and attrs.get('servings') is None:
            attrs['servings'] = self.instance.servings

        if self.instance is not None and attrs.get('preparations_time') is None:
            attrs['preparations_time'] = self.instance.preparations_time

        super_validate = super().validate(attrs)

        AuthorRecipeValidator(data=attrs, ErrorClass=serializers.ValidationError,)

        return super_validate
    

    def save(self, **kwargs):
        return super().save(**kwargs)
    

    def create(self, validated_data):
        return super().create(validated_data)
    

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)
    