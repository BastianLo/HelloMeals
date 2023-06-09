# Generated by Django 4.2.1 on 2023-06-11 10:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MealManager', '0039_ingredient_parent'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ingredient',
            name='HelloFreshImageUrl',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='ingredient',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='images/ingredients'),
        ),
    ]
