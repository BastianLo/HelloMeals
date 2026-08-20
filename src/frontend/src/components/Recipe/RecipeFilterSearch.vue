<script setup lang="ts">
import {OnClickOutside} from '@vueuse/components'
import Slider from '@vueform/slider'
import {ref} from "vue";
import {useRoute} from "vue-router";
import {useRecipeStore} from "@/stores/RecipeStore";
import {useRecipeFilterStore} from "@/stores/RecipeFilterStore";

let recipeStore = useRecipeStore()
let recipeFilterRefs = useRecipeFilterStore()
const isFavoritePage = useRoute().name === "RecipeFavorites"

const show = ref(false)
const showSortPopup = ref(false)
const showNutrients = ref(false)
const searchString = ref('')

let sliders = ref([
  {
    title: "Kalorien",
    min: 0,
    max: 2000,
    value: ref([recipeFilterRefs.calories_gt, recipeFilterRefs.calories_lt]),
    format: (value: number) => `${value} kcal`,
  },
  {
    title: "Protein",
    min: 0,
    max: 200,
    value: ref([recipeFilterRefs.protein_gt, recipeFilterRefs.protein_lt]),
    format: (value: number) => `${value}g`,
  },
  {
    title: "Kohlenhydrate",
    min: 0,
    max: 200,
    value: ref([recipeFilterRefs.carbs_gt, recipeFilterRefs.carbs_lt]),
    format: (value: number) => `${value}g`,
  },
  {
    title: "Fett",
    min: 0,
    max: 200,
    value: ref([recipeFilterRefs.fat_gt, recipeFilterRefs.fat_lt]),
    format: (value: number) => `${value}g`,
  },
])

const orderings = [
  {title: "Relevanz", value: "relevancy"},
  {title: "Neueste zuerst", value: "-createdAt"},
  {title: "Beste Bewertung", value: "-averageRating"},
  {title: "Kürzeste Zubereitungszeit", value: "prepTime"},
]

const sourceOptions = [
  {id: 1, name: 'HelloFresh', color: 'bg-lime-500 text-black'},
  {id: 2, name: 'KitchenStories', color: 'bg-yellow-500 text-black'},
  {id: 3, name: 'Chefkoch', color: 'bg-green-700 text-white'},
  {id: 4, name: 'Lecker', color: 'bg-pink-700 text-white'},
  {id: 5, name: 'EatSmarter', color: 'bg-orange-600 text-white'},
  {id: 6, name: 'Yazio', color: 'bg-pink-600 text-white'},
  {id: 7, name: 'Mob', color: 'bg-gray-600 text-white'},
]

const categoryOptions = [
  {value: 0, title: "Hauptgerichte"},
  {value: 1, title: "Frühstück"},
  {value: 2, title: "Dessert"},
  {value: 3, title: "Backen"},
  {value: 4, title: "Getränke"},
]

const difficultyOptions = [
  {value: 1, title: "Einfach"},
  {value: 2, title: "Mittel"},
  {value: 3, title: "Schwierig"},
]

const prepTimeOptions = [
  {value: "", title: "Egal"},
  {value: "15", title: "≤ 15 Min."},
  {value: "30", title: "≤ 30 Min."},
  {value: "60", title: "≤ 60 Min."},
]

let ordering = ref(null as string | null)
let recipeType = ref(null as number | null)
let sources = ref([] as number[])
let difficulty = ref(null as number | null)
let ratingGte = ref("0")
let prepTimeMinutes = ref("")
let favoritedOnly = ref(false)

const toggleSource = (id: number) => {
  const index = sources.value.indexOf(id)
  if (index === -1) sources.value.push(id)
  else sources.value.splice(index, 1)
}

const setRating = (stars: number) => {
  ratingGte.value = ratingGte.value === stars.toString() ? "0" : stars.toString()
}

const applyFilter = () => {
  recipeFilterRefs.calories_gt = sliders.value[0].value[0]
  recipeFilterRefs.calories_lt = sliders.value[0].value[1]
  recipeFilterRefs.protein_gt = sliders.value[1].value[0]
  recipeFilterRefs.protein_lt = sliders.value[1].value[1]
  recipeFilterRefs.carbs_gt = sliders.value[2].value[0]
  recipeFilterRefs.carbs_lt = sliders.value[2].value[1]
  recipeFilterRefs.fat_gt = sliders.value[3].value[0]
  recipeFilterRefs.fat_lt = sliders.value[3].value[1]
  recipeFilterRefs.recipeType = recipeType.value
  recipeFilterRefs.sources = sources.value
  recipeFilterRefs.ordering = ordering.value
  recipeFilterRefs.srch = searchString.value
  recipeFilterRefs.difficulty = difficulty.value
  recipeFilterRefs.rating_gte = ratingGte.value
  recipeFilterRefs.prep_time_minutes = prepTimeMinutes.value
  recipeFilterRefs.favorited = favoritedOnly.value

  recipeFilterRefs.page = "1"
}

const search = async () => {
  applyFilter()
  show.value = false
  await recipeStore.fetch_recipes(false)
}

const clearFilter = async () => {
  recipeFilterRefs.reset()
  // "favorited" is the page's identity (all recipes vs. the dedicated favorites page), not a
  // generic filter value, so clearing filters must not leave /Recipe/Favorites showing everything
  recipeFilterRefs.favorited = isFavoritePage
  updateComponentValues()
  show.value = false
  await recipeStore.fetch_recipes(false)
}

const updateComponentValues = () => {
  sliders.value[0].value = [recipeFilterRefs.calories_gt, recipeFilterRefs.calories_lt]
  sliders.value[1].value = [recipeFilterRefs.protein_gt, recipeFilterRefs.protein_lt]
  sliders.value[2].value = [recipeFilterRefs.carbs_gt, recipeFilterRefs.carbs_lt]
  sliders.value[3].value = [recipeFilterRefs.fat_gt, recipeFilterRefs.fat_lt]
  recipeType.value = recipeFilterRefs.recipeType
  sources.value = [...recipeFilterRefs.sources]
  ordering.value = recipeFilterRefs.ordering
  searchString.value = recipeFilterRefs.srch
  difficulty.value = recipeFilterRefs.difficulty
  ratingGte.value = recipeFilterRefs.rating_gte
  prepTimeMinutes.value = recipeFilterRefs.prep_time_minutes
  favoritedOnly.value = !!recipeFilterRefs.favorited
}

const sortBy = (key: string) => {
  ordering.value = key
  applyFilter()
  recipeStore.fetch_recipes(false)
  showSortPopup.value = false
}

// One-click toggle in the toolbar, outside the filter panel - applies immediately since
// favoriting is the single most common way people want to narrow this page down.
const toggleFavoritedQuick = async () => {
  recipeFilterRefs.favorited = !recipeFilterRefs.favorited
  favoritedOnly.value = !!recipeFilterRefs.favorited
  recipeFilterRefs.page = "1"
  await recipeStore.fetch_recipes(false)
}

updateComponentValues()
</script>

<template>

  <!-- Filter drawer -->
  <Transition name="drawer">
    <div v-if="show" class="fixed inset-0 z-50 flex justify-end" aria-modal="true" role="dialog">
      <div class="drawer-backdrop absolute inset-0 bg-black/60" @click="search()"></div>
      <div class="drawer-panel relative w-full sm:max-w-md h-full bg-gray-800 shadow-2xl flex flex-col">

        <div class="flex items-center justify-between px-5 py-4 border-b border-gray-700 shrink-0">
          <h2 class="text-lg font-semibold text-white">Filter</h2>
          <button @click="search()" aria-label="Schließen"
                  class="text-gray-400 hover:text-white p-1.5 rounded-lg hover:bg-gray-700">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"
                 xmlns="http://www.w3.org/2000/svg">
              <path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12"></path>
            </svg>
          </button>
        </div>

        <div class="flex-1 overflow-y-auto px-5 py-5 space-y-7">

          <!-- Favorites: intentionally the most prominent, first thing in the panel -->
          <button type="button" @click="favoritedOnly = !favoritedOnly"
                  class="w-full flex items-center justify-between p-4 rounded-xl border-2 transition"
                  :class="favoritedOnly ? 'border-red-500 bg-red-500/10' : 'border-gray-700 bg-gray-900/40 hover:border-gray-600'">
            <span class="flex items-center gap-3">
              <svg class="w-7 h-7" :class="favoritedOnly ? 'text-red-500' : 'text-gray-400'"
                   :fill="favoritedOnly ? 'currentColor' : 'none'" stroke="currentColor" stroke-width="1.5"
                   viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                <path
                    d="M11.645 20.91l-.007-.003-.022-.012a15.247 15.247 0 01-.383-.218 25.18 25.18 0 01-4.244-3.17C4.688 15.36 2.25 12.174 2.25 8.25 2.25 5.322 4.714 3 7.688 3A5.5 5.5 0 0112 5.052 5.5 5.5 0 0116.313 3c2.973 0 5.437 2.322 5.437 5.25 0 3.925-2.438 7.111-4.739 9.256a25.175 25.175 0 01-4.244 3.17 15.247 15.247 0 01-.383.219l-.022.012-.007.004-.003.001a.752.752 0 01-.704 0l-.003-.001z"
                    stroke-linecap="round" stroke-linejoin="round"></path>
              </svg>
              <span class="text-left">
                <span class="block text-white font-medium">Nur Favoriten</span>
                <span class="block text-xs text-gray-400">Zeige ausschließlich deine favorisierten Rezepte</span>
              </span>
            </span>
            <span class="relative inline-block w-11 h-6 rounded-full transition shrink-0"
                  :class="favoritedOnly ? 'bg-red-500' : 'bg-gray-600'">
              <span class="absolute top-0.5 left-0.5 w-5 h-5 bg-white rounded-full transition"
                    :class="{'translate-x-5': favoritedOnly}"></span>
            </span>
          </button>

          <!-- Quelle -->
          <div>
            <h3 class="text-sm font-semibold text-white mb-3">Quelle</h3>
            <div class="flex flex-wrap gap-2">
              <button v-for="source in sourceOptions" :key="source.id" type="button"
                      @click="toggleSource(source.id)"
                      class="px-3 py-1.5 rounded-full text-sm font-medium transition"
                      :class="sources.includes(source.id) ? source.color + ' ring-2 ring-white/70' : 'bg-gray-700 text-gray-300 hover:bg-gray-600'">
                {{ source.name }}
              </button>
            </div>
          </div>

          <!-- Menüart -->
          <div>
            <h3 class="text-sm font-semibold text-white mb-3">Menüart</h3>
            <div class="flex flex-wrap gap-2">
              <button v-for="category in categoryOptions" :key="category.value" type="button"
                      @click="recipeType = recipeType === category.value ? null : category.value"
                      class="px-3 py-1.5 rounded-full text-sm font-medium transition"
                      :class="recipeType === category.value ? 'bg-blue-600 text-white' : 'bg-gray-700 text-gray-300 hover:bg-gray-600'">
                {{ category.title }}
              </button>
            </div>
          </div>

          <!-- Schwierigkeit -->
          <div>
            <h3 class="text-sm font-semibold text-white mb-3">Schwierigkeit</h3>
            <div class="flex flex-wrap gap-2">
              <button v-for="option in difficultyOptions" :key="option.value" type="button"
                      @click="difficulty = difficulty === option.value ? null : option.value"
                      class="px-3 py-1.5 rounded-full text-sm font-medium transition"
                      :class="difficulty === option.value ? 'bg-blue-600 text-white' : 'bg-gray-700 text-gray-300 hover:bg-gray-600'">
                {{ option.title }}
              </button>
            </div>
          </div>

          <!-- Bewertung -->
          <div>
            <h3 class="text-sm font-semibold text-white mb-3">Mindestbewertung</h3>
            <div class="flex items-center gap-1">
              <button v-for="star in [1,2,3,4,5]" :key="star" type="button" @click="setRating(star)"
                      class="p-0.5" :aria-label="`Mindestens ${star} Sterne`">
                <svg class="w-7 h-7" :class="star <= parseInt(ratingGte) ? 'text-yellow-400' : 'text-gray-600'"
                     fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg">
                  <path
                      d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"></path>
                </svg>
              </button>
              <span class="ml-2 text-sm text-gray-400">{{ ratingGte === "0" ? "Egal" : `${ratingGte}+ Sterne` }}</span>
            </div>
          </div>

          <!-- Zubereitungszeit -->
          <div>
            <h3 class="text-sm font-semibold text-white mb-3">Zubereitungszeit</h3>
            <div class="flex flex-wrap gap-2">
              <button v-for="option in prepTimeOptions" :key="option.value" type="button"
                      @click="prepTimeMinutes = option.value"
                      class="px-3 py-1.5 rounded-full text-sm font-medium transition"
                      :class="prepTimeMinutes === option.value ? 'bg-blue-600 text-white' : 'bg-gray-700 text-gray-300 hover:bg-gray-600'">
                {{ option.title }}
              </button>
            </div>
          </div>

          <!-- Nährwerte (collapsible: heavier UI, less frequently used) -->
          <div>
            <button type="button" @click="showNutrients = !showNutrients"
                    class="flex items-center justify-between w-full text-sm font-semibold text-white mb-3">
              Nährwerte
              <svg class="w-5 h-5 text-gray-400 transition" :class="{'rotate-180': showNutrients}"
                   fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg">
                <path fill-rule="evenodd"
                      d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z"
                      clip-rule="evenodd"></path>
              </svg>
            </button>
            <div v-if="showNutrients" class="space-y-4">
              <div v-for="slider in sliders" class="mb-4">
                <div class="flex items-center mb-2 justify-between">
                  <p v-text="slider.title" class="mr-4 text-sm font-medium text-gray-300"></p>
                  <div class="flex items-center text-sm text-white">
                    <span v-text="slider.value[0]"></span>
                    <span class="mx-1">–</span>
                    <span v-text="slider.value[1]"></span>
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

        <div class="px-5 py-4 border-t border-gray-700 shrink-0 flex gap-3">
          <button @click="clearFilter()"
                  class="flex-1 px-4 py-2.5 bg-gray-700 hover:bg-gray-600 text-white text-sm font-medium rounded-lg">
            Zurücksetzen
          </button>
          <button @click="search()"
                  class="flex-1 px-4 py-2.5 bg-blue-600 hover:bg-blue-700 text-white text-sm font-medium rounded-lg">
            Anwenden
          </button>
        </div>
      </div>
    </div>
  </Transition>

  <!-- Toolbar -->
  <div class="flex flex-wrap items-center gap-3">
    <button @click="show = true"
            class="relative inline-flex items-center px-4 py-2 text-sm font-medium rounded-lg border border-gray-600 bg-gray-900 text-white hover:bg-gray-700">
      <svg class="w-5 h-5 mr-2 text-gray-400" aria-hidden="true" fill="currentColor"
           viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
        <path clip-rule="evenodd"
              d="M2.628 1.601C5.028 1.206 7.49 1 10 1s4.973.206 7.372.601a.75.75 0 01.628.74v2.288a2.25 2.25 0 01-.659 1.59l-4.682 4.683a2.25 2.25 0 00-.659 1.59v3.037c0 .684-.31 1.33-.844 1.757l-1.937 1.55A.75.75 0 018 18.25v-5.757a2.25 2.25 0 00-.659-1.591L2.659 6.22A2.25 2.25 0 012 4.629V2.34a.75.75 0 01.628-.74z"
              fill-rule="evenodd"></path>
      </svg>
      Filter
      <span v-if="recipeFilterRefs.active_filter_count > 0"
            class="ml-2 inline-flex items-center justify-center w-5 h-5 text-xs font-bold text-white bg-blue-600 rounded-full"
            v-text="recipeFilterRefs.active_filter_count"></span>
    </button>

    <button v-if="recipeFilterRefs.active_filter_count > 0" @click="clearFilter()" title="Filter zurücksetzen"
            class="inline-flex items-center px-3 py-2 text-sm font-medium rounded-lg border border-gray-600 bg-gray-900 text-gray-300 hover:bg-gray-700 hover:text-white">
      <svg class="w-5 h-5" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"
           xmlns="http://www.w3.org/2000/svg">
        <path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12"></path>
      </svg>
    </button>

    <button @click="toggleFavoritedQuick()" title="Nur Favoriten"
            class="inline-flex items-center px-3 py-2 text-sm font-medium rounded-lg border transition"
            :class="favoritedOnly ? 'border-red-500 bg-red-500/10 text-red-400' : 'border-gray-600 bg-gray-900 text-gray-300 hover:bg-gray-700'">
      <svg class="w-5 h-5" :fill="favoritedOnly ? 'currentColor' : 'none'" stroke="currentColor" stroke-width="1.5"
           viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
        <path
            d="M11.645 20.91l-.007-.003-.022-.012a15.247 15.247 0 01-.383-.218 25.18 25.18 0 01-4.244-3.17C4.688 15.36 2.25 12.174 2.25 8.25 2.25 5.322 4.714 3 7.688 3A5.5 5.5 0 0112 5.052 5.5 5.5 0 0116.313 3c2.973 0 5.437 2.322 5.437 5.25 0 3.925-2.438 7.111-4.739 9.256a25.175 25.175 0 01-4.244 3.17 15.247 15.247 0 01-.383.219l-.022.012-.007.004-.003.001a.752.752 0 01-.704 0l-.003-.001z"
            stroke-linecap="round" stroke-linejoin="round"></path>
      </svg>
    </button>

    <div class="relative flex-1 min-w-[220px]">
      <div class="absolute inset-y-0 left-0 flex items-center pl-3 pointer-events-none">
        <svg aria-hidden="true" class="w-5 h-5 text-gray-400" fill="none"
             stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path>
        </svg>
      </div>
      <input type="search" id="default-search" @keyup.enter="search()"
             v-model="searchString"
             class="block w-full p-2.5 pl-10 text-sm border rounded-lg bg-gray-700 border-gray-600 placeholder-gray-400 text-white focus:ring-blue-500 focus:border-blue-500"
             placeholder="Rezeptname suchen">
    </div>
    <button type="button" @click="search()"
            class="text-white focus:ring-4 focus:outline-none font-medium rounded-lg text-sm px-4 py-2.5 bg-blue-600 hover:bg-blue-700 focus:ring-blue-800">
      Suche
    </button>
    <OnClickOutside @trigger="showSortPopup = false">
      <div class="relative inline-block text-left">
        <div>
          <button type="button"
                  @click="showSortPopup = !showSortPopup"
                  class="inline-flex items-center px-4 py-2 text-sm font-medium rounded-lg border border-gray-600 bg-gray-900 text-white hover:bg-gray-700"
                  id="sort-menu" aria-expanded="false" aria-haspopup="true">
            <svg class="w-4 h-4 mr-2 text-gray-400" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20"
                 fill="currentColor" aria-hidden="true">
              <path fill-rule="evenodd"
                    d="M2.75 4.5a.75.75 0 000 1.5h9.5a.75.75 0 000-1.5h-9.5zm0 5a.75.75 0 000 1.5h5.5a.75.75 0 000-1.5h-5.5zm0 5a.75.75 0 000 1.5h2.5a.75.75 0 000-1.5h-2.5zm11-9.19l1.72 1.72a.75.75 0 101.06-1.06l-3-3a.75.75 0 00-1.06 0l-3 3a.75.75 0 101.06 1.06l1.72-1.72V16.5a.75.75 0 001.5 0V5.31z"
                    clip-rule="evenodd"/>
            </svg>
            Sortieren
            <svg class="w-4 h-4 ml-2 -mr-1" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20"
                 fill="currentColor" aria-hidden="true">
              <path fill-rule="evenodd"
                    d="M10 18a8 8 0 100-16 8 8 0 000 16zm0-2a6 6 0 100-12 6 6 0 000 12zm-1-5a1 1 0 112 0v1h1a1 1 0 110 2h-1v1a1 1 0 11-2 0v-1H8a1 1 0 110-2h1v-1z"
                    clip-rule="evenodd"/>
            </svg>
          </button>
        </div>
        <div v-if="showSortPopup" class="origin-top-right absolute right-0 mt-2 w-56 rounded-md shadow-lg bg-white ring-1 ring-black
            ring-opacity-5"
             role="menu" aria-orientation="vertical" aria-labelledby="sort-menu">
          <div class="py-1" role="none">
            <button v-for="option in orderings" :key="option.value"
                    @click="sortBy(option.value)"
                    class="w-full block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 hover:text-gray-900"
                    role="menuitem">{{ option.title }}
            </button>
          </div>
        </div>
      </div>
    </OnClickOutside>
  </div>

</template>

<style src="@vueform/slider/themes/default.css"></style>
<style scoped>
.drawer-enter-active,
.drawer-leave-active {
  transition: opacity 0.2s ease;
}

.drawer-enter-from,
.drawer-leave-to {
  opacity: 0;
}

.drawer-enter-active .drawer-panel,
.drawer-leave-active .drawer-panel {
  transition: transform 0.25s ease;
}

.drawer-enter-from .drawer-panel,
.drawer-leave-to .drawer-panel {
  transform: translateX(100%);
}
</style>
