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

        difficulty: null as number | null,
        rating_gte: "0",
        // kept as plain minutes for a friendly UI; converted to an ISO-8601 duration
        // ("PT<n>M") only when building the actual API query, see get_query()
        prep_time_minutes: "",

        ordering: null as string | null,


        page: "1",
        page_size: "24",
    }),
    getters: {
        // number of filters currently narrowing the result set, excluding pagination/sort -
        // used to badge the filter button so it's obvious something is active
        active_filter_count(state): number {
            let count = 0
            if (state.calories_lt !== "2000" || state.calories_gt !== "0") count++
            if (state.protein_lt !== "200" || state.protein_gt !== "0") count++
            if (state.carbs_lt !== "200" || state.carbs_gt !== "0") count++
            if (state.fat_lt !== "200" || state.fat_gt !== "0") count++
            if (state.recipeType !== null) count++
            if (state.sources.length > 0) count++
            if (state.difficulty !== null) count++
            if (state.rating_gte !== "0") count++
            if (state.prep_time_minutes !== "") count++
            if (state.favorited) count++
            return count
        },
    },
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
            this.favorited = null
            this.difficulty = null
            this.rating_gte = "0"
            this.prep_time_minutes = ""

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
            const recipeTypeParam = parsedUrl.searchParams.get('recipeType')
            this.recipeType = recipeTypeParam !== null ? parseInt(recipeTypeParam) : null
            this.sources = (parsedUrl.searchParams.get('source') || '').split(",").filter(s => s !== '').map(s => parseInt(s))
            this.srch = parsedUrl.searchParams.get('srch') || ''

            const favoritedParam = parsedUrl.searchParams.get('favorited')
            if (favoritedParam !== null) {
                this.favorited = favoritedParam === 'true'
            }

            const difficultyParam = parsedUrl.searchParams.get('difficulty')
            this.difficulty = difficultyParam ? parseInt(difficultyParam) : null
            this.rating_gte = parsedUrl.searchParams.get('average_rating_gte') || "0"
            const prepTimeParam = parsedUrl.searchParams.get('prep_time_lte')
            this.prep_time_minutes = prepTimeParam ? (prepTimeParam.match(/PT(\d+)M/)?.[1] || '') : ''

            this.ordering = parsedUrl.searchParams.get('ordering')

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
            if (this.recipeType !== null)
                query.recipeType = this.recipeType.toString()
            if (this.sources.length)
                query.source = this.sources.join(",")
            if (this.ordering)
                query.ordering = this.ordering
            if (this.srch)
                query.srch = this.srch
            if (this.favorited)
                query.favorited = this.favorited.toString()
            if (this.difficulty)
                query.difficulty = this.difficulty.toString()
            if (this.rating_gte && this.rating_gte !== "0")
                query.average_rating_gte = this.rating_gte
            if (this.prep_time_minutes)
                query.prep_time_lte = `PT${this.prep_time_minutes}M`
            return query
        },
        get_query_string() {
            return new URLSearchParams(this.get_query()).toString();
        },
    }
})
