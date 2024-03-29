<script setup lang="ts">
import {ref} from "vue";
import {usePantryStore} from "@/stores/PantryStore";
import type {Ref} from "@vue/runtime-core";
import {useIngredientStore} from "@/stores/IngredientStore";
import type {Navigation} from "@/types/common/Navigation";
import {OnClickOutside} from '@vueuse/components'

const store = usePantryStore()
const ingredientStore = useIngredientStore()
const focus = ref(false)
const suggestionsHovered = ref(false)
const searchString = ref('')

interface ingredient {
  helloFreshId: string
  image: string
  name: string
  usage_count: number
  HelloFreshImageUrl: string
  children: ingredient[]
  open: boolean
}

const suggestions = ref([]) as Ref<ingredient[]>
const suggestionNavigation = ref({} as Navigation)

const updateSuggestions = async () => {
  const result = await ingredientStore.getIngredients(searchString.value)
  suggestions.value = result.results
  suggestionNavigation.value = result.navigation
}
const updateSuggestionsByUrl = async (url: string) => {
  const result = await ingredientStore.fetchByUrl(url)
  suggestions.value = result.results
  suggestionNavigation.value = result.navigation
}


const unFocus = () => {
  setTimeout(() => {
    focus.value = false
  }, 1000)
}
</script>

<template>


  <div class="bg-slate-900 text-white font-sans p-4">
    <h1 class="text-3xl font-semibold mb-4">Vorratsliste</h1>
    <div class="mt-4 relative">
      <input
          id="ingredientInput"
          type="text"
          class="bg-gray-800 text-white px-4 py-2 rounded-md w-full"
          placeholder="Füge ein Produkt hinzu"
          v-model="searchString"
          @focus="focus = true; suggestionsHovered = true"
          @blur="unFocus()"
          @input="updateSuggestions()"
      />
      <OnClickOutside @trigger="suggestionsHovered = focus">
        <div v-if="focus || suggestionsHovered" id="autocomplete"
             class="absolute left-0 mt-2 w-full max-w-sm mx-auto bg-gray-700 rounded-lg shadow-md z-50">
          <div
              @click="store.addIngredientToPantry(suggestion.helloFreshId); searchString = ''; focus=false; suggestionsHovered = false"
              v-for="suggestion in suggestions" class="p-2 hover:bg-gray-600 cursor-pointer">
            <div class="flex justify-between items-center">
              <span>{{ suggestion.name }}</span>
              <span class="text-gray-500">{{ suggestion.usage_count }}</span>
            </div>
          </div>

          <div class="flex justify-center mt-2" v-if="suggestions.length > 0">
            <span class="text-sm text-gray-400">
              Zeige <span class="font-semibold text-white"
                          v-text="suggestionNavigation.start"></span> bis <span
                class="font-semibold text-white"
                v-text="suggestionNavigation.end"></span> von <span
                class="font-semibold text-white"
                v-text="suggestionNavigation.count"></span> Einträgen
            </span>
            <button @click="updateSuggestionsByUrl(suggestionNavigation.previous!)"
                    class="w-6 h-4 mr-2 ml-4 bg-gray-600 text-white  flex items-center justify-center">
              <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor"
                   class="w-4 h-4">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"/>
              </svg>
            </button>
            <button @click="updateSuggestionsByUrl(suggestionNavigation.next!)"
                    class="w-6 h-4 bg-gray-600 text-white  flex items-center justify-center">
              <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor"
                   class="w-4 h-4">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/>
              </svg>
            </button>
          </div>
        </div>
      </OnClickOutside>

    </div>
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 mt-4">
      <div
          v-for="(ingredient, index) in store.PantryIngredients"
          :key="index"
          @mouseover="ingredient.isHovered = true"
          @mousedown="ingredient.isHovered = true"
          @mouseup="ingredient.isHovered = false"
          @mouseout="ingredient.isHovered = false"
          class="bg-gray-800 rounded-lg p-4 shadow-md relative"
      >
        <div class="flex justify-between">
      <span
          class="text-xl overflow-hidden overflow-ellipsis whitespace-nowrap max-w-[80%]"
          :class="{ 'hover:max-w-none hover:whitespace-normal': ingredient.isHovered }"
      >
        {{ ingredient.name }}
      </span>
          <div class="flex items-center whitespace-nowrap">
            <button
                @click="store.removeIngredientFromPantry(ingredient.helloFreshId)"
                class="text-white px-2 py-1 rounded hover:bg-red-700 focus:ring-red-900 bg-red-600 focus:outline-none focus:ring-4"
            >
              Remove
            </button>
            <button @click="ingredient.showMenu = !ingredient.showMenu"
                    class="ml-2 py-1 text-white whitespace-nowrap relative">
              <!-- Vertical dots SVG or other icon representing more options -->
              <svg width="20px" height="15px" viewBox="0 0 16 16" xmlns="http://www.w3.org/2000/svg" fill="#ffffff"
                   class="bi bi-three-dots-vertical">
                <path
                    d="M9.5 13a1.5 1.5 0 1 1-3 0 1.5 1.5 0 0 1 3 0zm0-5a1.5 1.5 0 1 1-3 0 1.5 1.5 0 0 1 3 0zm0-5a1.5 1.5 0 1 1-3 0 1.5 1.5 0 0 1 3 0z"/>
              </svg>
              <OnClickOutside @trigger="ingredient.showMenu = false">
                <div v-if="ingredient.showMenu"
                     class="absolute left-0 mt-2 w-48 bg-gray-700 rounded-lg shadow-md z-50 transform -translate-x-44 hover:bg-gray-600"
                >
                  <router-link :to="{name: 'RecipeAll', query: {ingredientId: ingredient.helloFreshId}}"
                               class="pt-2  cursor-pointer">
                    <p>Zeige Rezepte</p>
                  </router-link>
                </div>
              </OnClickOutside>
            </button>
          </div>
        </div>
      </div>
    </div>


  </div>


</template>

<style scoped>

</style>