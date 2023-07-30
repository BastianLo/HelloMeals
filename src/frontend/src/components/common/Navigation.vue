<script setup lang="ts">

import {useRecipeStore} from "@/stores/RecipeStore";
import {storeToRefs} from "pinia";

let recipeStore = storeToRefs(useRecipeStore())
let nav = recipeStore.navigation
</script>

<template>
  <div class="flex flex-col items-center mb-24">
            <span class="text-sm text-gray-700 dark:text-gray-400">
              Zeige <span class="font-semibold text-gray-900 dark:text-white"
                          v-text="nav.start"></span> bis <span
                class="font-semibold text-gray-900 dark:text-white"
                v-text="nav.end"></span> von <span
                class="font-semibold text-gray-900 dark:text-white"
                v-text="nav.count"></span> Einträgen
            </span>
    <div class="inline-flex mt-2 xs:mt-0">
      <button
          class="px-4 py-2 text-sm font-medium text-white bg-gray-800 rounded-l hover:bg-gray-900 dark:bg-gray-800 dark:border-gray-700 dark:text-gray-400 dark:hover:bg-gray-700 dark:hover:text-white">
        Zurück
      </button>
      <button
          class="px-4 py-2 text-sm font-medium text-white bg-gray-800 border-0 border-l border-gray-700 rounded-r hover:bg-gray-900 dark:bg-gray-800 dark:border-gray-700 dark:text-gray-400 dark:hover:bg-gray-700 dark:hover:text-white">
        Weiter
      </button>
    </div>
  </div>
</template>

<style scoped>

</style>