<template>
  <section class="bg-gray-900">
    <div class="flex flex-col items-center justify-center px-6 py-8 mx-auto lg:py-0 mt-16">
      <a href="#" class="flex items-center mb-6 text-2xl font-semibold text-white">
        <img class="w-8 h-8 mr-2" src="@/assets/logo_512px.png"
             alt="logo">
        HelloMeals
      </a>
      <div
          class="w-full rounded-lg shadow border md:mt-0 sm:max-w-md xl:p-0 bg-gray-800 border-gray-700">
        <div class="p-6 space-y-4 md:space-y-6 sm:p-8">
          <h1 class="text-xl font-bold leading-tight tracking-tight md:text-2xl text-white">
            Melde dich mit deinem Account an
          </h1>
          <form class="flex flex-col space-y-4 md:space-y-6 items-center" @submit.prevent="login">
            <div class="w-full">
              <label for="email" class="block mb-2 text-sm font-medium text-white">
                Benutzername</label>
              <input type="text" v-model="username" name="username"
                     class="border sm:text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5 bg-gray-700 border-gray-600 placeholder-gray-400 text-white focus:ring-blue-500 focus:border-blue-500"/>
            </div>
            <div class="w-full">
              <label for="password"
                     class="block mb-2 text-sm font-medium text-white">Passwort</label>
              <input type="password" v-model="password" name="password"
                     class="border sm:text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5 bg-gray-700 border-gray-600 placeholder-gray-400 text-white focus:ring-blue-500 focus:border-blue-500"/>
            </div>
            <div v-if="errorMessage" class="text-red-500 text-sm mt-2">
              {{ errorMessage }}
            </div>
            <button type="submit"
                    class="w-fit justify-self-center border-gray-300 border bg-primary-600 hover:bg-primary-700 focus:ring-4 focus:outline-none focus:ring-primary-300 font-medium rounded-lg text-sm px-5 py-2.5 text-center bg-primary-600 hover:bg-primary-700 focus:ring-primary-800 text-white">
              Anmelden
            </button>
          </form>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">

import {ref} from "vue";
import {useAuthStore} from "@/stores/AuthStore";
import {storeToRefs} from "pinia";
import router from "@/router";

let errorMessage = ref("");
let username = ref("")
let password = ref("")

let authStore = useAuthStore()
let {user} = storeToRefs(authStore)
authStore.get_valid_token()

let login = async () => {
  const response = await authStore.login(username.value, password.value)
  errorMessage.value = response.message;
  if (response.response.ok) {
    await router.push(authStore.returnUrl)
  }
}
</script>