<script setup lang="ts">
import {useIngredientStore} from "@/stores/IngredientStore";
import {ref} from "vue";

const store = useIngredientStore()


const show = ref(false)
const mergeDialog = ref(false)
const targetSearchString = ref('')
const targetIngredient = ref('')

const overviewSearchString = ref('')
const sourceIngredients = ref([] as string[])

const mergeIngredients = async () => {
  await store.assignIngredients(sourceIngredients.value, targetIngredient.value)
  await store.fetchIngredients()
  sourceIngredients.value = []
}

const load = () => {
  store.fetchIngredients()
  store.fetchTargetIngredients()
}
load()

</script>

<template>
  <div>
    <div @mouseover="show = true" @mouseleave="show = false" data-dial-init
         class="fixed right-6 bottom-6 group mb-16">
      <div :class="{ 'hidden': !show }" id="speed-dial-menu-text-inside-button-square"
           class="flex flex-col items-center mb-4 space-y-2">
        <button @click="mergeDialog=true"
                class="w-[56px] h-[56px] text-gray-500 bg-white rounded-lg border border-gray-200 hover:text-gray-900 dark:border-gray-600 shadow-sm dark:hover:text-white dark:text-gray-400 hover:bg-gray-50 dark:bg-gray-700 dark:hover:bg-gray-600 focus:ring-4 focus:ring-gray-300 focus:outline-none dark:focus:ring-gray-400">
          <svg class="w-6 h-6 mx-auto mt-px" aria-hidden="true" fill="none" stroke="currentColor"
               stroke-width="1.5" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
            <path
                d="M15.75 17.25v3.375c0 .621-.504 1.125-1.125 1.125h-9.75a1.125 1.125 0 01-1.125-1.125V7.875c0-.621.504-1.125 1.125-1.125H6.75a9.06 9.06 0 011.5.124m7.5 10.376h3.375c.621 0 1.125-.504 1.125-1.125V11.25c0-4.46-3.243-8.161-7.5-8.876a9.06 9.06 0 00-1.5-.124H9.375c-.621 0-1.125.504-1.125 1.125v3.5m7.5 10.375H9.375a1.125 1.125 0 01-1.125-1.125v-9.25m12 6.625v-1.875a3.375 3.375 0 00-3.375-3.375h-1.5a1.125 1.125 0 01-1.125-1.125v-1.5a3.375 3.375 0 00-3.375-3.375H9.75"
                stroke-linecap="round" stroke-linejoin="round"></path>
          </svg>
          <span class="block mb-px text-xs font-medium">Mergen</span>
        </button>

      </div>
      <button @click="show = !show"
              class="flex items-center justify-center text-white bg-blue-700 rounded-lg w-14 h-14 hover:bg-blue-800 dark:bg-blue-600 dark:hover:bg-blue-700 focus:ring-4 focus:ring-blue-300 focus:outline-none dark:focus:ring-blue-800">
        <svg aria-hidden="true" class="w-8 h-8 transition-transform group-hover:rotate-45" fill="none"
             stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                d="M12 6v6m0 0v6m0-6h6m-6 0H6"></path>
        </svg>
        <span class="sr-only">Open actions menu</span>
      </button>
    </div>


    <!-- Merge Dialog -->
    <div :class="{ 'hidden': !mergeDialog }"
         id="medium-modal"
         tabindex="-1"
         class=" bg-gray-500 bg-opacity-75 flex justify-center fixed top-0 left-0 right-0 z-50 w-full p-4 overflow-x-hidden overflow-y-auto md:inset-0 h-[calc(100%-1rem)] max-h-full">
      <div class="relative w-full max-w-lg max-h-full">
        <!-- Modal content -->
        <div class="mb-24 relative bg-white rounded-lg shadow dark:bg-gray-700"
        >
          <!-- Modal header -->
          <div class="flex items-center justify-between p-5 border-b rounded-t dark:border-gray-600">
            <h3 class="text-xl font-medium text-gray-900 dark:text-white">
              Gruppieren in
            </h3>
            <button @click="mergeDialog = false"
                    class="text-gray-400 bg-transparent hover:bg-gray-200 hover:text-gray-900 rounded-lg text-sm p-1.5 ml-auto inline-flex items-center dark:hover:bg-gray-600 dark:hover:text-white"
                    data-modal-hide="medium-modal">
              <svg aria-hidden="true" class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20"
                   xmlns="http://www.w3.org/2000/svg">
                <path fill-rule="evenodd"
                      d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z"
                      clip-rule="evenodd"></path>
              </svg>
              <span class="sr-only">Close modal</span>
            </button>
          </div>
          <!-- Modal body -->
          <label for="default-search"
                 class="mb-2 text-sm font-medium text-gray-900 sr-only dark:text-white">Search</label>
          <div class="relative p-6 flex-grow overflow-y-auto">
            <div class="absolute inset-y-0 left-0 flex items-center pl-3 pointer-events-none">
              <svg aria-hidden="true" class="w-5 h-5 text-gray-500 dark:text-gray-400" fill="none"
                   stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                      d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path>
              </svg>
            </div>
            <input type="search" v-model="targetSearchString"
                   @keypress="store.fetchTargetIngredients(targetSearchString)"
                   class="block w-full p-4 pl-10 text-sm text-gray-900 border border-gray-300 rounded-lg bg-gray-50 focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
                   placeholder="Tag Group Name" required>
          </div>
          <!-- navbar -->
          <div class="flex pt-6 flex-col items-center">
                <span class="text-sm text-gray-700 dark:text-gray-400">
                  Zeige <span class="font-semibold text-gray-900 dark:text-white"
                              v-text="store.targetNav.start"></span>
                    bis
                    <span
                        class="font-semibold text-gray-900 dark:text-white"
                        v-text="store.targetNav.end"></span> von
                    <span
                        class="font-semibold text-gray-900 dark:text-white"
                        v-text="store.targetNav.count"></span>
                    Einträgen
                </span>
            <div class="inline-flex mt-2 xs:mt-0">
              <button @click="store.targetPrevious()"
                      class="px-4 py-2 text-sm font-medium text-white bg-gray-800 rounded-l hover:bg-gray-900 dark:bg-gray-800 dark:border-gray-700 dark:text-gray-400 dark:hover:bg-gray-700 dark:hover:text-white">
                Zurück
              </button>
              <button @click="store.targetNext()"
                      class="px-4 py-2 text-sm font-medium text-white bg-gray-800 border-0 border-l border-gray-700 rounded-r hover:bg-gray-900 dark:bg-gray-800 dark:border-gray-700 dark:text-gray-400 dark:hover:bg-gray-700 dark:hover:text-white">
                Weiter
              </button>
            </div>
          </div>
          <div class="p-6">
            <div v-for="ingr in store.targetIngredients" :key="ingr.helloFreshId">
              <div v-if="!sourceIngredients.includes(ingr.helloFreshId)">
                <div>
                  <input v-model="targetIngredient" type="radio" :value="ingr.helloFreshId"
                         :id="ingr.helloFreshId">
                  <label class="text-gray-900 dark:text-white"
                         :class="{'dark:text-lime-300 text-lime-600':ingr.children.length > 0}"
                         :for="ingr.helloFreshId"
                         v-text="ingr.name"></label>
                  <span class="text-gray-900 dark:text-white"
                        v-text=" '(' + ingr.usage_count + ')'"></span>
                </div>
              </div>
            </div>
          </div>
          <!-- Modal footer -->
          <div
              class="max-sm:pb-24 flex items-center p-6 space-x-2 border-t border-gray-200 rounded-b dark:border-gray-600">
            <button @click="mergeIngredients(); mergeDialog = false"
                    class="text-white bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300 font-medium rounded-lg text-sm px-5 py-2.5 text-center dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800">
              Bestätigen
            </button>
            <button @click="mergeDialog = false"
                    class="text-gray-500 bg-white hover:bg-gray-100 focus:ring-4 focus:outline-none focus:ring-gray-200 rounded-lg border border-gray-200 text-sm font-medium px-5 py-2.5 hover:text-gray-900 focus:z-10 dark:bg-gray-700 dark:text-gray-300 dark:border-gray-500 dark:hover:text-white dark:hover:bg-gray-600 dark:focus:ring-gray-600">
              Abbrechen
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Search bar -->
    <div class="mt-5 mb-5 flex flex-col items-center">
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
        <input type="search" id="default-search" @keypress="store.fetchIngredients(overviewSearchString)"
               v-model="overviewSearchString"
               class="block w-full p-4 pl-10 text-sm text-gray-900 border border-gray-300 rounded-lg bg-gray-50 focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
               placeholder="Name" required>
      </div>

    </div>
    <!-- Navigation -->
    <div class="flex flex-col items-center">
            <span class="text-sm text-gray-700 dark:text-gray-400">
              Zeige <span class="font-semibold text-gray-900 dark:text-white"
                          v-text="store.nav.start"></span> bis <span
                class="font-semibold text-gray-900 dark:text-white"
                v-text="store.nav.end"></span> von <span
                class="font-semibold text-gray-900 dark:text-white"
                v-text="store.nav.count"></span> Einträgen
            </span>
      <div class="inline-flex mt-2 xs:mt-0">
        <button @click="store.previous()"
                class="px-4 py-2 text-sm font-medium text-white bg-gray-800 rounded-l hover:bg-gray-900 dark:bg-gray-800 dark:border-gray-700 dark:text-gray-400 dark:hover:bg-gray-700 dark:hover:text-white">
          Zurück
        </button>
        <button @click="store.next()"
                class="px-4 py-2 text-sm font-medium text-white bg-gray-800 border-0 border-l border-gray-700 rounded-r hover:bg-gray-900 dark:bg-gray-800 dark:border-gray-700 dark:text-gray-400 dark:hover:bg-gray-700 dark:hover:text-white">
          Weiter
        </button>
      </div>
    </div>
    <div class="mt-5 mb-5 flex flex-col items-center">
      <ul>
        <div v-for="ingredient in store.ingredients">
          <div>
            <li class="px-2 hover:bg-secondary-100 dark:text-white flex items-center">
              <input id="default-checkbox" type="checkbox" :value="ingredient.helloFreshId"
                     v-model="sourceIngredients"
                     class="mr-2 w-4 h-4 text-blue-600 bg-gray-100 border-gray-300 rounded focus:ring-blue-500 dark:focus:ring-blue-600 dark:ring-offset-gray-800 focus:ring-2 dark:bg-gray-700 dark:border-gray-600">
              <div v-if="ingredient.children.length > 0">
                <svg
                    @click="ingredient.open = !ingredient.open"
                    xmlns="http://www.w3.org/2000/svg"
                    fill="none"
                    viewBox="0 0 24 24"
                    stroke-width="2.5"
                    stroke="currentColor"
                    class="h-4 w-4 mr-1 cursor-pointer"
                    :class="{ 'transform rotate-90': ingredient.open }">
                  <path
                      stroke-linecap="round"
                      stroke-linejoin="round"
                      d="M8.25 4.5l7.5 7.5-7.5 7.5"></path>
                </svg>
              </div>
              <span v-text="ingredient.name"></span>
              <span v-text=" '(' + ingredient.usage_count + ')'"></span>
            </li>
            <div v-if="ingredient.open && ingredient.children.length > 0">
              <ul v-for="subingredient in ingredient.children" class="ml-8">
                <li class="px-2 hover:bg-secondary-100 dark:text-white">
                  <input id="default-checkbox" type="checkbox" :value="subingredient.helloFreshId"
                         v-model="sourceIngredients"
                         class="w-4 h-4 text-blue-600 bg-gray-100 border-gray-300 rounded focus:ring-blue-500 dark:focus:ring-blue-600 dark:ring-offset-gray-800 focus:ring-2 dark:bg-gray-700 dark:border-gray-600">
                  <span v-text="subingredient.name"></span>
                  <span v-text=" '(' + subingredient.usage_count + ')'"></span>
                </li>
              </ul>
            </div>
          </div>
        </div>

      </ul>
    </div>
  </div>
</template>

<style scoped>

</style>