# Generated by Django 2.2.5 on 2021-04-13 08:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MovieWeb', '0036_auto_20210411_1014'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='focusitems',
            field=models.TextField(blank=True, default=''),
        ),
    ]
