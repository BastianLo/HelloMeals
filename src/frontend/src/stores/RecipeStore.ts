import {defineStore} from 'pinia'
import authorizedFetch from "@/composables/authorizedFetch";
import {Recipe} from "@/types/Recipe";
import {Navigation} from "@/types/common/Navigation";

const baseUrl = import.meta.env.DEV ? 'http://localhost:8000/api' : window.location.origin + "/api"

export const useRecipeStore = defineStore({
    id: 'recipeStore',
    state: () => ({
        recipes: [] as Recipe[],
        navigation: new Navigation(),
        base_information: {
            totalRecipeCount: null,
            favoriteRecipeCount: null
        },
        params: {
            page: "1",
            page_size: "24"
        }
    }),
    getters: {},
    actions: {
        async fetch_recipes(keep_url_params: boolean = true) {
            let apiUrl = baseUrl + '/Recipe'
            this.parse_query(window.location.href)
            this.$router.push({query: this.get_query()})
            if (keep_url_params) {
                apiUrl += '?' + this.get_query_string()
            }
            await this.fetch_recipes_by_url(apiUrl)
        },
        get_query() {
            return {
                page: this.params.page,
                page_size: this.params.page_size,
            }
        },
        get_query_string() {
            return new URLSearchParams(this.get_query()).toString();
        },
        parse_query(url: string) {
            const parsedUrl = new URL(url)
            this.params.page = parsedUrl.searchParams.get('page')!
            this.params.page_size = parsedUrl.searchParams.get('page_size')!
            this.params = {
                page: this.get_query().page || "1",
                page_size: this.get_query().page_size || "24"
            }
        },
        async fetch_recipes_by_url(url: string) {
            this.parse_query(url)
            this.$router.push({query: this.get_query()})
            const response = await authorizedFetch(url, {
                method: "GET",
            });
            const jsonResponse = await response.json();
            if (response.ok) {
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