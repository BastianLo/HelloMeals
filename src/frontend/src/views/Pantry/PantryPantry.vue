<script setup lang="ts">
import {ref} from "vue";
import {usePantryStore} from "@/stores/PantryStore";

const store = usePantryStore()
const focus = ref(false)
</script>

<template>


  <div class="bg-slate-900 text-white font-sans p-4">
    <h1 class="text-3xl font-semibold mb-4">Einkaufsliste</h1>
    <div class="mt-4 relative">
      <input
          id="ingredientInput"
          type="text"
          class="bg-gray-800 text-white px-4 py-2 rounded-md w-full"
          placeholder="Add an item"
          @focus="focus = true"
          @blur="focus = false"
      />
      <div v-if="focus" id="autocomplete"
           class="absolute left-0 mt-2 w-full max-w-sm mx-auto bg-gray-700 rounded-lg shadow-md z-50">
        <div class="p-2 hover:bg-gray-600 cursor-pointer">Suggestion 1</div>
        <div class="p-2 hover:bg-gray-600 cursor-pointer">Suggestion 2</div>
        <div class="p-2 hover:bg-gray-600 cursor-pointer">Suggestion 3</div>
        <div class="p-2 hover:bg-gray-600 cursor-pointer">Suggestion 4</div>
        <div class="p-2 hover:bg-gray-600 cursor-pointer">Suggestion 5</div>
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