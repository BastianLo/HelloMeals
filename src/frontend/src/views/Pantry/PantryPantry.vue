<script setup lang="ts">
import {ref} from "vue";
import {usePantryStore} from "@/stores/PantryStore";
import type {Ref} from "@vue/runtime-core";
import {useIngredientStore} from "@/stores/IngredientStore";

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

const updateSuggestions = async () => {
  suggestions.value = await ingredientStore.getIngredients(searchString.value)
}

const unFocus = () => {
  focus.value = false
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
          @focus="focus = true"
          @blur="unFocus()"
          @input="updateSuggestions()"
      />
      <div v-if="focus || suggestionsHovered" id="autocomplete" @mouseenter="suggestionsHovered = true"
           @mouseleave="suggestionsHovered = false"
           class="absolute left-0 mt-2 w-full max-w-sm mx-auto bg-gray-700 rounded-lg shadow-md z-50">
        <div @click="store.addIngredientToPantry(suggestion.helloFreshId); searchString = ''"
             v-for="suggestion in suggestions" class="p-2 hover:bg-gray-600 cursor-pointer">
          <div class="flex justify-between items-center">
            <span>{{ suggestion.name }}</span>
            <span class="text-gray-500">{{ suggestion.usage_count }}</span>
          </div>
        </div>
      </div>

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