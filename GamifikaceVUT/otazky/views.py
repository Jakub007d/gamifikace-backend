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
#Vráti komentáre pre otázku
class CommentsForQuestionView(generics.ListCreateAPIView):
    Model = Comment
    serializer_class = CommentSerializer

    def get_queryset(self):
        queryset= Comment.objects.all()
        questionID = self.request.query_params.get('questionID')
        if questionID:
            queryset = queryset.filter(question=questionID)
        return queryset
#Vráti všetky kurzy   
class CourseView(generics.ListCreateAPIView):
    Model = Course
    serializer_class = CourseSerializer

    def get_queryset(self):
        queryset= Course.objects.all()
        return queryset

#Vráti rebríček zoradený zostupne podla bodov.
class ScoreView(generics.ListCreateAPIView):
    Model = Score
    serializer_class = ScoreSerializer

    def get_queryset(self):
        courseID = self.request.query_params.get('courseID')
        queryset = Score.objects.filter(course = courseID)
        queryset = queryset.order_by('-points')
        return queryset

#Vráti odpovede pre danú otázku
class AnswersForQuestion(generics.ListCreateAPIView):
    Model = Answer
    serializer_class = AnswerSerializer

    def get_queryset(self):
        queryset= Answer.objects.all()
        questionID = self.request.query_params.get('questionID')
        if questionID:
            queryset = queryset.filter(question=questionID)
        return queryset

#Vráti okruhy pre kurz
class OkruhsForCourse(generics.ListCreateAPIView):
    Model = Okruh
    serializer_class = OkruhSerializer

    def get_queryset(self):
        queryset= Okruh.objects.all()
        courseID = self.request.query_params.get('courseID')
        if courseID:
            queryset = queryset.filter(course=courseID)
        return queryset

#Nájde a vráti okruh so špecifikovaným id
class OkruhByID(generics.ListCreateAPIView):
    Model = Okruh
    serializer_class = OkruhSerializer

    def get_queryset(self):
        queryset= Okruh.objects.all()
        okruhID = self.request.query_params.get('okruhID')
        if okruhID:
            queryset = queryset.filter(id=okruhID)
        return queryset

#Slúži pre získanie otázky za pomoci jej id
class QuestionByID(generics.ListCreateAPIView):
    Model = Question
    serializer_class = QuestionSerializer

    def get_queryset(self):
        queryset= Question.objects.all()
        question_id = self.request.query_params.get('questionID')
        if question_id:
            queryset = queryset.filter(id=question_id)
        return queryset

#Slúži pre získanie otázok pre okruh
class QuestionForOkruh(generics.ListCreateAPIView):
    Model = Question
    serializer_class = QuestionSerializer

    def get_queryset(self):
        queryset= Question.objects.all()
        okruhID = self.request.query_params.get('okruhID')
        if okruhID:
            queryset = queryset.filter(okruh=okruhID)
        return queryset

#Vráti otázky z výzvy
class CallangeQuestions(generics.ListCreateAPIView):
    Model = Question
    serializer_class = QuestionSerializer

    def get_queryset(self):
        print(self.request.query_params.get('courseID'))
        challange_questions= ChalangeQuestion.objects.filter(courseID=self.request.query_params.get('courseID'))
        queryset= None
        for chalange_question in challange_questions:
            if queryset is None :
                queryset = Question.objects.filter(id = chalange_question.question.id)
                print(queryset.values_list())
            else:
                queryset = queryset | Question.objects.filter(id = chalange_question.question.id)
        return queryset
    
#Pre access_token získa meno užívatela
class Username(APIView):
    def post(self,request, format=None):
        
        try:
            access_token_obj = AccessToken(request.data["access_token"])
        except:
            return HttpResponse('Unauthorized', status=401)
        user_id=access_token_obj['user_id']
        
        user = User.objects.get(id=user_id)
        return Response(str(user))

#Pre access_token získa id užívatela
class UsernameID(APIView):
    def post(self,request, format=None):
        
        try:
            access_token_obj = AccessToken(request.data["access_token"])
        except:
            return HttpResponse('Unauthorized', status=401)
        user_id=access_token_obj['user_id']
        return Response(str(user_id))

#Pridanie otázky do databáze
class NewQuestion(APIView):
    def post(self,request, format=None):
        user = User.objects.filter(id=request.data["created_by"])
        okruh = Okruh.objects.filter(id=request.data["okruh"])
        newQuestion=Question.objects.create(name=request.data["name"],text=request.data["text"],approved=request.data["approved"],visible=request.data["visible"],created_by=user[0],is_text_question=request.data["is_text_question"],likes=0,okruh=okruh[0])
        return Response(newQuestion.id)

#Pridanie komentáru do databáze
class NewComment(APIView):
    def post(self,request, format=None):
        user = User.objects.filter(id=request.data["user_id"])
        text = request.data["text"]
        question = Question.objects.filter(id=request.data["question_id"])
        comment = Comment.objects.create(text=text,created_by=user[0],question=question[0])
        return HttpResponse(200)

#Pridanie nového skóre do databáze
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

#Pridanie novej odpovedi do databáze
class NewAnswers(APIView):
    def post(self,request, format=None):
        question=Question.objects.filter(id=request.data[0]["question"])
        for answer in request.data:
            new_answer = Answer.objects.create(text=answer["text"],answer_type=answer["answer_type"],question=question[0])
        return HttpResponse(200)

#Získa objekt užívateľa a následne ho v odpovedi vráti
class UserForID(generics.ListCreateAPIView):
    model = User
    serializer_class = UserSerializer
    def get_queryset(self):
        user = User.objects.get(id=self.request.query_params.get('user_id'))
        return user

#Získa objekt užívateľa a následne ho v odpovedi vráti
class UserForID(generics.ListCreateAPIView):
    Model = User
    serializer_class = UserSerializer

    def get_queryset(self):
        queryset= User.objects.all()
        userID = self.request.query_params.get('user_id')
        if userID:
            queryset = queryset.filter(id=userID)
        return queryset
 
#Domovská obrazovka
class HomeView(APIView):
    permission_classes = (IsAuthenticated, )  
    def get(self, request):       
        content = {'message': 'Stránka backendu aplikacie gamifikace.online'}   
        return Response(content)

#Odhlásenie užívateľa
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

#Pridá navštevovaný kurz k uživateľovi
class AddUserToCourse(APIView):
    def post(self,request, format=None):
        queryset= Course.objects.all()
        userID = request.data["userID"]
        courseID = request.data["courseID"]
        courses = queryset.filter(id=courseID)
        found = False
        for course in courses:
            if courseID == str(course.id):
                visited_by = course.visited_by
                for user in visited_by.all():
                    if userID == str(user.id):
                        found = True
                if found != True:
                    querry_user = User.objects.all()
                    visited_by.add(querry_user.filter(id=userID)[0])
            found = False
        return Response(status=200)
    
#Odstránuje kurz z navštevovaných kurzov
class RemoveUserFomCourse(APIView):
    def post(self,request, format=None):
        queryset= Course.objects.all()
        userID = request.data["userID"]
        courseID = request.data["courseID"]
        courses = queryset.filter(id=courseID)
        found = False
        for course in courses:
            if courseID == str(course.id):
                visited_by = course.visited_by
                for user in visited_by.all():
                    if userID == str(user.id):
                        found = True
                if found == True:
                    querry_user = User.objects.all()
                    visited_by.remove(querry_user.filter(id=userID)[0])
            found = False
            
        return Response(200)

#Vracia kurzy navštevované uživateľom.
class CoursesForUSer(generics.ListCreateAPIView):
    Model = Course
    serializer_class = CourseSerializer

    def get_queryset(self):
        queryset= Course.objects.all()
        queryset2 = []
        userID = self.request.query_params.get('user_id')
        print(userID)
        found = False
        for course in queryset:
            visited_by = course.visited_by
            for user in visited_by.all():
                if userID == str(user.id):
                    print(userID)
                    found = True
            if found:
                queryset2.append(course)
            found = False
        return queryset2