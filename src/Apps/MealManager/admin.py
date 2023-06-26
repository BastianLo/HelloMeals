from django.contrib import admin

from .models import *

# Register your models here.

admin.site.register(Profile)
admin.site.register(InviteToken)
admin.site.register(RecipeStockIngredientCount)
admin.site.register(Stock)
admin.site.register(ShoppingList)
admin.site.register(Recipe)
admin.site.register(Nutrients)
admin.site.register(Ingredient)
admin.site.register(IngredientGroup)
admin.site.register(Utensil)
admin.site.register(TagMerge)
admin.site.register(Tag)
admin.site.register(TagGroup)
admin.site.register(WorkSteps)
admin.site.register(RecipeIngredient)
admin.site.register(RecipeTag)
admin.site.register(RecipeUtensil)
