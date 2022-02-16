from django.db import models
from django.contrib.auth.models import User
from ckeditor_uploader.fields import RichTextUploadingField

from django.core.validators import RegexValidator
from django.template.defaultfilters import slugify
from django.utils import timezone

# Create your models here.

class Student_Model(models.Model):
    user            = models.OneToOneField(User,primary_key=True,on_delete=models.CASCADE)
    name            = models.CharField(max_length=20)
    computer_code   = models.CharField(blank=True, max_length =13)
    slug            = models.SlugField(blank=True, max_length=200)
    image           = models.ImageField(upload_to="profile_pics/", null=True, default="profile_pics/user_logo.png",height_field='height_field',width_field='width_field')
    height_field    = models.IntegerField(default=0, null=True)
    width_field     = models.IntegerField(default=0, null=True)
    enrollment_no   = models.CharField(blank=True, max_length=100)
    course          = models.CharField(blank=True, max_length=20)
    created         = models.DateTimeField(default=timezone.now)
    modified        = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return str(self.user) + "; " + str(self.name) + "; " + str(self.course) + "; " + str(self.computer_code)


##########################################################

class UserTimeStamp(models.Model):
	created_at = models.DateTimeField(auto_now_add = True)
	updated_at = models.DateTimeField(auto_now = True)
	user = models.ForeignKey(User,on_delete = models.CASCADE)

	class Meta:
		abstract = True

class Subject(models.Model):
    topic = models.CharField(max_length = 100)
    image = models.ImageField(upload_to='images/')
    description = models.CharField(max_length = 100,null=True)
    user = models.CharField(max_length = 100)

    def __str__(self):
        return self.topic

class Material(models.Model):
    material_name = models.CharField(max_length=50)
    topic = models.ForeignKey(to=Subject, on_delete=models.CASCADE, null=True, blank=True)
    #material_video = models.FileField(upload_to='images)
    material_video = models.CharField(max_length=100,null=True)
    content = RichTextUploadingField(null=True)
    material_desc = models.TextField()
    material_code = models.TextField()
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    likes = models.IntegerField(default = 0)
    def __str__(self):
        return self.material_name

class Comment(UserTimeStamp):
    post = models.ForeignKey(Material,on_delete = models.CASCADE)
    comment = models.TextField()

class Reply(UserTimeStamp):
    comment = models.ForeignKey(Comment,on_delete = models.CASCADE)
    reply = models.TextField()
