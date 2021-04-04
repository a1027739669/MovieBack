# Generated by Django 2.2.5 on 2021-04-03 03:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MovieWeb', '0017_delete_chatrecord'),
    ]

    operations = [
        migrations.CreateModel(
            name='ChatRecord',
            fields=[
                ('chatid', models.BigIntegerField(primary_key=True, serialize=False)),
                ('username', models.CharField(blank=True, max_length=255, null=True, verbose_name='用户名')),
                ('nickname', models.CharField(blank=True, max_length=255, null=True, verbose_name='用户昵称')),
                ('content', models.TextField(blank=True, null=True)),
            ],
            options={
                'db_table': 'chatrecord',
                'managed': True,
            },
        ),
    ]
