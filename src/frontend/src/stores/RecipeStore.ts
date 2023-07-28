import {defineStore} from 'pinia'
import authorizedFetch from "../../composables/authorizedFetch";

const baseUrl = import.meta.env.DEV ? 'http://localhost:8000/api' : window.location.origin + "/api"

export const useRecipeStore = defineStore({
    id: 'recipeStore',
    state: () => ({
        recipes: [],
    }),
    getters: {},
    actions: {
        async fetch_recipes() {
            const response = await authorizedFetch(baseUrl + '/Recipe', {
                method: "GET",
            })
            const jsonResponse = await response.json()
            if (response.ok) {
                this.recipes = jsonResponse.results
            }
        },
    }
})