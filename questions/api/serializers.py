from rest_framework import serializers
from questions.models import TestAnswer, Question


class AnswerSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)
    created_at = serializers.SerializerMethodField()
    likes_count = serializers.SerializerMethodField()
    user_has_voited = serializers.SerializerMethodField()
    question_slug = serializers.SerializerMethodField()

    class Meta:
        model = TestAnswer
        exclude = [
                'question',
                'voters',
                'updated_at'
                ]

    def get_created_at(self, instance):
        return instance.created_at.strftime('%Y-%m-%d')

    def get_likes_count(self, instance):
        return instance.voters.count()

    def get_user_has_voited(self, instance):
        request = self.context.get('request')
        return instance.voters.filter(pk=request.user.pk).exists()

    def get_question_slug(self, instance):
        return instance.question.slug


class QuestionSerializer(serializers.ModelSerializer):
    
    author = serializers.StringRelatedField(read_only=True)
    created_at = serializers.SerializerMethodField()
    slug = serializers.SlugField(read_only=True)
    answers_count = serializers.SerializerMethodField()
    user_has_answered = serializers.SerializerMethodField()

    class Meta:
        model = Question
        exclude = ['updated_at']
        
    def get_created_at(self, instance):
        return instance.created_at.strftime('%Y-%m-%d')

    def get_answers_count(self, instance):
        return instance.test_answers.count()

    def get_user_has_answered(self, instance):
        request = self.context.get('request')
        return instance.test_answers.filter(author=request.user.pk).exists()












