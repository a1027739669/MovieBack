# Generated by Django 2.2.5 on 2021-03-31 12:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('MovieWeb', '0009_movie_all_score'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='rating',
        ),
        migrations.RemoveField(
            model_name='comment',
            name='vote',
        ),
    ]