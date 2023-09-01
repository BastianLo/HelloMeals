import {defineStore} from 'pinia'
import authorizedFetch from "@/stores/CommonStore";
import type {Navigation} from "@/types/common/Navigation";

const baseUrl = import.meta.env.DEV ? 'http://localhost:8000/api' : window.location.origin + "/api"


interface ingredient {
    helloFreshId: string
    image: string
    name: string
    usage_count: number
    HelloFreshImageUrl: string
    children: ingredient[]
    open: boolean
}

interface result {
    results: ingredient[],
    navigation: Navigation
}

export const useIngredientStore = defineStore({
    id: 'IngredientStore',
    state: () => ({
        ingredients: [] as ingredient[],
        targetIngredients: [] as ingredient[],
        nav: {} as Navigation,
        targetNav: {} as Navigation,
    }),
    getters: {},
    actions: {
        async fetchIngredients(searchString?: string) {
            const path = baseUrl + '/Ingredient?page_size=48' + (searchString ? `&srch=${searchString}` : '')
            const result: result = await this.fetchByUrl(path)
            this.ingredients = result.results
            this.nav = result.navigation
        },
        async fetchTargetIngredients(searchString?: string) {
            const path = baseUrl + '/Ingredient?page_size=48' + (searchString ? `&srch=${searchString}` : '')
            const result: result = await this.fetchByUrl(path)
            this.targetIngredients = result.results
            this.targetNav = result.navigation
        },
        async targetPrevious() {
            const result: result = await this.fetchByUrl(this.targetNav.previous!)
            this.targetIngredients = result.results
            this.targetNav = result.navigation
        },
        async targetNext() {
            const result: result = await this.fetchByUrl(this.targetNav.next!)
            this.targetIngredients = result.results
            this.targetNav = result.navigation
        },
        async previous() {
            const result: result = await this.fetchByUrl(this.nav.previous!)
            this.ingredients = result.results
            this.nav = result.navigation
        },
        async next() {
            const result: result = await this.fetchByUrl(this.nav.next!)
            this.ingredients = result.results
            this.nav = result.navigation
        },
        async assignIngredients(ingredients: string[], target: string) {
            for (const ingredient of ingredients) {
                await authorizedFetch(baseUrl + `/Ingredient/${ingredient}/assign/${target}`, {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                    }
                });
            }
        },
        async fetchByUrl(url: string) {
            const response = await authorizedFetch(url, {
                method: "GET",
            });
            const resultJson = await response!.json()

            return {
                results: resultJson.results,
                navigation: {
                    start: resultJson.start,
                    end: resultJson.end,
                    count: resultJson.count,
                    next: resultJson.next,
                    previous: resultJson.previous
                } as Navigation
            } as result
        },


    }
})