import type {Nutrients} from "@/types/Nutrients";

export class Recipe {
    helloFreshId: string;
    ingredient_count: number;
    available_ingredient_count: number;
    similarity: number;
    relevancy: number;
    favorited: boolean;
    source: number;
    recipeType: number;
    name: string;
    author: string;
    websiteLink: string;
    prepTime: string;
    totalTime: string;
    difficulty: number;
    createdAt: string;
    updatedAt: string;
    averageRating: string;
    ratingCount: number;
    servings: number;
    image: string;
    HelloFreshImageUrl: string;
    isPremium: boolean;
    headline: string;
    videoLink: string;
    isExcludedFromIndex: boolean;
    description: string;
    favoritesCount: number;
    helloFreshActive: boolean;
    cardLink: string;
    clonedFrom: string;
    highlighted: boolean;
    isAddon: boolean;
    isComplete: boolean;
    isDinnerToLunch: boolean;
    viewCount: number;
    isPlus: boolean;
    healthScore: number;
    nutrients: Nutrients;

    constructor(data: Partial<Recipe> = {}) {
        this.helloFreshId = data.helloFreshId || "";
        this.ingredient_count = data.ingredient_count || 0;
        this.available_ingredient_count = data.available_ingredient_count || 0;
        this.similarity = data.similarity || 0;
        this.relevancy = data.relevancy || 0;
        this.favorited = data.favorited || false;
        this.source = data.source || 0;
        this.recipeType = data.recipeType || 0;
        this.name = data.name || "";
        this.author = data.author || "";
        this.websiteLink = data.websiteLink || "";
        this.prepTime = data.prepTime || "";
        this.totalTime = data.totalTime || "";
        this.difficulty = data.difficulty || 0;
        this.createdAt = data.createdAt || "";
        this.updatedAt = data.updatedAt || "";
        this.averageRating = data.averageRating || "";
        this.ratingCount = data.ratingCount || 0;
        this.servings = data.servings || 0;
        this.image = data.image || "";
        this.HelloFreshImageUrl = data.HelloFreshImageUrl || "";
        this.isPremium = data.isPremium || false;
        this.headline = data.headline || "";
        this.videoLink = data.videoLink || "";
        this.isExcludedFromIndex = data.isExcludedFromIndex || false;
        this.description = data.description || "";
        this.favoritesCount = data.favoritesCount || 0;
        this.helloFreshActive = data.helloFreshActive || false;
        this.cardLink = data.cardLink || "";
        this.clonedFrom = data.clonedFrom || "";
        this.highlighted = data.highlighted || false;
        this.isAddon = data.isAddon || false;
        this.isComplete = data.isComplete || false;
        this.isDinnerToLunch = data.isDinnerToLunch || false;
        this.viewCount = data.viewCount || 0;
        this.isPlus = data.isPlus || false;
        this.healthScore = data.healthScore || 0;
        this.nutrients = data.nutrients || {
            energyKj: null,
            energyKcal: null,
            fat: null,
            fatSaturated: null,
            carbs: null,
            sugar: null,
            protein: null,
            salt: null,
        };
    }
}
