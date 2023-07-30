<template>
  <p>abc</p>
  <h1>ABC</h1>
  <div class="grid grid-cols-1 gap-4 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 mx-auto mb-6 mt-10">
    <div v-for="recipe in recipeStore.recipes" :key="recipe.helloFreshId">
      <RecipeCard :recipe="recipe"/>
    </div>
  </div>

</template>

<script setup lang="ts">
import {useRecipeStore} from "@/stores/RecipeStore";
import RecipeCard from "@/components/Recipe/RecipeCard.vue";

let recipeStore = useRecipeStore()
recipeStore.fetch_recipes()
</script>

<style scoped>

</style>