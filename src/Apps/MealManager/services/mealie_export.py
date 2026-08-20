import html
import json

from isodate import duration_isoformat

from ..models import RecipeIngredient, RecipeTag, WorkSteps


def _format_ingredient(recipe_ingredient):
    parts = []
    if recipe_ingredient.amount is not None:
        amount = recipe_ingredient.amount
        parts.append(str(int(amount)) if amount == amount.to_integral_value() else str(amount))
    if recipe_ingredient.unit:
        parts.append(recipe_ingredient.unit)
    parts.append(recipe_ingredient.ingredient.name)
    return " ".join(parts)


def _absolute_image_url(recipe, build_absolute_uri):
    """Prefer the original external source image (already a real, publicly resolvable URL) so
    the export works regardless of whether this HelloMeals instance itself is reachable from
    wherever the export ends up (e.g. Mealie fetching it, or a pasted-HTML import with no page
    origin to resolve a relative URL against). Only fall back to our own locally-downloaded copy
    - turned into an absolute URL via the request - when no external URL was ever recorded."""
    if recipe.HelloFreshImageUrl:
        return recipe.HelloFreshImageUrl
    if recipe.image and build_absolute_uri:
        return build_absolute_uri(recipe.image.url)
    return None


def build_recipe_json_ld(recipe, build_absolute_uri=None):
    ingredients = RecipeIngredient.objects.filter(
        ingredient_group__in=recipe.ingredient_groups.all()
    ).select_related("ingredient")
    work_steps = WorkSteps.objects.filter(relatedRecipe=recipe).order_by("index")
    tags = RecipeTag.objects.filter(recipe=recipe).select_related("tag")

    data = {
        "@context": "https://schema.org",
        "@type": "Recipe",
        "name": recipe.name,
    }
    if recipe.description:
        data["description"] = recipe.description
    image_url = _absolute_image_url(recipe, build_absolute_uri)
    if image_url:
        data["image"] = [image_url]
    if recipe.author:
        data["author"] = {"@type": "Person", "name": recipe.author}
    if recipe.servings:
        data["recipeYield"] = str(recipe.servings)
    if recipe.prepTime:
        data["prepTime"] = duration_isoformat(recipe.prepTime)
    if recipe.totalTime:
        data["totalTime"] = duration_isoformat(recipe.totalTime)
    if recipe.websiteLink:
        data["url"] = recipe.websiteLink

    ingredient_lines = [_format_ingredient(i) for i in ingredients]
    if ingredient_lines:
        data["recipeIngredient"] = ingredient_lines

    if work_steps:
        data["recipeInstructions"] = [
            {"@type": "HowToStep", "text": step.description} for step in work_steps
        ]

    tag_names = [t.tag.name for t in tags]
    if tag_names:
        data["keywords"] = ", ".join(tag_names)
        data["recipeCategory"] = tag_names[0]

    if recipe.nutrients:
        nutrition = {"@type": "NutritionInformation"}
        n = recipe.nutrients
        if n.energyKcal is not None:
            nutrition["calories"] = f"{n.energyKcal} kcal"
        if n.protein is not None:
            nutrition["proteinContent"] = f"{n.protein} g"
        if n.carbs is not None:
            nutrition["carbohydrateContent"] = f"{n.carbs} g"
        if n.fat is not None:
            nutrition["fatContent"] = f"{n.fat} g"
        if len(nutrition) > 1:
            data["nutrition"] = nutrition

    if recipe.ratingCount:
        data["aggregateRating"] = {
            "@type": "AggregateRating",
            "ratingValue": str(recipe.averageRating) if recipe.averageRating is not None else "0",
            "ratingCount": recipe.ratingCount,
        }

    return data


def build_recipe_html(recipe, build_absolute_uri=None):
    """Wrap the recipe's schema.org Recipe JSON-LD in a minimal HTML document, matching what
    Mealie's "paste HTML" recipe importer expects - the same JSON-LD shape our own Mob scraper
    already consumes when scraping recipe websites, just produced instead of parsed."""
    json_ld = json.dumps(build_recipe_json_ld(recipe, build_absolute_uri), ensure_ascii=False, indent=2)
    title = html.escape(recipe.name)
    return (
        "<!DOCTYPE html>\n"
        "<html>\n<head>\n"
        f"<title>{title}</title>\n"
        f'<script type="application/ld+json">\n{json_ld}\n</script>\n'
        "</head>\n<body></body>\n</html>\n"
    )
