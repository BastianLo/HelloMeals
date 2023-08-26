<template>
  <RefreshSwiper @refresh="load()"/>
  <div class="flex flex-col items-center mt-12">
    <h2 class="text-lg font-semibold mb-6 text-gray-200">Explore Our Recipes</h2>
    <div class="space-y-4">
      <!-- Total Recipes Link -->
      <router-link
          class="px-6 py-3 text-white font-medium rounded-lg text-sm inline-flex items-center bg-gradient-to-r from-blue-600 to-blue-800 hover:from-blue-700 hover:to-blue-900 focus:ring-4 focus:ring-blue-800 focus:outline-none shadow-md block w-full"
          :to="{name: 'RecipeAll'}"
      >
        <span class="mr-2" v-text="'Alle Rezepte'"></span>
        <span
            class="bg-blue-700 rounded-full p-2 text-xs font-semibold leading-none text-white">Total Recipes: {{
            base_information.totalRecipeCount
          }}</span>
      </router-link>

      <!-- Favorite Recipes Link -->
      <router-link
          class="px-6 py-3 text-white font-medium rounded-lg text-sm inline-flex items-center bg-gradient-to-r from-yellow-500 to-yellow-700 hover:from-yellow-600 hover:to-yellow-800 focus:ring-4 focus:ring-yellow-800 focus:outline-none shadow-md block w-full"
          to="/Recipe/Favorites"
      >
        <span class="mr-2">Lieblingsrezepte</span>
        <span
            class="bg-yellow-600 rounded-full p-2 text-xs font-semibold leading-none text-white">Favorite Recipes: {{
            base_information.favoriteRecipeCount
          }}</span>
      </router-link>
    </div>
    <p class="text-gray-400 text-sm mt-6 text-center max-w-md">
      Looking for some delicious recipes to try? Browse our collection of recipes to find your next favorite dish!
    </p>
  </div>
</template>

<script setup lang="ts">
import {storeToRefs} from "pinia";
import {useRecipeStore} from "@/stores/RecipeStore";
import RefreshSwiper from "@/components/common/RefreshSwiper.vue";

let {base_information} = storeToRefs(useRecipeStore());

const load = () => {
  useRecipeStore().fetch_base_information();
}
load()
</script>

<style>
/* Add any additional styles here if needed */
</style>