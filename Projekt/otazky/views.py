'''from django.shortcuts import render
from django.http import HttpResponse
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.template import loader
from rest_framework import viewsets, status
from rest_framework.views import APIView
from sqlparse.filters import output
from rest_framework import generics

from .models import *
from .serializers import *
from rest_framework.response import Response


class OtazkaView(generics.ListAPIView):
    def get(self, request):
        outputt = [{"id": output.id, "name": output.name, "text": output.text, "approved": output.approved,
                    "visible": output.visible, "created_by": output.created_by.username, "likes": output.likes,
                    "created_at": output.created_at, "okruh": output.okruh.name} for output in Question.objects.all()]
        return Response(outputt)

    def post(self, request):
        serializer = QuestionSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
    queryset=Question.objects.all()
    serializer_class = QuestionSerializer
'''
import json
from django.http import HttpResponse
from django.shortcuts import render
from rest_framework import generics

from .models import *
from .serializers import *
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import AccessToken,RefreshToken
from django.core.serializers.json import DjangoJSONEncoder
from rest_framework import status
class OtazkaView(generics.ListCreateAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

class CommentView(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

class CommentsForQuestionView(generics.ListCreateAPIView):
    Model = Comment
    serializer_class = CommentSerializer

    def get_queryset(self):
        queryset= Comment.objects.all()
        questionID = self.request.query_params.get('questionID')
        if questionID:
            queryset = queryset.filter(question=questionID)
        return queryset
    
class CourseView(generics.ListCreateAPIView):
    Model = Course
    serializer_class = CourseSerializer

    def get_queryset(self):
        queryset= Course.objects.all()
        return queryset

class ScoreView(generics.ListCreateAPIView):
    Model = Score
    serializer_class = ScoreSerializer

    def get_queryset(self):
        courseID = self.request.query_params.get('courseID')
        queryset = Score.objects.filter(course = courseID)
        queryset = queryset.order_by('-points')
        return queryset
    
class AnswersForQuestion(generics.ListCreateAPIView):
    Model = Answer
    serializer_class = AnswerSerializer

    def get_queryset(self):
        queryset= Answer.objects.all()
        questionID = self.request.query_params.get('questionID')
        if questionID:
            queryset = queryset.filter(question=questionID)
        return queryset

class OkruhsForCourse(generics.ListCreateAPIView):
    Model = Okruh
    serializer_class = OkruhSerializer

    def get_queryset(self):
        queryset= Okruh.objects.all()
        courseID = self.request.query_params.get('courseID')
        if courseID:
            queryset = queryset.filter(course=courseID)
        return queryset

class OkruhByID(generics.ListCreateAPIView):
    Model = Okruh
    serializer_class = OkruhSerializer

    def get_queryset(self):
        queryset= Okruh.objects.all()
        okruhID = self.request.query_params.get('okruhID')
        if okruhID:
            queryset = queryset.filter(id=okruhID)
        return queryset

class QuestionByID(generics.ListCreateAPIView):
    Model = Question
    serializer_class = QuestionSerializer

    def get_queryset(self):
        queryset= Question.objects.all()
        question_id = self.request.query_params.get('questionID')
        if question_id:
            queryset = queryset.filter(id=question_id)
        return queryset

class QuestionForOkruh(generics.ListCreateAPIView):
    Model = Question
    serializer_class = QuestionSerializer

    def get_queryset(self):
        queryset= Question.objects.all()
        okruhID = self.request.query_params.get('okruhID')
        if okruhID:
            queryset = queryset.filter(okruh=okruhID)
        return queryset

class CallangeQuestions(generics.ListCreateAPIView):
    Model = Question
    serializer_class = QuestionSerializer

    def get_queryset(self):
        print(self.request.query_params.get('courseID'))
        challange_questions= ChalangeQuestion.objects.filter(courseID=self.request.query_params.get('courseID'))
        queryset= None
        for chalange_question in challange_questions:
            print(chalange_question.id)
            if queryset is None :
                queryset = Question.objects.filter(id = chalange_question.question.id)
                print(queryset.values_list())
            else:
                queryset = queryset | Question.objects.filter(id = chalange_question.question.id)
        return queryset
    
class Username(APIView):
    def post(self,request, format=None):
        
        try:
            access_token_obj = AccessToken(request.data["access_token"])
        except:
            return HttpResponse('Unauthorized', status=401)
        user_id=access_token_obj['user_id']
        
        user = User.objects.get(id=user_id)
        print(user)
        return Response(str(user))

class UsernameID(APIView):
    def post(self,request, format=None):
        
        try:
            access_token_obj = AccessToken(request.data["access_token"])
        except:
            return HttpResponse('Unauthorized', status=401)
        user_id=access_token_obj['user_id']
        return Response(str(user_id))

class NewQuestion(APIView):
    def post(self,request, format=None):
        user = User.objects.filter(id=request.data["created_by"])
        okruh = Okruh.objects.filter(id=request.data["okruh"])
        newQuestion=Question.objects.create(name=request.data["name"],text=request.data["text"],approved=request.data["approved"],visible=request.data["visible"],created_by=user[0],is_text_question=request.data["is_text_question"],likes=0,okruh=okruh[0])
        print(newQuestion.id)
        return Response(newQuestion.id)

class NewComment(APIView):
    def post(self,request, format=None):
        user = User.objects.filter(id=request.data["user_id"])
        text = request.data["text"]
        question = Question.objects.filter(id=request.data["question_id"])
        comment = Comment.objects.create(text=text,created_by=user[0],question=question[0])
        return HttpResponse(200)

class ScoreEntry(APIView):
    def post(self,request, format=None):
        user = User.objects.filter(id=request.data["user_id"])
        course = Course.objects.filter(id=request.data["courseID"])
        points =request.data["point"]
        querry = Score.objects.filter(course=request.data["courseID"],user=request.data["user_id"])
        if not querry:
            score = Score.objects.create(user=user[0],course=course[0],points=points)
        else:
            for score in querry:
                score.points=points
                score.save()
        return Response(status=200)
class NewAnswers(APIView):
    def post(self,request, format=None):
        question=Question.objects.filter(id=request.data[0]["question"])#MOZNO BUG TODO
        for answer in request.data:
            new_answer = Answer.objects.create(text=answer["text"],answer_type=answer["answer_type"],question=question[0])
        return HttpResponse(200)

class UserForID(generics.ListCreateAPIView):
    model = User
    serializer_class = UserSerializer
    def get_queryset(self):
        user = User.objects.get(id=self.request.query_params.get('user_id'))
        return user

    
class UserForID(generics.ListCreateAPIView):
    Model = User
    serializer_class = UserSerializer

    def get_queryset(self):
        queryset= User.objects.all()
        userID = self.request.query_params.get('user_id')
        if userID:
            queryset = queryset.filter(id=userID)
        return queryset
 
class HomeView(APIView):
    permission_classes = (IsAuthenticated, )  
    def get(self, request):       
        content = {'message': 'Welcome to the JWT Authentication page using React Js and Django!'}   
        return Response(content)

class LogoutView(APIView):     
    permission_classes = (IsAuthenticated,)     
    def post(self, request):
          
        try:               
            refresh_token = request.data["refresh_token"]               
            token = RefreshToken(refresh_token)               
            token.blacklist()               
            return Response(status=status.HTTP_205_RESET_CONTENT)          
        except Exception as e:               
            return Response(status=status.HTTP_400_BAD_REQUEST)