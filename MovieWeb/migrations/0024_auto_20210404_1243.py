# Generated by Django 2.2.5 on 2021-04-04 04:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('MovieWeb', '0023_chatrecord_commenttime'),
    ]

    operations = [
        migrations.RenameField(
            model_name='chatrecord',
            old_name='userid',
            new_name='uid',
        ),
    ]
