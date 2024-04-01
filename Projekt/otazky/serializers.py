from rest_framework import serializers
from .models import *


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['id', 'name', 'text', 'approved', 'visible', 'created_by', 'likes', 'created_at', 'okruh','is_text_question']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'id')

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ('id','name')

class ScoreSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username')
    coursename = serializers.CharField(source='course.name')
    class Meta:
        model = Score
        fields = ('id','course','user','coursename','username','points')

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'text', 'created_at', 'created_by', 'likes', 'question']

class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ['id', 'answer_type', 'text', 'question']

class OkruhSerializer(serializers.ModelSerializer):
    class Meta:
        model = Okruh
        fields = ['id','name', 'available', 'course']

class ChallangeQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChalangeQuestion
        fields=['question']
