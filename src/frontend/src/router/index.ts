import {createRouter, createWebHistory} from 'vue-router'
import {useAuthStore} from "@/stores/AuthStore";

const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes: [
        {
            path: '/',
            name: 'home',
            component: () => import('../views/HomeView.vue')
        },
        {
            path: '/auth',
            name: 'auth',
            children: [
                {
                    path: 'login',
                    name: 'login',
                    component: () => import('../views/auth/login.vue')
                },
                {
                    path: 'register/:id',
                    name: 'register',
                    component: () => import('../views/auth/register.vue')
                }
            ]
        },
        {
            path: '/Recipe',
            name: 'RecipeIndex',
            component: () => import('../views/Recipe/RecipeIndex.vue'),
            children: []
        },
        {
            path: '/Recipe/All',
            name: 'RecipeAll',
            component: () => import('../views/Recipe/RecipeAll.vue')
        },
        {
            path: '/Recipe/Favorites',
            name: 'RecipeFavorites',
            component: () => import('../views/Recipe/RecipeAll.vue')
        },
        {
            path: '/Recipe/:id',
            name: 'RecipeById',
            component: () => import('../views/Recipe/RecipeDetails.vue')
        },
        {
            path: '/Pantry',
            name: 'PantryIndex',
            component: () => import('../views/PlaceholderView.vue')
        },
        {
            path: '/Planner',
            name: 'PlannerIndex',
            component: () => import('../views/PlaceholderView.vue')
        },
        {
            path: '/Settings',
            name: 'SettingsIndex',
            component: () => import('../views/Settings/SettingsIndex.vue')
        },
        {
            path: '/Settings/Profile',
            name: 'SettingsProfile',
            component: () => import('../views/Settings/Profile/SettingsProfile.vue')
        },
        {
            path: '/Settings/Admin',
            name: 'SettingsAdmin',
            component: () => import('../views/Settings/Admin/SettingsAdminIndex.vue')
        },
        {
            path: '/Settings/Admin/Downloader',
            name: 'SettingsAdminDownloader',
            component: () => import('../views/Settings/Admin/SettingsAdminDownloader.vue')
        },
        {
            path: '/Settings/Admin/Invites',
            name: 'SettingsAdminInvites',
            component: () => import('../views/Settings/Admin/SettingsAdminInvites.vue')
        },
        {
            path: '/Settings/Admin/Grouping',
            name: 'SettingsAdminGrouping',
            component: () => import('../views/Settings/Admin/grouping/SettingsAdminGroupingIndex.vue')
        },
        {
            path: '/Settings/Admin/Grouping/Tags',
            name: 'SettingsAdminGroupingTags',
            component: () => import('../views/Settings/Admin/grouping/SettingsAdminGroupingTags.vue')
        },
        {
            path: '/Settings/Admin/Grouping/Ingredients',
            name: 'SettingsAdminGroupingIngredients',
            component: () => import('../views/Settings/Admin/grouping/SettingsAdminGroupingIngredients.vue')
        },
    ]
})

router.beforeEach(async (to) => {
    // redirect to login page if not logged in and trying to access a restricted page
    const publicPages = ['/auth/login'];
    const authRequired = !publicPages.includes(to.path);
    const auth = useAuthStore();
    if (authRequired && !(await auth.get_valid_token())) {
        auth.returnUrl = to.fullPath;
        return '/auth/login';
    }
});
export default router
