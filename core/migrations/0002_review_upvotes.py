# Generated by Django 5.2 on 2025-06-07 18:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='upvotes',
            field=models.IntegerField(default=0),
        ),
    ]
