from audioop import reverse
from email.policy import default
from django.db import models
# from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from PIL import Image
from ckeditor.fields import RichTextField
# from django.contrib.auth.models import AbstractUser

User = get_user_model()
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
    id_user = models.IntegerField()
    bio = models.CharField(max_length=1000,blank=True)
    phone = models.IntegerField(null=True, blank=True)
    image = models.ImageField(default='profile_pic\default_pic.png', upload_to="profile_pic")

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
    name = models.CharField(max_length=1000,blank=True)
    body = RichTextField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    liked = models.ManyToManyField(User, related_name='answer_post', blank=True,)

    def __str__(self):
        return '%s - %s' % (self.question.name, self.user)

    def get_absolute_url(self):
        return reverse('question-detail', kwargs={'pk':self.pk})

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        
    def total_likes(self):
        return self.likes.all().count()

LIKE_CHOICES = (
    ('Like','Like'),
    ('Unlike','Unlike')
)

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    answer =  models.ForeignKey(Answer, on_delete=models.CASCADE)
    value = models.CharField(choices=LIKE_CHOICES, default='Like', max_length=10)

    def __str__(self):
        return str(self.answer)