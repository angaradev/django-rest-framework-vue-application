from rest_framework import serializers
from .models import Language, Paradigm, Programmer

class LanguageSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Language
        fields = ('id', 'url', 'name', 'paradigm')


class ParadigmSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Paradigm
        fields = ('id', 'url', 'name')

class ProgrammerSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Programmer
        fields = ('id', 'url', 'name', 'languages')


class LanguageSerializerNested(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = ('id', 'name')


class NestedParadigmSerializer(serializers.ModelSerializer):
    lang = LanguageSerializerNested(many=True, read_only=True)

    class Meta:
        model = Paradigm
        fields = ['id', 'name', 'lang']

