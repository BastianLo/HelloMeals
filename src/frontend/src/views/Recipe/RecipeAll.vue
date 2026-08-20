<template>
  <RefreshSwiper @refresh="load()"/>
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">

    <!-- Header -->
    <div class="mt-8 mb-6">
      <h1 class="text-2xl font-bold text-white mb-1" v-text="pageTitle"></h1>
      <p class="text-sm text-gray-400" v-if="recipeStore.navigation.count !== null">
        {{ recipeStore.navigation.count }} {{ recipeStore.navigation.count === 1 ? 'Rezept' : 'Rezepte' }} gefunden
      </p>
    </div>

    <!-- Filter/Sort toolbar -->
    <div class="bg-gray-800 border border-gray-700 rounded-lg p-4 mb-8">
      <RecipeFilterSearch/>
    </div>

    <div v-if="recipeStore.recipes.length > 0">
      <Navigation/>
      <div class="grid grid-cols-1 gap-4 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 mx-auto mb-6">
        <div v-for="recipe in recipeStore.recipes" :key="recipe.helloFreshId">
          <RecipeCard :recipe="recipe"/>
        </div>
      </div>
      <Navigation/>
    </div>
    <div v-else class="text-center text-gray-400 py-24">
      Keine Rezepte gefunden. Versuche, den Filter anzupassen.
    </div>

  </div>
</template>

<script setup lang="ts">
import {computed} from "vue";
import {useRecipeStore} from "@/stores/RecipeStore";
import RecipeCard from "@/components/Recipe/RecipeCard.vue";
import Navigation from "@/components/common/Navigation.vue";
import RecipeFilterSearch from "@/components/Recipe/RecipeFilterSearch.vue";
import {useRouter} from "vue-router";
import {useRecipeFilterStore} from "@/stores/RecipeFilterStore";
import RefreshSwiper from "@/components/common/RefreshSwiper.vue";

const isFavoritePage = useRouter().currentRoute.value.name === "RecipeFavorites"
const pageTitle = computed(() => isFavoritePage ? "Deine Favoriten" : "Alle Rezepte")
let recipeStore = useRecipeStore()
useRecipeFilterStore().favorited = isFavoritePage
const load = () => {
  recipeStore.fetch_recipes()
}

load()

</script>

<style scoped>

</style>
