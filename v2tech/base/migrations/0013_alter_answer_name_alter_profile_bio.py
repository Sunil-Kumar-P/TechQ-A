# Generated by Django 4.0.6 on 2022-08-10 17:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0012_rename_likes_answer_liked_like'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answer',
            name='name',
            field=models.CharField(blank=True, max_length=1000),
        ),
        migrations.AlterField(
            model_name='profile',
            name='bio',
            field=models.CharField(blank=True, max_length=1000),
        ),
    ]
