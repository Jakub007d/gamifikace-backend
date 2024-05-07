import uuid
from django.db import models
from django.contrib.auth.models import User


#V tomto súbore sa nachádza implementácia jednotlivých entít modelu.
class Course(models.Model):
    name = models.CharField(max_length=255, unique=True, default="")
    full_name = models.CharField(max_length=255, default="")
    visited_by = models.ManyToManyField(User)
    def __str__(self):
        return self.name

class Score(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False)
    points = models.IntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE,default="1")

class Okruh(models.Model):
    name = models.CharField(max_length=255, unique=True, default="")
    available = models.BooleanField(default=False)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    def __str__(self):
        return self.name


class Question(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False)
    name = models.CharField(max_length=255)
    text = models.TextField(default="")
    approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    visible = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    likes = models.IntegerField(default=0)
    reported = models.BooleanField(default=False)
    okruh = models.ForeignKey(Okruh, on_delete=models.CASCADE)
    is_text_question = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Answer(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False)
    answer_type = models.BooleanField(default=True)
    text = models.TextField(default="")
    question = models.ForeignKey(Question, on_delete=models.CASCADE)

    def __str__(self):
        return self.text


class Comment(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False)
    text = models.TextField(default="")
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    likes = models.IntegerField(default=0)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)

class ChalangeQuestion(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False)
    courseID = models.ForeignKey(Course, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)