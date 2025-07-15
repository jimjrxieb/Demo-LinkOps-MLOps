import { createRouter, createWebHistory } from 'vue-router'

// Import views
import Demo from '../views/Demo.vue'
import WhisPipeline from '../views/WhisPipeline.vue'
import OrbLibrary from '../views/OrbLibrary.vue'
import AddKeys from '../views/AddKeys.vue'
import AboutDemo from '../views/AboutDemo.vue'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Demo
  },
  {
    path: '/pipeline',
    name: 'WhisPipeline',
    component: WhisPipeline
  },
  {
    path: '/orbs',
    name: 'OrbLibrary',
    component: OrbLibrary
  },
  {
    path: '/keys',
    name: 'AddKeys',
    component: AddKeys
  },
  {
    path: '/about',
    name: 'AboutDemo',
    component: AboutDemo
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router 