from django.contrib import admin

from .models import Answer, Question, Topic, Profile,Like

admin.site.register([Profile])
admin.site.register(Question)
admin.site.register(Topic)
admin.site.register(Answer)
admin.site.register(Like)