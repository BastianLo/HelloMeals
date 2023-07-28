import {defineStore} from 'pinia'
import {useAuthStore} from "@/stores/AuthStore";

const baseUrl = import.meta.env.DEV ? 'http://localhost:8000/api' : window.location.origin + "/api"

export const useRecipeStore = defineStore({
    id: 'recipeStore',
    state: () => ({
        recipes: [],
    }),
    getters: {},
    actions: {
        async fetch_recipes() {
            const response = await fetch(baseUrl + '/Recipe', {
                method: "GET",
                headers: {
                    "Content-Type": "application/json",
                    "Authorization": "Bearer " + await (useAuthStore().get_valid_token())
                }
            })
            const jsonResponse = await response.json()
            if (response.ok) {
                this.recipes = jsonResponse.results
            }
        },
    }
})