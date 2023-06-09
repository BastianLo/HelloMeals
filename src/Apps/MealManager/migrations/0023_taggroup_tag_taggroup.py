# Generated by Django 4.2.1 on 2023-05-28 11:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('MealManager', '0022_recipe_isplus_recipe_viewcount'),
    ]

    operations = [
        migrations.CreateModel(
            name='TagGroup',
            fields=[
                ('name', models.CharField(max_length=255, primary_key=True, serialize=False, unique=True)),
            ],
        ),
        migrations.AddField(
            model_name='tag',
            name='tagGroup',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='MealManager.taggroup'),
        ),
    ]
