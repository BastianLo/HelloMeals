import {defineStore} from 'pinia'


export const useRecipeFilterStore = defineStore({
    id: 'recipeFilterStore',
    state: () => ({
        calories_lt: "2000",
        calories_gt: "0",
        protein_lt: "200",
        protein_gt: "0",
        carbs_lt: "200",
        carbs_gt: "0",
        fat_lt: "200",
        fat_gt: "0",
        page: "1",
        page_size: "24",
    }),
    getters: {},
    actions: {}
})