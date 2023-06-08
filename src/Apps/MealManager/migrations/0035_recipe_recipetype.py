# Generated by Django 4.2.1 on 2023-06-08 05:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MealManager', '0034_recipe_healthscore'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipe',
            name='recipeType',
            field=models.IntegerField(choices=[(0, 'Hauptgericht'), (1, 'Frühstück')], default=0),
        ),
    ]
