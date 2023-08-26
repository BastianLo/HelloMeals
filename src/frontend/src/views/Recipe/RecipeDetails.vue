<template>
  <div class="bg-gray-800">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div class="grid grid-cols-1 md:grid-cols-2 gap-8">
        <div>
          <h1 class="text-3xl font-semibold text-white mb-4" v-text="recipeStore.detailRecipe.name"></h1>
          <p class="text-base text-gray-400" v-text="recipeStore.detailRecipe.headline"></p>
          <!-- Top menu buttons -->
          <div class="flex items-center gap-2">
            <button class="action-button"
                    @click="recipeStore.favorite_recipe_value(recipeStore.detailRecipe.helloFreshId, !recipeStore.detailRecipe.favorited); recipeStore.fetch_recipes_detail(recipeId as string, false)">
              <svg v-if="recipeStore.detailRecipe.favorited" class="w-8 h-8 text-red-400 button-icon"
                   aria-hidden="true"
                   fill="currentColor" viewBox="0 0 24 24"
                   xmlns="http://www.w3.org/2000/svg">
                <path
                    d="M11.645 20.91l-.007-.003-.022-.012a15.247 15.247 0 01-.383-.218 25.18 25.18 0 01-4.244-3.17C4.688 15.36 2.25 12.174 2.25 8.25 2.25 5.322 4.714 3 7.688 3A5.5 5.5 0 0112 5.052 5.5 5.5 0 0116.313 3c2.973 0 5.437 2.322 5.437 5.25 0 3.925-2.438 7.111-4.739 9.256a25.175 25.175 0 01-4.244 3.17 15.247 15.247 0 01-.383.219l-.022.012-.007.004-.003.001a.752.752 0 01-.704 0l-.003-.001z"></path>
              </svg>
              <svg v-if="!recipeStore.detailRecipe.favorited"
                   class="w-8 h-8 text-red-400 button-icon"
                   aria-hidden="true" fill="none"
                   stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24"
                   xmlns="http://www.w3.org/2000/svg">
                <path
                    d="M21 8.25c0-2.485-2.099-4.5-4.688-4.5-1.935 0-3.597 1.126-4.312 2.733-.715-1.607-2.377-2.733-4.313-2.733C5.1 3.75 3 5.765 3 8.25c0 7.22 9 12 9 12s9-4.78 9-12z"
                    stroke-linecap="round" stroke-linejoin="round"></path>
              </svg>
            </button>
            <button @click="share()" class="action-button">
              <svg aria-hidden="true" fill="none" stroke="currentColor" stroke-width="1.5"
                   viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"
                   class="inline-block w-8 h-8 mr-1 text-white button-icon">
                <path
                    d="M7.217 10.907a2.25 2.25 0 100 2.186m0-2.186c.18.324.283.696.283 1.093s-.103.77-.283 1.093m0-2.186l9.566-5.314m-9.566 7.5l9.566 5.314m0 0a2.25 2.25 0 103.935 2.186 2.25 2.25 0 00-3.935-2.186zm0-12.814a2.25 2.25 0 103.933-2.185 2.25 2.25 0 00-3.933 2.185z"
                    stroke-linecap="round" stroke-linejoin="round"></path>
              </svg>
            </button>
            <div v-show="showAlert"
                 class="fixed inset-x-0 top-4 flex items-center justify-center">
              <div
                  class="flex p-4 mb-4 text-sm border rounded-lg bg-gray-800 text-green-400 border-green-800"
                  role="alert">
                <svg aria-hidden="true" class="flex-shrink-0 inline w-5 h-5 mr-3" fill="currentColor"
                     viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg">
                  <path fill-rule="evenodd"
                        d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z"
                        clip-rule="evenodd"></path>
                </svg>
                <span class="sr-only">Info</span>
                <div>
                  <span class="font-medium">Link kopiert!</span> Der Link zum Rezept wurde in die
                  Zwischenablage kopiert
                </div>
                <button type="button" @click="showAlert= false"
                        class="ml-2 flex-shrink-0 p-1 transition duration-300 ease-in-out rounded-full focus:outline-none focus:ring-2 hover:bg-red-800 focus:ring-red-500">
                  <span class="sr-only">Dismiss</span>
                  <svg aria-hidden="true" class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20"
                       xmlns="http://www.w3.org/2000/svg">
                    <path fill-rule="evenodd"
                          d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z"
                          clip-rule="evenodd"></path>
                  </svg>
                </button>
              </div>
            </div>
            <a class="action-button" v-if="recipeStore.detailRecipe.websiteLink !== null"
               :href="recipeStore.detailRecipe.websiteLink"
               target="_blank" rel="noopener noreferrer">
              <svg aria-hidden="true" fill="none" stroke="currentColor" stroke-width="1.5"
                   viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"
                   class="inline-block w-8 h-8 text-white button-icon">
                <path
                    d="M13.19 8.688a4.5 4.5 0 011.242 7.244l-4.5 4.5a4.5 4.5 0 01-6.364-6.364l1.757-1.757m13.35-.622l1.757-1.757a4.5 4.5 0 00-6.364-6.364l-4.5 4.5a4.5 4.5 0 001.242 7.244"
                    stroke-linecap="round" stroke-linejoin="round"></path>
              </svg>
            </a>
            <a class="action-button" v-if="recipeStore.detailRecipe.cardLink !== null"
               :href="recipeStore.detailRecipe.cardLink"
               target="_blank" rel="noopener noreferrer">
              <svg aria-hidden="true" fill="none" stroke="currentColor" stroke-width="1.5"
                   viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"
                   class="inline-block w-8 h-8 text-white">
                <path
                    d="M6.72 13.829c-.24.03-.48.062-.72.096m.72-.096a42.415 42.415 0 0110.56 0m-10.56 0L6.34 18m10.94-4.171c.24.03.48.062.72.096m-.72-.096L17.66 18m0 0l.229 2.523a1.125 1.125 0 01-1.12 1.227H7.231c-.662 0-1.18-.568-1.12-1.227L6.34 18m11.318 0h1.091A2.25 2.25 0 0021 15.75V9.456c0-1.081-.768-2.015-1.837-2.175a48.055 48.055 0 00-1.913-.247M6.34 18H5.25A2.25 2.25 0 013 15.75V9.456c0-1.081.768-2.015 1.837-2.175a48.041 48.041 0 011.913-.247m10.5 0a48.536 48.536 0 00-10.5 0m10.5 0V3.375c0-.621-.504-1.125-1.125-1.125h-8.25c-.621 0-1.125.504-1.125 1.125v3.659M18 10.5h.008v.008H18V10.5zm-3 0h.008v.008H15V10.5z"
                    stroke-linecap="round" stroke-linejoin="round"></path>
              </svg>
            </a>
          </div>

          <div class="mb-2 flex items-center">
            <span v-if="recipeStore.detailRecipe.totalTime"
                  class="text-xs font-medium inline-flex items-center px-2.5 py-0.5 rounded mr-2 bg-gray-700 text-gray-400 border border-gray-500">
                  <svg aria-hidden="true" class="w-3 h-3 mr-1" fill="currentColor"
                       viewBox="0 0 20 20"
                       xmlns="http://www.w3.org/2000/svg">
                    <path fill-rule="evenodd"
                          d="M10 18a8 8 0 100-16 8 8 0 000 16zm1-12a1 1 0 10-2 0v4a1 1 0 00.293.707l2.828 2.829a1 1 0 101.415-1.415L11 9.586V6z"
                          clip-rule="evenodd"></path>
                  </svg>
              <span v-text="recipeStore.detailRecipe.totalTime"></span>
            </span>
            <span v-if="recipeStore.detailRecipe.prepTime"
                  class="text-xs font-medium inline-flex items-center px-2.5 py-0.5 rounded bg-gray-700 text-blue-400 border border-blue-400">
                        <svg aria-hidden="true" class="w-3 h-3 mr-1" fill="currentColor"
                             viewBox="0 0 20 20"
                             xmlns="http://www.w3.org/2000/svg">
                          <path fill-rule="evenodd"
                                d="M10 18a8 8 0 100-16 8 8 0 000 16zm1-12a1 1 0 10-2 0v4a1 1 0 00.293.707l2.828 2.829a1 1 0 101.415-1.415L11 9.586V6z"
                                clip-rule="evenodd"></path>
                        </svg>
                    <span v-text="recipeStore.detailRecipe.prepTime"></span>
                  </span>
            <div v-if="recipeStore.detailRecipe.difficulty">
                  <span v-if="recipeStore.detailRecipe.difficulty === 1"
                        class="ml-2 text-xs font-medium mr-2 px-2.5 py-0.5 rounded bg-green-900 text-green-300">Einfach</span>
              <span v-if="recipeStore.detailRecipe.difficulty === 2"
                    class="ml-2 text-xs font-medium mr-2 px-2.5 py-0.5 rounded bg-yellow-900 text-yellow-300">Mittel</span>
              <span v-if="recipeStore.detailRecipe.difficulty === 3"
                    class="ml-2 text-xs font-medium mr-2 px-2.5 py-0.5 rounded bg-red-900 text-red-300">Schwierig</span>
            </div>
          </div>
          <p class="text-sm text-white mb-4" v-text="recipeStore.detailRecipe.description"></p>
          <div class="mb-4 grid grid-cols-3 max-sm:grid-cols-2 gap-4" v-if="recipeStore.detailRecipe.nutrients">
            <div
                :class="{'bg-green-200': recipeStore.detailRecipe.nutrients.energyKcal < 600, 'bg-orange-200': recipeStore.detailRecipe.nutrients.energyKcal > 600 && recipeStore.detailRecipe.nutrients.energyKcal <  800, 'bg-red-200': recipeStore.detailRecipe.nutrients.energyKcal >= 800}"
                class="p-4 rounded-lg" v-if="recipeStore.detailRecipe.nutrients.energyKcal">
              <p class="text-sm font-semibold mb-2">Energie:</p>
              <p class="text-lg">{{ recipeStore.detailRecipe.nutrients.energyKcal }} kcal</p>
            </div>
            <div
                :class="{'bg-green-200': nutrientDensities.carbs < 0.07, 'bg-orange-200': nutrientDensities.carbs >= 0.07 && nutrientDensities.carbs < 0.12 , 'bg-red-200': nutrientDensities.carbs >= 0.12}"
                class="p-4 rounded-lg" v-if="recipeStore.detailRecipe.nutrients.carbs">
              <p class="text-sm font-semibold mb-2">Kohlenhydrate:</p>
              <p class="text-lg">{{ recipeStore.detailRecipe.nutrients.carbs }} g</p>
            </div>
            <div
                :class="{'bg-green-200': nutrientDensities.protein > 0.07, 'bg-orange-200': nutrientDensities.protein <= 0.07 && nutrientDensities.protein > 0.04 , 'bg-red-200': nutrientDensities.protein <= 0.04}"
                class="p-4 rounded-lg" v-if="recipeStore.detailRecipe.nutrients.protein">
              <p class="text-sm font-semibold mb-2">Protein:</p>
              <p class="text-lg">{{ recipeStore.detailRecipe.nutrients.protein }} g</p>
            </div>
            <div
                :class="{'bg-green-200': nutrientDensities.fat < 0.07, 'bg-orange-200': nutrientDensities.fat >= 0.07 && nutrientDensities.fat < 0.12 , 'bg-red-200': nutrientDensities.fat >= 0.12}"
                class="p-4 rounded-lg" v-if="recipeStore.detailRecipe.nutrients.fat">
              <p class="text-sm font-semibold mb-2">Fett:</p>
              <p class="text-lg">{{ recipeStore.detailRecipe.nutrients.fat }} g</p>
            </div>
            <div
                :class="{'bg-green-200': nutrientDensities.sugar < 0.05, 'bg-orange-200': nutrientDensities.sugar >= 0.05 && nutrientDensities.sugar < 0.1 , 'bg-red-200': nutrientDensities.sugar >= 0.1}"
                class="p-4 rounded-lg" v-if="recipeStore.detailRecipe.nutrients.sugar">
              <p class="text-sm font-semibold mb-2">Zucker:</p>
              <p class="text-lg">{{ recipeStore.detailRecipe.nutrients.sugar }} g</p>
            </div>
            <div
                :class="{'bg-green-200': nutrientDensities.salt < 0.002, 'bg-orange-200': nutrientDensities.salt >= 0.002 && nutrientDensities.salt < 0.004 , 'bg-red-200': nutrientDensities.salt >= 0.004}"
                class="p-4 rounded-lg" v-if="recipeStore.detailRecipe.nutrients.salt">
              <p class="text-sm font-semibold mb-2">Salz:</p>
              <p class="text-lg">{{ recipeStore.detailRecipe.nutrients.salt }} g</p>
            </div>
          </div>
          <div class="mb-4 flex flex-wrap">
            <span v-for="utensil in recipeStore.detailRecipe.utensils"
                  class=" text-xs font-medium mr-2 mb-2 px-2.5 py-0.5 rounded bg-green-900 text-green-300"
                  v-text="utensil.utensil.name" style="white-space: nowrap;"></span>
          </div>
          <div class="mb-4">
            <img class="w-full" v-if="recipeStore.detailRecipe.image" :src="recipeStore.detailRecipe.image"
                 alt="Recipe Image">
          </div>
        </div>
        <div>
          <div>
            <h2 class="text-2xl font-semibold text-white mb-4">Zutaten</h2>
            <div class="mt-1">
              <div class="flex items-center mb-4">
                <label for="servings"
                       class="text-white mr-2">Portionen:</label>
                <input type="number" id="servings" min="1" step="1"
                       class="w-16 py-1 px-2 border border-gray-300 rounded text-white bg-gray-800 focus:outline-none focus:ring-2 focus:ring-blue-500"
                       v-model="servings">
              </div>
            </div>
            <div v-for="group in recipeStore.detailRecipe.ingredient_groups">
              <div v-if="group.ingredients.length > 0">
                <h3 class="text-lg font-semibold text-white mb-2" v-text="group.name"></h3>
                <div class="overflow-x-auto">
                  <table class="table-auto border-collapse">
                    <tbody>
                    <tr v-for="ingredient in group.ingredients" class="odd:bg-slate-700">
                      <td>
                        <button
                            class="mt-2 flex items-center justify-center w-8 h-8 border border-gray-500 rounded-full">
                          <svg v-if="ingredient.ingredient.available" class="w-6 h-6 text-green-500" aria-hidden="true"
                               fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg">
                            <path d="M10 18a8 8 0 100-16 8 8 0 000 16zm-3-9l2 2 5-5"></path>
                          </svg>
                          <svg v-else class="w-6 h-6 text-gray-500" aria-hidden="true"
                               fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg">
                            <path d="M10 18a8 8 0 100-16 8 8 0 000 16zm-3-9l2 2 5-5"></path>
                          </svg>
                        </button>
                      </td>
                      <td class="px-2 py-2 text-white max-w-xs"
                          v-if="recipeStore.detailRecipe.servings"
                          v-text="ingredient.amount > 0 ? Math.round(ingredient.amount / recipeStore.detailRecipe.servings * servings*100)/100 : ''"></td>
                      <td class="px-4 py-2 text-white"
                          v-text="ingredient.unit"></td>
                      <td class="">
                        <div class="h-max px-4 py-2 text-white break-all flex items-center">
                          <span
                              class="flex-grow"
                              v-text="ingredient.ingredient.name"></span>
                        </div>
                      </td>
                    </tr>
                    </tbody>
                  </table>
                </div>
              </div>

            </div>
          </div>
        </div>
      </div>
      <div class="mt-14">
        <h2 class="text-2xl font-semibold text-white mb-4">Arbeitsschritte</h2>
        <hr class="mb-8 border-gray-300">
        <div class="work-steps-container bg-gray-800 p-4 rounded-lg">
          <div class="list-decimal list-inside text-white">
            <div v-for="(step, index) in recipeStore.detailRecipe.work_steps" class="mb-8">
              <div class="flex items-start">
                <template v-if="recipeStore.detailRecipe.work_steps.length > 1">
                  <div x-data="{ completed: false }"
                       @click="completed[index] = !completed[index]"
                       class="cursor-pointer flex-shrink-0 w-8 h-8 text-white font-semibold rounded-full flex items-center justify-center"
                       :class="{'bg-blue-500': !completed[index], 'bg-green-500': completed[index]}">
                    <span v-text="index + 1"></span>
                  </div>
                </template>
                <div class="ml-3">
                        <span class=" ml-1"
                              :class="{'text-white': !completed[index], 'text-gray-500': completed[index]}"
                              v-html="step.description.replace('\n', '<br>').replace('\r', '<br>')"></span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>

  <RefreshSwiper @refresh="load()"/>
</template>

<script setup lang="ts">
import {useRouter} from "vue-router";
import {useRecipeStore} from "@/stores/RecipeStore";
import {computed, ref, watch} from "vue";
import AlertBannerType, {useAlertBannerStore} from "@/stores/AlertBannerStore";
import RefreshSwiper from "@/components/common/RefreshSwiper.vue";

let recipeStore = useRecipeStore()

const recipeId = useRouter().currentRoute.value.params.id


const servings = ref(0)

const showAlert = ref(false)
const completed = ref([] as boolean[])

window.scrollTo({top: 0});
const load = () => {
  recipeStore.fetch_recipes_detail(recipeId as string)
}
load()
const share = () => {
  try {
    navigator.share({title: recipeStore.detailRecipe.name, url: location.href})
  } catch (e) {
    useAlertBannerStore().showBanner(AlertBannerType.SUCCESS, "Link kopiert!", "Der Link zum Rezept wurde in die Zwischenablage kopiert.")
    navigator.clipboard.writeText(location.href);
  }
}
watch(() => recipeStore.detailRecipe, (newDetailRecipe) => {
  if (newDetailRecipe) {
    servings.value = newDetailRecipe.servings || 0;
  }
});

const nutrientDensities = computed(() => {
  const nutrients = recipeStore.detailRecipe.nutrients;
  if (nutrients.energyKcal === null) {
    nutrients.energyKcal = 0
  }
  return {
    carbs: nutrients.carbs ? (nutrients.carbs / nutrients.energyKcal) : 0,
    protein: nutrients.protein ? (nutrients.protein / nutrients.energyKcal) : 0,
    fat: nutrients.fat ? (nutrients.fat / nutrients.energyKcal) : 0,
    sugar: nutrients.sugar ? (nutrients.sugar / nutrients.energyKcal) : 0,
    salt: nutrients.salt ? (nutrients.salt / nutrients.energyKcal) : 0,
  };
});
</script>
<style>
</style>