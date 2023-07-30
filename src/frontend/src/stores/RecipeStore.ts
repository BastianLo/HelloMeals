import {defineStore} from 'pinia'
import authorizedFetch from "@/composables/authorizedFetch";
import {Recipe} from "@/types/Recipe";

const baseUrl = import.meta.env.DEV ? 'http://localhost:8000/api' : window.location.origin + "/api"

export const useRecipeStore = defineStore({
    id: 'recipeStore',
    state: () => ({
        recipes: [] as Recipe[],
        navigation: [],
        base_information: {
            totalRecipeCount: null,
            favoriteRecipeCount: null
        },
    }),
    getters: {},
    actions: {
        async fetch_recipes() {
            const response = await authorizedFetch(baseUrl + '/Recipe', {
                method: "GET",
            });
            const jsonResponse = await response.json();
            if (response.ok) {
                // Clear existing recipes to avoid duplicates
                this.recipes = [];
                jsonResponse.results.forEach((recipeData: any) => {
                    // Create a new Recipe object and push it to the recipes array
                    const recipe = new Recipe();
                    Object.assign(recipe, recipeData);
                    this.recipes.push(recipe);
                });
            }
        },
        async favorite_recipe(recipe: Recipe) {
            await authorizedFetch(baseUrl + `/Recipe/${recipe.helloFreshId}/favorite/${!recipe.favorited}`, {
                method: "POST",
            });
        },
        async get_recipe_by_id(recipe_id: string, fields: string[] = []) {
            const response = await authorizedFetch(baseUrl + `/Recipe/${recipe_id}?query={${fields.join(',')}}`, {
                method: "GET",
            });
            const jsonResponse = await response.json();
            if (response.ok) {
                return jsonResponse;
            }
        },
        async fetch_base_information() {
            const response = await authorizedFetch(baseUrl + '/Recipe/BaseInformation', {
                method: "GET",
            })
            const jsonResponse = await response.json()
            if (response.ok) {
                this.base_information = jsonResponse
            }
        },
    }
})