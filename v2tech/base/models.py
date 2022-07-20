from email.policy import default
from django.db import models
from django.contrib.auth.models import User
from PIL import Image
# from django.contrib.auth.models import AbstractUser


# #user module pls dont touch this part
# class User(AbstractUser):
#     username = models.CharField(unique=True, max_length=200, null=True)
#     name = models.CharField(max_length=200, null=True)
#     email = models.EmailField(unique=True,null=True)
#     bio = models.TextField(null=True)
#     avatar = models.ImageField(null=True,default="")


#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = []


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.CharField(max_length=1000)
    phone = models.IntegerField(null=True, blank=True)
    image = models.ImageField(default='default.jpg', upload_to="profile_pic")

    def __str__(self):
        return f'{self.user.username} - Profile'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.image.path)
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)


#Topics Module
class Topic(models.Model):
    name = models.CharField(max_length=200)

    def __str__ (self):
        return self.name


#Questions Module
class Question(models.Model):
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200)
    description = models.TextField(null = True, blank=True)
    participants = models.ManyToManyField(User, related_name='participants', blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated', 'created']

    def __str__(self):
        return self.name

#Answers Module
class Answer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    body = models.TextField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.body[0:50]