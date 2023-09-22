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
        recipeType: null as number | null,
        sources: [] as number[],
        srch: '',
        favorited: null as boolean | null,
        ingredientId: null as string | null,

        ordering: null as string | null,


        page: "1",
        page_size: "24",
    }),
    getters: {},
    actions: {
        reset() {
            this.calories_lt = "2000"
            this.calories_gt = "0"
            this.protein_lt = "200"
            this.protein_gt = "0"
            this.carbs_lt = "200"
            this.carbs_gt = "0"
            this.fat_lt = "200"
            this.fat_gt = "0"
            this.recipeType = null
            this.sources = []
            this.srch = ''

            this.ordering = null

            this.page = "1"
            this.page_size = "24"
        },
        parse_query(url: string) {
            const parsedUrl = new URL(url)
            this.calories_lt = parsedUrl.searchParams.get('calories_lt') || "2000"
            this.calories_gt = parsedUrl.searchParams.get('calories_gt') || "0"
            this.protein_lt = parsedUrl.searchParams.get('protein_lt') || "200"
            this.protein_gt = parsedUrl.searchParams.get('protein_gt') || "0"
            this.carbs_lt = parsedUrl.searchParams.get('carbs_lt') || "200"
            this.carbs_gt = parsedUrl.searchParams.get('carbs_gt') || "0"
            this.fat_lt = parsedUrl.searchParams.get('fat_lt') || "200"
            this.fat_gt = parsedUrl.searchParams.get('fat_gt') || "0"
            this.recipeType = parsedUrl.searchParams.get('recipeType') as number | null
            this.sources = (parsedUrl.searchParams.get('source') || '').split(",").filter(s => s !== '').map(s => parseInt(s))
            this.srch = parsedUrl.searchParams.get('srch') || ''

            this.ordering = parsedUrl.searchParams.get('ordering')

            this.ingredientId = parsedUrl.searchParams.get('ingredients') ? parsedUrl.searchParams.get('ingredients') : this.ingredientId

            this.page = parsedUrl.searchParams.get('page')!
            this.page_size = parsedUrl.searchParams.get('page_size')!
        },
        get_query() {
            const query: Record<string, string> = {}
            query.page = this.page || "1"
            query.page_size = this.page_size || "24"
            if (this.calories_lt && this.calories_lt !== "2000")
                query.calories_lt = this.calories_lt
            if (this.calories_gt && this.calories_gt !== "0")
                query.calories_gt = this.calories_gt
            if (this.protein_lt && this.protein_lt !== "200")
                query.protein_lt = this.protein_lt
            if (this.protein_gt && this.protein_gt !== "0")
                query.protein_gt = this.protein_gt
            if (this.carbs_lt && this.carbs_lt !== "200")
                query.carbs_lt = this.carbs_lt
            if (this.carbs_gt && this.carbs_gt !== "0")
                query.carbs_gt = this.carbs_gt
            if (this.fat_lt && this.fat_lt !== "200")
                query.fat_lt = this.fat_lt
            if (this.fat_gt && this.fat_gt !== "0")
                query.fat_gt = this.fat_gt
            if (this.recipeType)
                query.recipeType = this.recipeType.toString()
            if (this.sources.length)
                query.source = this.sources.join(",")
            if (this.ordering)
                query.ordering = this.ordering
            if (this.srch)
                query.srch = this.srch
            if (this.favorited)
                query.favorited = this.favorited.toString()
            if (this.ingredientId)
                query.ingredients = this.ingredientId!
            return query
        },
        get_query_string() {
            return new URLSearchParams(this.get_query()).toString();
        },
    }
})