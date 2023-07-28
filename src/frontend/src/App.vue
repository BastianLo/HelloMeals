<template>
  <div>
    <!-- Top Bar -->
    <nav class="border-b border-gray-600">
      <div class="max-w-screen-xl flex flex-wrap items-center justify-between mx-auto p-4">
        <RouterLink class="flex items-center" to="/">
          <img src="@/assets/logo_512px.png" class="h-8 mr-3" alt="Flowbite Logo"/>
          <span class="self-center text-2xl font-semibold whitespace-nowrap text-white">HelloMeals</span>
        </RouterLink>
      </div>
    </nav>
    <RouterView/>
    <!-- Foot Menu -->
    <div class="fixed bottom-0 left-0 z-50 w-full">
      <div class="border-t bg-gray-700 border-gray-600">
        <div class="grid h-16 max-w-lg mx-auto font-medium" :class="'grid-cols-4'">
          <RouterLink v-for="item in menuItems" :to="item.href"
                      class="inline-flex flex-col items-center justify-center px-5 hover:bg-gray-800 group border-x border-gray-600">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" :fill="item.fill ? 'currentcolor' : 'none'"
                 :stroke="item.fill ? 'none' : 'currentColor'"
                 stroke-width="2"
                 class="w-6 h-6 mb-1 text-gray-400">
              <path
                  :d="item.svg"></path>
            </svg>
            <span v-text="$t(item.name)"
                  class="text-sm text-gray-400 group-hover:text-blue-500"></span>
          </RouterLink>
        </div>

      </div>
    </div>
    <slot/>
    <div class="mb-20"/>

  </div>
</template>
<script setup lang="ts">

const menuItems = [
  {
    name: 'recipe.navLabel',
    fill: true,
    href: '/Recipe',
    svg: 'M3.375 3C2.339 3 1.5 3.84 1.5 4.875v.75c0 1.036.84 1.875 1.875 1.875h17.25c1.035 0 1.875-.84 1.875-1.875v-.75C22.5 3.839 21.66 3 20.625 3H3.375z M3.087 9l.54 9.176A3 3 0 006.62 21h10.757a3 3 0 002.995-2.824L20.913 9H3.087zm6.163 3.75A.75.75 0 0110 12h4a.75.75 0 010 1.5h-4a.75.75 0 01-.75-.75z'
  },
  {
    name: 'storage.navLabel',
    fill: false,
    href: '/Storage',
    svg: 'M15.75 10.5V6a3.75 3.75 0 10-7.5 0v4.5m11.356-1.993l1.263 12c.07.665-.45 1.243-1.119 1.243H4.25a1.125 1.125 0 01-1.12-1.243l1.264-12A1.125 1.125 0 015.513 7.5h12.974c.576 0 1.059.435 1.119 1.007zM8.625 10.5a.375.375 0 11-.75 0 .375.375 0 01.75 0zm7.5 0a.375.375 0 11-.75 0 .375.375 0 01.75 0z'
  },
  {
    name: 'planner.navLabel',
    fill: true,
    href: '/Planner',
    svg: 'M12.75 12.75a.75.75 0 11-1.5 0 .75.75 0 011.5 0zM7.5 15.75a.75.75 0 100-1.5.75.75 0 000 1.5zM8.25 17.25a.75.75 0 11-1.5 0 .75.75 0 011.5 0zM9.75 15.75a.75.75 0 100-1.5.75.75 0 000 1.5zM10.5 17.25a.75.75 0 11-1.5 0 .75.75 0 011.5 0zM12 15.75a.75.75 0 100-1.5.75.75 0 000 1.5zM12.75 17.25a.75.75 0 11-1.5 0 .75.75 0 011.5 0zM14.25 15.75a.75.75 0 100-1.5.75.75 0 000 1.5zM15 17.25a.75.75 0 11-1.5 0 .75.75 0 011.5 0zM16.5 15.75a.75.75 0 100-1.5.75.75 0 000 1.5zM15 12.75a.75.75 0 11-1.5 0 .75.75 0 011.5 0zM16.5 13.5a.75.75 0 100-1.5.75.75 0 000 1.5z M6.75 2.25A.75.75 0 017.5 3v1.5h9V3A.75.75 0 0118 3v1.5h.75a3 3 0 013 3v11.25a3 3 0 01-3 3H5.25a3 3 0 01-3-3V7.5a3 3 0 013-3H6V3a.75.75 0 01.75-.75zm13.5 9a1.5 1.5 0 00-1.5-1.5H5.25a1.5 1.5 0 00-1.5 1.5v7.5a1.5 1.5 0 001.5 1.5h13.5a1.5 1.5 0 001.5-1.5v-7.5z'
  },
  {
    name: 'settings.navLabel',
    href: '/Settings',
    fill: true,
    svg: 'M5 4a1 1 0 00-2 0v7.268a2 2 0 000 3.464V16a1 1 0 102 0v-1.268a2 2 0 000-3.464V4zM11 4a1 1 0 10-2 0v1.268a2 2 0 000 3.464V16a1 1 0 102 0V8.732a2 2 0 000-3.464V4zM16 3a1 1 0 011 1v7.268a2 2 0 010 3.464V16a1 1 0 11-2 0v-1.268a2 2 0 010-3.464V4a1 1 0 011-1z'
  },
]
document.body.classList.add("bg-slate-900")
</script>

