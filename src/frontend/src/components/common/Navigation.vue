<script setup lang="ts">

import {useRecipeStore} from "@/stores/RecipeStore";
import {useRecipeFilterStore} from "@/stores/RecipeFilterStore";
import {storeToRefs} from "pinia";
import {computed} from "vue";

let recipeStoreRefs = storeToRefs(useRecipeStore())
let recipeStore = useRecipeStore()
let recipeFilterStore = useRecipeFilterStore()
let nav = recipeStoreRefs.navigation

const pageSize = computed(() => parseInt(recipeFilterStore.page_size || "24"))
const currentPage = computed(() => parseInt(recipeFilterStore.page || "1"))
const totalPages = computed(() => {
  if (!nav.value.count) return 1
  return Math.max(1, Math.ceil(nav.value.count / pageSize.value))
})

// windowed page list with ellipsis markers, e.g. [1, '...', 4, 5, 6, '...', 42]
const pageItems = computed(() => {
  const total = totalPages.value
  const current = currentPage.value
  const neighbours = 1
  const items: (number | '...')[] = [1]

  const left = Math.max(2, current - neighbours)
  const right = Math.min(total - 1, current + neighbours)

  if (left > 2) items.push('...')
  for (let i = left; i <= right; i++) items.push(i)
  if (right < total - 1) items.push('...')
  if (total > 1) items.push(total)

  return items
})

const goToPage = async (page: number) => {
  if (page < 1 || page > totalPages.value || page === currentPage.value) return
  recipeFilterStore.page = page.toString()
  await recipeStore.fetch_recipes(false)
  window.scrollTo(0, 0);
}

</script>

<template>
  <div class="flex flex-col items-center mb-24">
    <span class="text-sm text-gray-400 mb-3">
      Zeige <span class="font-semibold text-white" v-text="nav.start"></span> bis
      <span class="font-semibold text-white" v-text="nav.end"></span> von
      <span class="font-semibold text-white" v-text="nav.count"></span> Rezepten
    </span>
    <nav class="inline-flex items-center flex-wrap justify-center gap-1" aria-label="Seiten-Navigation">
      <button
          @click="goToPage(1)"
          :disabled="currentPage <= 1"
          title="Erste Seite"
          class="px-3 py-2 text-sm font-medium rounded bg-gray-800 border border-gray-700 text-gray-400 hover:bg-gray-700 hover:text-white disabled:opacity-40 disabled:hover:bg-gray-800 disabled:hover:text-gray-400">
        «
      </button>
      <button
          @click="goToPage(currentPage - 1)"
          :disabled="currentPage <= 1"
          title="Zurück"
          class="px-3 py-2 text-sm font-medium rounded bg-gray-800 border border-gray-700 text-gray-400 hover:bg-gray-700 hover:text-white disabled:opacity-40 disabled:hover:bg-gray-800 disabled:hover:text-gray-400">
        Zurück
      </button>

      <template v-for="item in pageItems">
        <span v-if="item === '...'" class="px-2 text-gray-500 select-none">…</span>
        <button v-else
                @click="goToPage(item)"
                :class="item === currentPage ? 'bg-blue-600 text-white border-blue-600' : 'bg-gray-800 text-gray-400 border-gray-700 hover:bg-gray-700 hover:text-white'"
                class="min-w-[2.5rem] px-3 py-2 text-sm font-medium rounded border"
                v-text="item">
        </button>
      </template>

      <button
          @click="goToPage(currentPage + 1)"
          :disabled="currentPage >= totalPages"
          title="Weiter"
          class="px-3 py-2 text-sm font-medium rounded bg-gray-800 border border-gray-700 text-gray-400 hover:bg-gray-700 hover:text-white disabled:opacity-40 disabled:hover:bg-gray-800 disabled:hover:text-gray-400">
        Weiter
      </button>
      <button
          @click="goToPage(totalPages)"
          :disabled="currentPage >= totalPages"
          title="Letzte Seite"
          class="px-3 py-2 text-sm font-medium rounded bg-gray-800 border border-gray-700 text-gray-400 hover:bg-gray-700 hover:text-white disabled:opacity-40 disabled:hover:bg-gray-800 disabled:hover:text-gray-400">
        »
      </button>
    </nav>
  </div>
</template>

<style scoped>
</style>
