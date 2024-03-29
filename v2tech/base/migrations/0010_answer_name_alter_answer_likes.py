# Generated by Django 4.0.6 on 2022-08-08 11:39

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('base', '0009_answer_likes_alter_answer_body_alter_profile_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='answer',
            name='name',
            field=models.CharField(max_length=1000, null=True),
        ),
        migrations.AlterField(
            model_name='answer',
            name='likes',
            field=models.ManyToManyField(null=True, related_name='answer_post', to=settings.AUTH_USER_MODEL),
        ),
    ]
