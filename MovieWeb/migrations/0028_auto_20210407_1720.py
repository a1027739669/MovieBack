# Generated by Django 2.2.5 on 2021-04-07 09:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('MovieWeb', '0027_auto_20210407_1707'),
    ]

    operations = [
        migrations.RenameField(
            model_name='chatrecord',
            old_name='chattime',
            new_name='date',
        ),
    ]