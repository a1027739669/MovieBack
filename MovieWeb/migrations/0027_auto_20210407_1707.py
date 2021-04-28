# Generated by Django 2.2.5 on 2021-04-07 09:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MovieWeb', '0026_auto_20210404_1330'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user',
            options={'managed': True, 'verbose_name': '用户', 'verbose_name_plural': '用户管理'},
        ),
        migrations.RenameField(
            model_name='chatrecord',
            old_name='msg',
            new_name='content',
        ),
        migrations.AlterField(
            model_name='user',
            name='local',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='用户所在地'),
        ),
        migrations.AlterField(
            model_name='user',
            name='selfnote',
            field=models.TextField(blank=True, null=True, verbose_name='个性签名'),
        ),
    ]
