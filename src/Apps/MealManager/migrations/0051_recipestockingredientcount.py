# Generated by Django 4.2.1 on 2023-06-25 16:29

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('MealManager', '0050_alter_invitetoken_issuer'),
    ]

    operations = [
        migrations.CreateModel(
            name='RecipeStockIngredientCount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ingredientCount', models.IntegerField()),
                ('ingredientMax', models.IntegerField()),
                ('recipe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='MealManager.recipe')),
                ('stock', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='MealManager.stock')),
            ],
        ),
    ]