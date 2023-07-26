<template>
  <div>
    <h1>Recipes</h1>
    <p class="text-white" v-if="recipes.length">{{ recipes }}</p>
    <p v-else>Loading...</p>
  </div>
</template>


<script setup>
import {useRecipeStore} from "~/store/recipeStore";
import {storeToRefs} from "pinia";

useRecipeStore().fetchRecipes();
let recipes = storeToRefs(useRecipeStore()).recipes;
</script>
