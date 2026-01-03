import {createRouter, createWebHistory} from 'vue-router'

const routes = [
    { path: '/',component: () => import('../views/MenuBar.vue')},
    { path: '/datalabeling', component: () => import('../views/DataLabeling.vue') },
    { path: '/data_collection', component: () => import('../views/DataCollection.vue') }
]

const router = createRouter({
    history: createWebHistory(),
    routes
})

export default router