<script setup lang="ts">
import {computed, ref} from "vue";
import {storeToRefs} from "pinia";
import {useRecipeStore} from "@/stores/RecipeStore";
import {Recipe} from "@/types/Recipe";
import RecipePreviewRow from "@/components/Recipe/RecipePreviewRow.vue";
import RefreshSwiper from "@/components/common/RefreshSwiper.vue";

const recipeStore = useRecipeStore()
const {base_information} = storeToRefs(recipeStore)

const newRecipes = ref([] as Recipe[])
const popularRecipes = ref([] as Recipe[])
const favoriteRecipes = ref([] as Recipe[])
const spotlightRecipe = ref(null as Recipe | null)

const sources = [
  {id: 1, name: 'HelloFresh', color: 'bg-lime-500 text-black'},
  {id: 2, name: 'KitchenStories', color: 'bg-yellow-500 text-black'},
  {id: 3, name: 'Chefkoch', color: 'bg-green-700 text-white'},
  {id: 4, name: 'Lecker', color: 'bg-pink-700 text-white'},
  {id: 5, name: 'EatSmarter', color: 'bg-orange-600 text-white'},
  {id: 6, name: 'Yazio', color: 'bg-pink-600 text-white'},
  {id: 7, name: 'Mob', color: 'bg-gray-600 text-white'},
]

const categories = [
  {id: 0, name: 'Hauptgerichte'},
  {id: 1, name: 'Frühstück'},
  {id: 2, name: 'Dessert'},
  {id: 3, name: 'Backen'},
  {id: 4, name: 'Getränke'},
]

const pickSpotlight = () => {
  const pool = [...newRecipes.value, ...popularRecipes.value]
  if (pool.length === 0) {
    spotlightRecipe.value = null
    return
  }
  spotlightRecipe.value = pool[Math.floor(Math.random() * pool.length)]
}

const load = async () => {
  await recipeStore.fetch_base_information()

  const [newest, popular, favorites] = await Promise.all([
    recipeStore.fetch_recipe_list({ordering: '-createdAt', page_size: '12'}),
    recipeStore.fetch_recipe_list({ordering: 'relevancy', page_size: '12'}),
    recipeStore.fetch_recipe_list({favorited: 'true', page_size: '12'}),
  ])
  newRecipes.value = newest
  popularRecipes.value = popular
  favoriteRecipes.value = favorites
  pickSpotlight()
}
load()

const hasFavorites = computed(() => favoriteRecipes.value.length > 0)
</script>

<template>
  <RefreshSwiper @refresh="load()"/>
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">

    <!-- Hero -->
    <div class="text-center mt-12 mb-10">
      <h1 class="text-3xl font-bold text-white mb-2">Willkommen bei HelloMeals</h1>
      <p class="text-gray-400 mb-6">
        <span v-if="base_information.totalRecipeCount !== null">{{ base_information.totalRecipeCount }} Rezepte</span>
        warten darauf, entdeckt zu werden.
      </p>
      <router-link :to="{name: 'RecipeAll'}"
                   class="inline-flex items-center px-6 py-3 text-white font-medium rounded-lg text-sm bg-gradient-to-r from-blue-600 to-blue-800 hover:from-blue-700 hover:to-blue-900 focus:ring-4 focus:ring-blue-800 focus:outline-none shadow-md">
        <svg aria-hidden="true" class="w-5 h-5 mr-2" fill="none" stroke="currentColor" stroke-width="2"
             viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
          <path stroke-linecap="round" stroke-linejoin="round" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path>
        </svg>
        Alle Rezepte durchsuchen
      </router-link>
    </div>

    <!-- Spotlight: a random pick from what's already loaded, no extra request -->
    <div class="mb-12" v-if="spotlightRecipe">
      <h2 class="text-xl font-semibold text-white mb-4">Zufällig entdeckt</h2>
      <router-link :to="'/Recipe/' + spotlightRecipe.helloFreshId"
                   class="relative block rounded-lg overflow-hidden group h-64">
        <img :src="spotlightRecipe.image" class="w-full h-full object-cover transition duration-300 group-hover:scale-105" alt=""/>
        <div class="absolute inset-0 bg-gradient-to-t from-black/85 via-black/10 to-transparent"></div>
        <div class="absolute bottom-0 left-0 right-0 p-6">
          <h3 class="text-2xl font-bold text-white mb-1" v-text="spotlightRecipe.name"></h3>
          <p class="text-gray-300 text-sm max-w-lg" v-text="spotlightRecipe.headline"></p>
        </div>
        <button @click.stop.prevent="pickSpotlight()" title="Anderen Vorschlag zeigen"
                class="absolute top-4 right-4 bg-black/50 hover:bg-black/70 text-white rounded-full p-2 transition">
          <svg aria-hidden="true" class="w-5 h-5" fill="none" stroke="currentColor" stroke-width="2"
               viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
            <path stroke-linecap="round" stroke-linejoin="round"
                  d="M16.023 9.348h4.992v-.001M2.985 19.644v-4.992m0 0h4.992m-4.993 0l3.181 3.183a8.25 8.25 0 0013.803-3.7M4.031 9.865a8.25 8.25 0 0113.803-3.7l3.181 3.182m0-4.991v4.99"></path>
          </svg>
        </button>
      </router-link>
    </div>

    <RecipePreviewRow title="Neu hinzugefügt" :recipes="newRecipes" see-all-to="/Recipe/All?ordering=-createdAt"/>
    <RecipePreviewRow title="Beliebte Rezepte" :recipes="popularRecipes" see-all-to="/Recipe/All?ordering=relevancy"/>
    <RecipePreviewRow v-if="hasFavorites" title="Deine Favoriten" :recipes="favoriteRecipes"
                       see-all-to="/Recipe/Favorites"/>

    <!-- Browse by source -->
    <section class="mb-12">
      <h2 class="text-xl font-semibold text-white mb-4 px-1">Nach Quelle stöbern</h2>
      <div class="flex flex-wrap gap-2 px-1">
        <router-link v-for="source in sources" :key="source.id"
                     :to="'/Recipe/All?source=' + source.id"
                     class="px-3 py-1.5 rounded-full text-sm font-medium hover:opacity-80 transition"
                     :class="source.color">
          {{ source.name }}
        </router-link>
      </div>
    </section>

    <!-- Browse by category -->
    <section class="mb-12">
      <h2 class="text-xl font-semibold text-white mb-4 px-1">Nach Kategorie stöbern</h2>
      <div class="flex flex-wrap gap-2 px-1">
        <router-link v-for="category in categories" :key="category.id"
                     :to="'/Recipe/All?recipeType=' + category.id"
                     class="px-3 py-1.5 rounded-full text-sm font-medium bg-gray-700 text-gray-200 hover:bg-gray-600 transition">
          {{ category.name }}
        </router-link>
      </div>
    </section>

  </div>
</template>

<style>
</style>
