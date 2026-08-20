<script setup lang="ts">
import {computed} from "vue";
import {useI18n} from "vue-i18n";
import {useSettingsStore, type globalPreference} from "@/stores/SettingsStore";
import RefreshSwiper from "@/components/common/RefreshSwiper.vue";

const store = useSettingsStore()
const {t, te} = useI18n()

const load = () => {
  store.fetchPreferences()
}
load()

// The backend only ever returns the raw (English) help_text it was registered with - the
// frontend owns translation, falling back to that raw text for any preference we don't have a
// translation key for yet, so newly-added backend preferences never break instead of vanishing.
const preferenceLabel = (preference: globalPreference) => {
  const key = `settings.preferences.${preference.identifier}`
  return te(key) ? t(key) : preference.help_text
}

const booleanPreferences = computed(() => store.preferences.filter(p => p.field.class === 'BooleanField'))
const numberPreferences = computed(() => store.preferences.filter(p => p.field.class === 'FloatField'))
</script>

<template>
  <RefreshSwiper @refresh="load()"/>
  <div class="max-w-xl mx-auto mb-24">
    <h1 class="text-xl font-semibold text-white mb-4" v-text="t('settings.general.title')"></h1>
    <div v-for="preference in booleanPreferences" :key="preference.id"
         class="flex items-center justify-between py-3 border-b border-gray-700">
      <label :for="preference.identifier" class="text-white text-sm mr-4" v-text="preferenceLabel(preference)"></label>
      <input :id="preference.identifier" type="checkbox"
             :checked="preference.value as boolean"
             @change="store.updatePreference(preference, ($event.target as HTMLInputElement).checked)"
             class="w-5 h-5 rounded shrink-0 focus:ring-2 focus:ring-blue-500 accent-blue-600">
    </div>
    <div v-for="preference in numberPreferences" :key="preference.id"
         class="flex items-center justify-between py-3 border-b border-gray-700">
      <label :for="preference.identifier" class="text-white text-sm mr-4" v-text="preferenceLabel(preference)"></label>
      <input :id="preference.identifier" type="number" step="0.1"
             :value="preference.value"
             @change="store.updatePreference(preference, parseFloat(($event.target as HTMLInputElement).value))"
             class="w-24 shrink-0 rounded bg-gray-700 border-gray-600 text-white text-sm focus:ring-blue-500 focus:border-blue-500">
    </div>
  </div>
</template>

<style scoped>
</style>
