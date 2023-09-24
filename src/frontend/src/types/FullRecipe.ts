export interface FullRecipe {
    helloFreshId: string;
    utensils: ReadonlyArray<RecipeUtensil>;
    ingredient_groups: ReadonlyArray<IngredientGroupBase>;
    favorited: string;
    source: number;
    recipeType: ReadonlyArray<number>;
    name: string;
    author?: string | null;
    websiteLink?: string | null;
    prepTime?: string | null;
    totalTime?: string | null;
    difficulty?: number | null;
    createdAt?: string | null;
    updatedAt?: string | null;
    averageRating?: string | null;
    ratingCount?: number | null;
    servings: number | null;
    image: string | null;
    HelloFreshImageUrl?: string | null;
    isPremium?: boolean | null;
    headline?: string | null;
    videoLink?: string | null;
    isExcludedFromIndex?: boolean | null;
    description?: string | null;
    favoritesCount?: number | null;
    helloFreshActive?: boolean | null;
    cardLink?: string | null;
    clonedFrom?: string | null;
    highlighted?: boolean | null;
    isAddon?: boolean | null;
    isComplete?: boolean | null;
    isDinnerToLunch?: boolean | null;
    viewCount?: number | null;
    isPlus?: boolean | null;
    healthScore?: number | null;
    nutrients: Nutrient;
    work_steps: WorkStep[];
}

export interface WorkStep {
    id: string;
    index: number;
    description: string;
    image: string;
    HelloFreshImageUrl: string;
    relatedRecipe: string;
}

export interface RecipeUtensil {
    utensil: Utensil;
}

interface Nutrient {
    energyKj: number | null,
    energyKcal: number | null,
    fat: number | null,
    fatSaturated: number | null,
    carbs: number | null,
    sugar: number | null,
    protein: number | null,
    salt: number | null
}

export interface Utensil {
    name: string;
}

export interface IngredientGroupBase {
    id: string;
    name?: string | null;
    ingredients: IngredientWrapper[];
}

export interface IngredientWrapper {
    id: string;
    unit: string;
    amount: number;
    ingredient: Ingredient;
}

export interface Ingredient {
    helloFreshId: string;
    name: string;
    image: string;
    usage_count: number;
    available: boolean;
    HelloFreshImageUrl: string;
}
