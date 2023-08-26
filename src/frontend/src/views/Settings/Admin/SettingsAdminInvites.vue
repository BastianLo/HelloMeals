<script setup lang="ts">
import {useInviteStore} from "@/stores/InviteStore";
import {share} from "@/reusableMethods/share";

const store = useInviteStore()

const base_url = window.location.origin
const load = () => {
  store.fetchInvites()
}
load()
</script>

<template>
  <div data-dial-init class="fixed right-6 bottom-6 group mb-24">
    <button @click="store.createInvite()"
            class="flex items-center justify-center text-white bg-blue-700 rounded-lg w-14 h-14 hover:bg-blue-800 dark:bg-blue-600 dark:hover:bg-blue-700 focus:ring-4 focus:ring-blue-300 focus:outline-none dark:focus:ring-blue-800">
      <svg aria-hidden="true" class="w-8 h-8" fill="none"
           stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
              d="M12 6v6m0 0v6m0-6h6m-6 0H6"></path>
      </svg>
    </button>
  </div>
  <div class="mb-32">
    <div v-for="invite in store.invites" class="flex items-center justify-between mb-4">
      <p class="dark:text-white text-xl" v-text="invite.id"></p>
      <div class="grid grid-cols-2 gap-2">
        <button @click="store.deleteInvite(invite.id)"
                class="flex items-center justify-center p-1 rounded-lg bg-red-500 hover:bg-red-600 focus:outline-none">
          <svg class="w-6 h-6 text-white" aria-hidden="true" fill="none" stroke="currentColor"
               stroke-width="1.5"
               viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
            <path
                d="M14.74 9l-.346 9m-4.788 0L9.26 9m9.968-3.21c.342.052.682.107 1.022.166m-1.022-.165L18.16 19.673a2.25 2.25 0 01-2.244 2.077H8.084a2.25 2.25 0 01-2.244-2.077L4.772 5.79m14.456 0a48.108 48.108 0 00-3.478-.397m-12 .562c.34-.059.68-.114 1.022-.165m0 0a48.11 48.11 0 013.478-.397m7.5 0v-.916c0-1.18-.91-2.164-2.09-2.201a51.964 51.964 0 00-3.32 0c-1.18.037-2.09 1.022-2.09 2.201v.916m7.5 0a48.667 48.667 0 00-7.5 0"
                stroke-linecap="round" stroke-linejoin="round"></path>
          </svg>
        </button>
        <button @click="share('Invite', base_url + '/auth/register/' + invite.id)"
                class="flex items-center justify-center p-1 rounded-lg bg-blue-500 hover:bg-blue-600 focus:outline-none">
          <svg class="w-6 h-6 text-white" aria-hidden="true" fill="none" stroke="currentColor"
               stroke-width="1.5"
               viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
            <path
                d="M7.217 10.907a2.25 2.25 0 100 2.186m0-2.186c.18.324.283.696.283 1.093s-.103.77-.283 1.093m0-2.186l9.566-5.314m-9.566 7.5l9.566 5.314m0 0a2.25 2.25 0 103.935 2.186 2.25 2.25 0 00-3.935-2.186zm0-12.814a2.25 2.25 0 103.933-2.185 2.25 2.25 0 00-3.933 2.185z"
                stroke-linecap="round" stroke-linejoin="round"></path>
          </svg>
        </button>
      </div>
    </div>
  </div>
</template>

<style scoped>

</style>