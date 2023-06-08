# Generated by Django 4.2.1 on 2023-06-08 09:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MealManager', '0035_recipe_recipetype'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='recipeType',
            field=models.IntegerField(choices=[(0, 'Hauptgericht'), (1, 'Frühstück'), (2, 'Dessert'), (3, 'Backen'), (4, 'Getränke')], default=0),
        ),
    ]
