<script setup lang="ts">
import {ref} from "vue";
import {usePantryStore} from "@/stores/PantryStore";
import type {Ref} from "@vue/runtime-core";
import {useIngredientStore} from "@/stores/IngredientStore";
import type {Navigation} from "@/types/common/Navigation";
import {OnClickOutside} from "@vueuse/components/index";

const store = usePantryStore()
const ingredientStore = useIngredientStore()
const focus = ref(false)
const suggestionsHovered = ref(false)
const suggestionsAcutalHovered = ref(false)
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
    <h1 class="text-3xl font-semibold mb-4">Einkaufsliste</h1>
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
          <div @click="store.addIngredientToPantry(suggestion.helloFreshId); searchString = ''"
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
            <button @click="updateSuggestionsByUrl(suggestionNavigation.previous)"
                    class="w-6 h-4 mr-2 ml-4 bg-gray-600 text-white  flex items-center justify-center">
              <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor"
                   class="w-4 h-4">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"/>
              </svg>
            </button>
            <button @click="updateSuggestionsByUrl(suggestionNavigation.next)"
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
      <!-- @vue-ignore -->
      <div v-for="(ingredient, index) in store.PantryIngredients" :key="index"
           @mouseover="ingredient.isHovered = true"
           @mousedown="ingredient.isHovered = true"
           @mouseup="ingredient.isHovered = false"
           @mouseout="ingredient.isHovered = false"
           class="bg-gray-800 rounded-lg p-4 shadow-md">
        <div class="flex justify-between">
        <span
            class="text-xl overflow-hidden overflow-ellipsis whitespace-nowrap max-w-[80%]"
            :class="{ 'hover:max-w-none hover:whitespace-normal': ingredient.isHovered }"
        >
            {{ ingredient.name }}
        </span>
          <button @click="store.removeIngredientFromPantry(ingredient.helloFreshId)"
                  class="bg-red-500 text-white px-2 py-1 rounded">Remove
          </button>
        </div>
      </div>

    </div>
  </div>


</template>

<style scoped>

</style>