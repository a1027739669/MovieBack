# Generated by Django 2.2.5 on 2021-04-10 08:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MovieWeb', '0033_remove_movie_tag'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='persons',
            field=models.ManyToManyField(blank=True, default=None, null=True, related_name='person_movie', to='MovieWeb.Person', verbose_name='演员'),
        ),
    ]
