# Generated by Django 2.2.5 on 2021-04-29 06:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MovieWeb', '0042_auto_20210428_1442'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='person',
            name='namezh',
        ),
        migrations.AlterField(
            model_name='person',
            name='nameen',
            field=models.TextField(blank=True, null=True, verbose_name='英文名'),
        ),
    ]