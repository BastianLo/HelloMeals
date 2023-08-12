import {defineStore} from 'pinia'
import {Recipe} from "@/types/Recipe";
import {Navigation} from "@/types/common/Navigation";
import authorizedFetch, {useCommonStore} from "@/stores/CommonStore";
import {useRecipeFilterStore} from "@/stores/RecipeFilterStore";
import type {FullRecipe} from "@/types/FullRecipe";

const baseUrl = import.meta.env.DEV ? 'http://localhost:8000/api' : window.location.origin + "/api"

export const useRecipeStore = defineStore({
    id: 'recipeStore',
    state: () => ({
        recipes: [] as Recipe[],
        detailRecipe: {} as FullRecipe,
        recipeFilterStore: useRecipeFilterStore(),
        navigation: new Navigation(),
        base_information: {
            totalRecipeCount: null,
            favoriteRecipeCount: null
        },
    }),
    getters: {},
    actions: {
        async fetch_recipes(keep_url_params: boolean = true, parseUrlParams: boolean = true) {
            let apiUrl = baseUrl + '/Recipe'
            if (parseUrlParams)
                this.recipeFilterStore.parse_query(window.location.href)
            await useCommonStore().router.push({query: this.recipeFilterStore.get_query()})
            if (keep_url_params) {
                apiUrl += '?' + this.recipeFilterStore.get_query_string()
            }
            await this.fetch_recipes_by_url(apiUrl)
        },
        async fetch_recipes_by_url(url: string) {
            this.recipeFilterStore.parse_query(url)
            await useCommonStore().router.push({query: this.recipeFilterStore.get_query()})
            const response = await authorizedFetch(url, {
                method: "GET",
            });
            const jsonResponse = await response!.json();
            if (response!.ok) {
                this.recipes = [];
                jsonResponse.results.forEach((recipeData: any) => {
                    const recipe = new Recipe();
                    Object.assign(recipe, recipeData);
                    this.recipes.push(recipe);
                });

                const nav = {
                    start: jsonResponse.start,
                    end: jsonResponse.end,
                    count: jsonResponse.count,
                    next: jsonResponse.next,
                    previous: jsonResponse.previous
                } as Navigation;
                this.navigation = new Navigation(nav)
            }
        },
        async fetch_recipes_detail(id: string) {
            const response = await authorizedFetch(baseUrl + '/FullRecipe/' + id, {
                method: "GET",
            });
            const jsonResponse = await response!.json();
            if (response!.ok) {
                this.detailRecipe = jsonResponse
            }
        },
        async favorite_recipe(recipe: Recipe) {
            await authorizedFetch(baseUrl + `/Recipe/${recipe.helloFreshId}/favorite/${!recipe.favorited}`, {
                method: "POST",
            });
        },
        async favorite_recipe_value(id: String, value: boolean) {
            await authorizedFetch(baseUrl + `/Recipe/${id}/favorite/${value}`, {
                method: "POST",
            });
        },
        async get_recipe_by_id(recipe_id: string, fields: string[] = []) {
            const response = await authorizedFetch(baseUrl + `/Recipe/${recipe_id}?query={${fields.join(',')}}`, {
                method: "GET",
            });
            const jsonResponse = await response!.json();
            if (response!.ok) {
                return jsonResponse;
            }
        },
        async fetch_base_information() {
            const response = await authorizedFetch(baseUrl + '/Recipe/BaseInformation', {
                method: "GET",
            })
            const jsonResponse = await response!.json()
            if (response!.ok) {
                this.base_information = jsonResponse
            }
        },
    }
})