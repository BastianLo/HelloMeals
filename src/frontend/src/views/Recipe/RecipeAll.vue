<template>
  <p>abc</p>
  <h1>ABC</h1>
  <p class="text-white">{{ recipeStore.recipes }}</p>
</template>

<script setup lang="ts">
import {useRecipeStore} from "@/stores/RecipeStore";

let recipeStore = useRecipeStore()
recipeStore.fetch_recipes()
</script>

<style scoped>

</style>