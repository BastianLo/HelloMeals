<script setup lang="ts">

import {useRecipeStore} from "@/stores/RecipeStore";
import {storeToRefs} from "pinia";

let recipeStoreRefs = storeToRefs(useRecipeStore())
let recipeStore = useRecipeStore()
let nav = recipeStoreRefs.navigation

let previous = async () => {
  if (recipeStoreRefs.navigation.value.previous) {
    await recipeStore.fetch_recipes_by_url(recipeStoreRefs.navigation.value.previous!)
    window.scrollTo(0, 0);
  }
}
let next = async () => {
  if (recipeStoreRefs.navigation.value.next) {
    await recipeStore.fetch_recipes_by_url(recipeStoreRefs.navigation.value.next!)
    window.scrollTo(0, 0);
  }
}

</script>

<template>
  <div class="flex flex-col items-center mb-24">
            <span class="text-sm text-gray-400">
              Zeige <span class="font-semibold text-white"
                          v-text="nav.start"></span> bis <span
                class="font-semibold text-white"
                v-text="nav.end"></span> von <span
                class="font-semibold text-white"
                v-text="nav.count"></span> Einträgen
            </span>
    <div class="inline-flex mt-2 xs:mt-0">
      <button
          @click="previous()"
          class="px-4 py-2 text-sm font-medium rounded-l bg-gray-800 border-gray-700 text-gray-400 hover:bg-gray-700 hover:text-white">
        Zurück
      </button>
      <button
          @click="next()"
          class="px-4 py-2 text-sm font-medium border-0 border-l rounded-r bg-gray-800 border-gray-700 text-gray-400 hover:bg-gray-700 hover:text-white">
        Weiter
      </button>
    </div>
  </div>
</template>

<style scoped>

</style>