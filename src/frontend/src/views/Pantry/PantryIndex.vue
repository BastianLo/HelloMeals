<script setup lang="ts">
import {usePantryStore} from "@/stores/PantryStore";
import {ref} from "vue";
import {OnClickOutside} from "@vueuse/components";

const store = usePantryStore()

const newPantryName = ref('')
const newMembershipId = ref('')

const popups = ref({
  create: false,
  join: false,
  delete: false
})

</script>

<template>
  <div class="flex flex-col items-center">
    <!-- Modal to create pantry -->
    <div class="relative z-10" aria-labelledby="modal-title" role="dialog" aria-modal="true"
         v-if="popups.create">
      <div class="fixed inset-0 bg-gray-500 bg-opacity-75 transition-opacity"></div>
      <div class="fixed inset-0 z-10 overflow-y-auto">
        <div class="flex min-h-full items-end justify-center p-4 text-center sm:items-center sm:p-0 mb-40">
          <OnClickOutside @trigger="popups.create=false">
            <div style="width: 400px"
                 class="relative transform overflow-hidden rounded-lg bg-white text-left shadow-xl transition-all sm:my-8 sm:w-full sm:max-w-lg">
              <div class="w-lg shadow p-5 rounded-lg bg-gray-800 flex flex-col items-center">
                <!-- Popup head -->
                <div class="flex items-center justify-between mt-4">
                  <p class="text-xl font-bold text-white">
                    Name
                  </p>
                </div>
                <!-- Popup body -->
                <div class="mt-5 flex flex-col items-center">
                  <label>
                    <input placeholder="Name" v-model="newPantryName"
                           class="text-white bg-gray-700 border border-gray-400 rounded-lg px-4 py-2 focus:outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-300"/>
                  </label>
                  <button @click="store.createPantry(newPantryName); popups.create=false"
                          class="mt-4 text-white px-4 py-2 focus:ring-4 focus:outline-none font-medium rounded-lg text-sm bg-blue-600 hover:bg-blue-700 focus:ring-blue-800">
                    Erstellen
                  </button>
                </div>
              </div>
            </div>
          </OnClickOutside>
        </div>
      </div>
    </div>


    <!-- Modal to join pantry -->
    <div class="relative z-10" aria-labelledby="modal-title" role="dialog" aria-modal="true"
         v-if="popups.join">
      <div class="fixed inset-0 bg-gray-500 bg-opacity-75 transition-opacity"></div>
      <div class="fixed inset-0 z-10 overflow-y-auto">
        <div class="flex min-h-full items-end justify-center p-4 text-center sm:items-center sm:p-0 mb-40">
          <OnClickOutside @trigger="popups.join=false">
            <div style="width: 400px"
                 class="relative transform overflow-hidden rounded-lg bg-white text-left shadow-xl transition-all sm:my-8 sm:w-full sm:max-w-lg">
              <div class="w-lg shadow p-5 rounded-lg bg-gray-800 flex flex-col items-center">
                <!-- Popup head -->
                <div class="flex items-center justify-between mt-4">
                  <p class="text-xl font-bold text-white">
                    Wähle einen Vorrat aus, um diesen beizutreten
                  </p>
                </div>
                <!-- Popup body -->
                <div class="mt-5 flex flex-col items-center">
                  <select v-model="newMembershipId"
                          class="border text-sm rounded-lg block w-full p-2.5 bg-gray-700 border-gray-600 placeholder-gray-400 text-white focus:ring-blue-500 focus:border-blue-500">
                    <option value="" selected>Auswählen</option>
                    <option v-for="pantry in store.availablePantries" :value="pantry.id" v-text="pantry.name"></option>
                  </select>

                  <button @click="store.joinPantry(newMembershipId); popups.join=false"
                          class="mt-4 text-white px-4 py-2 focus:ring-4 focus:outline-none font-medium rounded-lg text-sm bg-blue-600 hover:bg-blue-700 focus:ring-blue-800">
                    Beitreten
                  </button>
                </div>
              </div>
            </div>
          </OnClickOutside>
        </div>
      </div>
    </div>

    <!-- Modal to leave pantry -->
    <div class="relative z-10" aria-labelledby="modal-title" role="dialog" aria-modal="true"
         v-if="popups.delete">
      <div class="fixed inset-0 bg-gray-500 bg-opacity-75 transition-opacity"></div>
      <div class="fixed inset-0 z-10 overflow-y-auto">
        <div class="flex min-h-full items-end justify-center p-4 text-center sm:items-center sm:p-0 mb-40">
          <OnClickOutside @trigger="popups.delete=false">
            <div style="width: 400px"
                 class="relative transform overflow-hidden rounded-lg bg-white text-left shadow-xl transition-all sm:my-8 sm:w-full sm:max-w-lg">
              <div class="w-lg shadow p-5 rounded-lg bg-gray-800 flex flex-col items-center">
                <!-- Popup head -->
                <div class="flex items-center justify-between mt-4">
                  <p class="text-xl font-bold text-white">
                    Vorrat wirklich verlassen?
                  </p>
                </div>
                <!-- Popup body -->
                <div class="mt-5 flex flex-row space-x-4 items-center">
                  <button @click="store.leavePantry(); popups.delete=false"
                          class="mt-4 text-white px-4 py-2 focus:ring-4 focus:outline-none font-medium rounded-lg text-sm bg-red-600 hover:bg-red-700 focus:ring-red-800">
                    Ja
                  </button>
                  <button @click="popups.delete=false"
                          class="mt-4 text-white px-4 py-2 focus:ring-4 focus:outline-none font-medium rounded-lg text-sm bg-blue-600 hover:bg-blue-700 focus:ring-blue-800">
                    Nein
                  </button>
                </div>
              </div>
            </div>
          </OnClickOutside>
        </div>
      </div>
    </div>


    <div class="w-96 flex flex-col items-center" v-if="store.joinedPantryId === null">
      <p class="mr-4 mb-2 text-center text-3xl font-bold text-white">Kein Vorrat erstellt</p>
      <p class="mr-4 text-l text-white">Du hast noch keinen Vorrat erstellt. Du kannst entweder ein
        neuen Vorrat erstellen oder einem bestehenden Vorrat eines anderen Nutzers beitreten</p>
      <button type="button" @click="popups.create = true"
              class="mt-4 w-1/2 text-white focus:ring-4 font-medium rounded-lg text-sm px-5 py-2.5 bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-blue-800">
        Erstellen
      </button>
      <button type="button" @click="popups.join=true"
              class="mt-4 w-1/2 text-white focus:ring-4 font-medium rounded-lg text-sm px-5 py-2.5 bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-blue-800">
        Beitreten
      </button>
    </div>
    <div class="w-96 flex flex-col items-center" v-if="store.joinedPantryId !== null">
      <p class="mr-4 mb-2 text-center text-3xl font-bold text-white">Vorrat
        '{{ store.getJoinedPantryName }}'</p>
      <p class="mr-4 text-l text-white">Du bist im Vorrat '{{ store.getJoinedPantryName }}' mit den
        folgenden Personen:</p>
      <ul class="max-w-md space-y-1 list-disc list-inside">
        <li v-for="member in store.joinedPantryMembers" class="text-white">{{ member }}</li>
      </ul>
      <button type="button" @click="popups.delete = true"
              class="mt-4 w-1/2 text-white focus:ring-4 font-medium rounded-lg text-sm px-5 py-2.5 bg-red-600 hover:bg-red-700 focus:outline-none focus:ring-red-800">
        Verlassen
      </button>
    </div>
  </div>

</template>

<style scoped>

</style>