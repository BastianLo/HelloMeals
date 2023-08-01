import {defineStore} from 'pinia'
import {Recipe} from "@/types/Recipe";
import {Navigation} from "@/types/common/Navigation";
import authorizedFetch, {useCommonStore} from "@/stores/CommonStore";
import {useRecipeFilterStore} from "@/stores/RecipeFilterStore";

const baseUrl = import.meta.env.DEV ? 'http://localhost:8000/api' : window.location.origin + "/api"

export const useRecipeStore = defineStore({
    id: 'recipeStore',
    state: () => ({
        recipes: [] as Recipe[],
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
                this.parse_query(window.location.href)
            await useCommonStore().router.push({query: this.get_query()})
            if (keep_url_params) {
                apiUrl += '?' + this.get_query_string()
            }
            console.log(apiUrl)
            await this.fetch_recipes_by_url(apiUrl)
        },
        get_query() {
            let query = {}
            query.page = this.recipeFilterStore.page || "1"
            query.page_size = this.recipeFilterStore.page_size || "24"
            console.log(this.recipeFilterStore.calories_lt)
            if (this.recipeFilterStore.calories_lt && this.recipeFilterStore.calories_lt !== "2000")
                query.calories_lt = this.recipeFilterStore.calories_lt
            if (this.recipeFilterStore.calories_gt && this.recipeFilterStore.calories_gt !== "0")
                query.calories_gt = this.recipeFilterStore.calories_gt
            if (this.recipeFilterStore.protein_lt && this.recipeFilterStore.protein_lt !== "200")
                query.protein_lt = this.recipeFilterStore.protein_lt
            if (this.recipeFilterStore.protein_gt && this.recipeFilterStore.protein_gt !== "0")
                query.protein_gt = this.recipeFilterStore.protein_gt
            if (this.recipeFilterStore.carbs_lt && this.recipeFilterStore.carbs_lt !== "200")
                query.carbs_lt = this.recipeFilterStore.carbs_lt
            if (this.recipeFilterStore.carbs_gt && this.recipeFilterStore.carbs_gt !== "0")
                query.carbs_gt = this.recipeFilterStore.carbs_gt
            if (this.recipeFilterStore.fat_lt && this.recipeFilterStore.fat_lt !== "200")
                query.fat_lt = this.recipeFilterStore.fat_lt
            if (this.recipeFilterStore.fat_gt && this.recipeFilterStore.fat_gt !== "0")
                query.fat_gt = this.recipeFilterStore.fat_gt
            console.log(query)
            return query
        },
        get_query_string() {
            return new URLSearchParams(this.get_query()).toString();
        },
        parse_query(url: string) {
            const parsedUrl = new URL(url)
            this.recipeFilterStore.page = parsedUrl.searchParams.get('page')!
            this.recipeFilterStore.page_size = parsedUrl.searchParams.get('page_size')!
            this.recipeFilterStore.calories_lt = parsedUrl.searchParams.get('calories_lt') || "2000"
            this.recipeFilterStore.calories_gt = parsedUrl.searchParams.get('calories_gt') || "0"
            this.recipeFilterStore.protein_lt = parsedUrl.searchParams.get('protein_lt') || "200"
            this.recipeFilterStore.protein_gt = parsedUrl.searchParams.get('protein_gt') || "0"
            this.recipeFilterStore.carbs_lt = parsedUrl.searchParams.get('carbs_lt') || "200"
            this.recipeFilterStore.carbs_gt = parsedUrl.searchParams.get('carbs_gt') || "0"
            this.recipeFilterStore.fat_lt = parsedUrl.searchParams.get('fat_lt') || "200"
            this.recipeFilterStore.fat_gt = parsedUrl.searchParams.get('fat_gt') || "0"
            //this.params = this.get_query()
        },
        async fetch_recipes_by_url(url: string) {
            this.parse_query(url)
            await useCommonStore().router.push({query: this.get_query()})
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
        async favorite_recipe(recipe: Recipe) {
            await authorizedFetch(baseUrl + `/Recipe/${recipe.helloFreshId}/favorite/${!recipe.favorited}`, {
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