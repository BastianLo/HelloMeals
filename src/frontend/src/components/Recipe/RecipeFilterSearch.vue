<script setup lang="ts">
import {OnClickOutside} from '@vueuse/components'
import Slider from '@vueform/slider'
import {ref} from "vue";
import {useRecipeStore} from "@/stores/RecipeStore";
import {useRecipeFilterStore} from "@/stores/RecipeFilterStore";

let recipeStore = useRecipeStore()
let recipeFilterRefs = useRecipeFilterStore()
const show = ref(false)
const searchString = ref('')
const openFilter = ref({
  nutrients: false
})
let sliders = ref([
  {
    title: "Kalorien",
    min: 0,
    max: 2000,
    value: ref([recipeFilterRefs.calories_gt, recipeFilterRefs.calories_lt]),
    format: function (value: number) {
      return `${value} kcal`
    }
  },
  {
    title: "Protein",
    min: 0,
    max: 200,
    value: ref([recipeFilterRefs.protein_gt, recipeFilterRefs.protein_lt]),
    format: function (value: number) {
      return `${value}g`
    }
  },
  {
    title: "Kohlenhydrate",
    min: 0,
    max: 200,
    value: ref([recipeFilterRefs.carbs_gt, recipeFilterRefs.carbs_lt]),
    format: function (value: number) {
      return `${value}g`
    }
  },
  {
    title: "Fett",
    min: 0,
    max: 200,
    value: ref([recipeFilterRefs.fat_gt, recipeFilterRefs.fat_lt]),
    format: function (value: number) {
      return `${value}g`
    }
  },
])

const applyFilter = () => {
  console.log("applyFilter")
  recipeFilterRefs.calories_gt = sliders.value[0].value[0]
  recipeFilterRefs.calories_lt = sliders.value[0].value[1]
  recipeFilterRefs.protein_gt = sliders.value[1].value[0]
  recipeFilterRefs.protein_lt = sliders.value[1].value[1]
  recipeFilterRefs.carbs_gt = sliders.value[2].value[0]
  recipeFilterRefs.carbs_lt = sliders.value[2].value[1]
  recipeFilterRefs.fat_gt = sliders.value[3].value[0]
  recipeFilterRefs.fat_lt = sliders.value[3].value[1]
  recipeFilterRefs.page = "1"
}

const search = async () => {
  applyFilter()
  show.value = false
  await recipeStore.fetch_recipes(true, false)
}

const clearFilter = async () => {
  show.value = false
  recipeFilterRefs.reset()
  updateComponentValues()
  await recipeStore.fetch_recipes(false, false)
}

const updateComponentValues = () => {
  sliders.value[0].value = [recipeFilterRefs.calories_gt, recipeFilterRefs.calories_lt]
  sliders.value[1].value = [recipeFilterRefs.protein_gt, recipeFilterRefs.protein_lt]
  sliders.value[2].value = [recipeFilterRefs.carbs_gt, recipeFilterRefs.carbs_lt]
  sliders.value[3].value = [recipeFilterRefs.fat_gt, recipeFilterRefs.fat_lt]
}

</script>

<template>

  <!-- Filter button and Searchbox -->

  <div class="relative z-10 h-screen flex items-center justify-center" aria-labelledby="modal-title" role="dialog"
       aria-modal="true" v-if="show">
    <div class="fixed inset-0 bg-gray-500 bg-opacity-75 transition-opacity"></div>
    <div class="fixed inset-0 z-10 overflow-y-auto">
      <div class="flex items-center justify-center h-full p-4 text-center sm:p-0">
        <OnClickOutside @trigger="search()">
          <div style="width: 400px"
               class="relative transform overflow-hidden rounded-lg bg-white text-left shadow-xl transition-all sm:my-8 sm:w-full sm:max-w-lg">
            <div class="w-lg shadow p-5 rounded-lg dark:bg-gray-800">
              <!-- Popup head -->
              <div class="flex items-center justify-between mt-4">
                <p class="font-medium dark:text-white">
                  Filter
                </p>
                <button @click="search()"
                        class="text-white bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300 font-medium rounded-lg text-sm px-4 py-2 dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800">
                  Anwenden
                </button>
                <button @click="clearFilter()"
                        class="px-4 py-2 bg-gray-100 hover:bg-gray-200 text-gray-800 text-sm font-medium rounded-md">
                  Löschen
                </button>
              </div>
              <!-- Popup body -->
              <div class="mt-5">
                <div>
                  <div class="mb-5">
                    <h2 id="accordion-collapse-heading-2">
                      <button type="button"
                              @click="openFilter.nutrients = !openFilter.nutrients"
                              :class="{'border-b-0':openFilter.nutrients}"
                              class="flex items-center justify-between w-full p-5 font-medium text-left text-gray-500 border border-gray-200 focus:ring-4 focus:ring-gray-200 dark:focus:ring-gray-800 dark:border-gray-700 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-800"
                      >
                        <span :class="{'dark:text-white': openFilter.nutrients}"> Nährwerte </span>
                        <svg :class="{'rotate-180': openFilter.nutrients}" data-accordion-icon
                             class="w-6 h-6 shrink-0" fill="currentColor"
                             viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg">
                          <path fill-rule="evenodd"
                                d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z"
                                clip-rule="evenodd"></path>
                        </svg>
                      </button>
                    </h2>
                    <div :class="{ 'hidden': !openFilter.nutrients}" class="border dark:border-gray-700 border-t-0"
                         aria-labelledby="accordion-collapse-heading-2">
                      <div class="p-2 rounded">
                        <div v-for="slider in sliders" class="mb-4">
                          <div class="flex items-center mb-4 justify-between">
                            <p v-text="slider.title"
                               class="mr-4 text-lg font-extrabold leading-none tracking-tight text-gray-900 dark:text-white">
                            </p>
                            <div class="flex items-center">
                                                      <span
                                                          class="mr-2 text-lg font-extrabold leading-none tracking-tight text-gray-900 dark:text-white"
                                                          v-text="slider.value[0]"></span>
                              <span
                                  class="mr-2 text-lg font-extrabold leading-none tracking-tight text-gray-900 dark:text-white">-</span>
                              <span
                                  class="text-lg font-extrabold leading-none tracking-tight text-gray-900 dark:text-white"
                                  v-text="slider.value[1]"></span>
                            </div>
                          </div>
                          <Slider show-tooltip="drag" class="mb-5 ml-2 mr-2"
                                  v-model="slider.value"
                                  :min="slider.min"
                                  :max="slider.max"
                                  :step="slider.max/100"
                                  :merge="slider.max/5"
                                  :format="slider.format"
                                  tooltipPosition="bottom"
                          />
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </OnClickOutside>
      </div>
    </div>
  </div>
  <div class="mt-5 mb-5 flex flex-row justify-center ">
    <button class="p-1 mr-4" @click="show = !show">
      <svg class="w-6 h-6 mb-1 text-gray-500 dark:text-gray-400" aria-hidden="true" fill="currentColor"
           viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
        <path clip-rule="evenodd"
              d="M2.628 1.601C5.028 1.206 7.49 1 10 1s4.973.206 7.372.601a.75.75 0 01.628.74v2.288a2.25 2.25 0 01-.659 1.59l-4.682 4.683a2.25 2.25 0 00-.659 1.59v3.037c0 .684-.31 1.33-.844 1.757l-1.937 1.55A.75.75 0 018 18.25v-5.757a2.25 2.25 0 00-.659-1.591L2.659 6.22A2.25 2.25 0 012 4.629V2.34a.75.75 0 01.628-.74z"
              fill-rule="evenodd"></path>
      </svg>
    </button>
    <label for="default-search"
           class="mb-2 text-sm font-medium text-gray-900 sr-only dark:text-white">Suche</label>
    <div class="relative" style="width: 400px">
      <div class="absolute inset-y-0 left-0 flex items-center pl-3 pointer-events-none">
        <svg aria-hidden="true" class="w-5 h-5 text-gray-500 dark:text-gray-400" fill="none"
             stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path>
        </svg>
      </div>
      <input type="search" id="default-search" @keyup.enter="search()"
             v-model="searchString"
             class="block w-full p-4 pl-10 text-sm text-gray-900 border border-gray-300 rounded-lg bg-gray-50 focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
             placeholder="Rezeptname" required>
      <button type="button" @click="search()"
              class="text-white absolute right-2.5 bottom-2.5 bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300 font-medium rounded-lg text-sm px-4 py-2 dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800">
        Suche
      </button>
    </div>
  </div>

</template>

<style src="@vueform/slider/themes/default.css"></style>