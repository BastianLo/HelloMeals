# Generated by Django 4.2.1 on 2023-06-19 16:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('MealManager', '0045_stock_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='ingredientgroup',
            name='related_recipe',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='MealManager.recipe'),
        ),
    ]