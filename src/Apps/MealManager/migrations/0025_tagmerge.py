# Generated by Django 4.2.1 on 2023-05-29 21:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MealManager', '0024_remove_recipecuisine_cuisine_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='TagMerge',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('source', models.CharField(max_length=255, unique=True)),
                ('target', models.CharField(max_length=255, unique=True)),
            ],
        ),
    ]
