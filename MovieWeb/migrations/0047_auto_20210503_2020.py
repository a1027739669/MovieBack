# Generated by Django 2.2.5 on 2021-05-03 12:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MovieWeb', '0046_stayrating_type'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='stayrating',
            name='type',
        ),
        migrations.AddField(
            model_name='stayrating',
            name='favoriteid',
            field=models.BigIntegerField(default=0),
        ),
    ]