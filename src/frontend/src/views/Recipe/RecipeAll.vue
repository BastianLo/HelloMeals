<template>
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

let recipeStore = useRecipeStore()
recipeStore.fetch_recipes()
</script>

<style scoped>

</style>