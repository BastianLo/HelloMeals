# Generated by Django 4.2.1 on 2023-06-19 16:58

from django.db import migrations


def populate_recipe_foreignkey(apps, schema_editor):
    Recipe = apps.get_model('MealManager', 'Recipe')

    for recipe in Recipe.objects.all():
        ingredient_groups = recipe.ingredient_groups.all()
        for ingredient_group in ingredient_groups:
            ingredient_group.related_recipe = recipe
            ingredient_group.save()


class Migration(migrations.Migration):
    dependencies = [
        ('MealManager', '0046_ingredientgroup_related_recipe'),
    ]
    operations = [
        migrations.RunPython(populate_recipe_foreignkey),
    ]