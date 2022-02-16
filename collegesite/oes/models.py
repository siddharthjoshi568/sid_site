from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.

class Faculty(models.Model):
    username = models.CharField(primary_key=True, max_length=20, unique=True)
    name = models.CharField(max_length=20)
    email = models.EmailField()
    password = models.CharField(max_length=20)

    def __str__(self):
        return str(self.username)

class Course(models.Model):
    course_name = models.CharField(default = "", max_length=100)
    description = models.TextField(null="True", blank=True)
    faculty = models.CharField(default = "", max_length=100)
    status = models.IntegerField(default = 1)
    created = models.DateTimeField(default = timezone.now)
    modified = models.DateTimeField(default = timezone.now)
    def __str__(self):
        return str(self.id) + "; " + str(self.course_name) + "; " + str(self.description)


class Exam_detail(models.Model):
    exam_name = models.CharField(default = "", max_length = 100)
    description = models.TextField(null="True", blank=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    no_of_questions = models.IntegerField()
    attempts_allowed = models.IntegerField()
    pass_percentage = models.IntegerField()
    course_id = models.ForeignKey(Course, on_delete = models.CASCADE)
    semester = models.IntegerField(default = 0)
    year = models.IntegerField(default = 0)
    status = models.IntegerField(default = 0)
    created = models.DateTimeField(default = timezone.now)
    modified = models.DateTimeField(default = timezone.now)
    def __str__(self):
        return str(self.id) + "; " + str(self.exam_name) + "; " + str(self.description)

class Level(models.Model):
    level_name = models.CharField(default = "", max_length = 100)
    def __str__(self):
        return str(self.id) + "; " + str(self.level_name)

class Question_bank(models.Model):
    question = models.TextField(max_length=500)
    option1 = models.CharField(max_length=100)
    option2 = models.CharField(max_length=100)
    option3 = models.CharField(max_length=100)
    option4 = models.CharField(max_length=100)
    #choose = ((option1, option1), (option2, option2), (option3, option3), (option2, option4))
    #answer = models.CharField(max_length=100, choices=choose)
    answer = models.CharField(max_length=100)

    #level_id = models.ForeignKey(Level, on_delete = models.CASCADE)
    exam_id = models.ForeignKey(Exam_detail, on_delete =models.CASCADE)
    marks = models.FloatField()
    status = models.IntegerField(default = 0)
    created = models.DateTimeField(default = timezone.now)
    modified = models.DateTimeField(default = timezone.now)
    def __str__(self):
        return str(self.id) + "; " + str(self.question)


class Registration(models.Model):
    user_id = models.ForeignKey(User, on_delete = models.CASCADE)
    exam_id = models.ForeignKey(Exam_detail, on_delete = models.CASCADE)
    attempt_no = models.IntegerField()
    registered = models.IntegerField(default = 0)
    #view_answers  = models.IntegerField(default = 0)
    answered = models.IntegerField(default = 0)
    registered_time = models.DateTimeField(default = timezone.now)
    def __str__(self):
        return str(self.id) + "; " + str(self.user_id) + "; " + str(self.exam_id) + "; " + str(self.attempt_no)

class Result(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    reg_id = models.ForeignKey(Registration, on_delete = models.CASCADE)
    exam_id = models.ForeignKey(Exam_detail, on_delete=models.CASCADE)
    no_ques_attempt = models.IntegerField(default=0)
    no_ques_unattempt = models.IntegerField(default=0)
    no_ques_right = models.IntegerField(default=0)
    no_ques_wrong = models.IntegerField(default=0)
    total_marks = models.FloatField(default=0)
    created = models.DateTimeField(default=timezone.now)
    modified = models.DateTimeField(default=timezone.now)
    def __str__(self):
        return str(self.id) + "; " + str(self.reg_id) + "; " + str(self.exam_id)
