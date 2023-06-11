# Generated by Django 4.2.1 on 2023-06-09 09:19

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('MealManager', '0036_alter_recipe_recipetype'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipe',
            name='favoriteBy',
            field=models.ManyToManyField(related_name='favorite_recipes', to=settings.AUTH_USER_MODEL),
        ),
    ]