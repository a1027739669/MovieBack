# Generated by Django 2.2.5 on 2021-03-29 02:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('MovieWeb', '0006_comment_nickname'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='nickname',
        ),
    ]
