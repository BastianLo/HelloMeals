import {defineStore} from 'pinia'
import {useAuth} from "#imports";

const baseUrl = 'http://localhost:8000/api'

export const useRecipeStore = defineStore({
    id: 'auth',
    state: () => ({
        recipes: [],
        navigation: {
            count: null,
            start: null,
            end: null,
            next: null,
            previous: null
        },
    }),
    actions: {
        async fetchRecipes(force = false) {
            if (!force && this.recipes.length) {
                return
            }
            const response = await $fetch('http://127.0.0.1:8000/api/Recipe', {
                headers: {
                    "authorization": useAuth().token.value
                }
            })
            this.navigation.count = response.count
            this.navigation.start = response.start
            this.navigation.end = response.end
            this.navigation.next = response.next
            this.navigation.previous = response.previous
            this.recipes = response.results
        }
    }
})