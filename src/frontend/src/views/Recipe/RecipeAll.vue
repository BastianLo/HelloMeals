<template>
  <RefreshSwiper @refresh="load()"/>
  <div style="position: absolute; left:20px;right:20px;">
    <RecipeFilterSearch/>
    <navigation class="mt-10"/>
    <div class="grid grid-cols-1 gap-4 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 mx-auto mb-6 mt-10">
      <div v-for="recipe in recipeStore.recipes" :key="recipe.helloFreshId">
        <RecipeCard :recipe="recipe"/>
      </div>
    </div>
    <navigation/>

  </div>
</template>

<script setup lang="ts">
import {useRecipeStore} from "@/stores/RecipeStore";
import RecipeCard from "@/components/Recipe/RecipeCard.vue";
import Navigation from "@/components/common/Navigation.vue";
import RecipeFilterSearch from "@/components/Recipe/RecipeFilterSearch.vue";
import {useRouter} from "vue-router";
import {useRecipeFilterStore} from "@/stores/RecipeFilterStore";
import RefreshSwiper from "@/components/common/RefreshSwiper.vue";

const ingredientId: any = useRouter().currentRoute.value.query.ingredientId
useRecipeFilterStore().ingredientId = ingredientId
console.log(ingredientId)

const isFavoritePage = useRouter().currentRoute.value.name === "RecipeFavorites"
let recipeStore = useRecipeStore()
useRecipeFilterStore().favorited = isFavoritePage
const load = () => {
  recipeStore.fetch_recipes()
}

load()

</script>

<style scoped>

</style>