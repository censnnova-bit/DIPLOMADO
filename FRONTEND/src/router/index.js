import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import Login from '../views/Login.vue'
import ClassroomList from '../views/ClassroomList.vue'
import ClassroomDetail from '../views/ClassroomDetail.vue'
import AdminSalones from '../views/AdminSalones.vue'
import AdminReservas from '../views/AdminReservas.vue'
import AdminAsignaturas from '../views/AdminAsignaturas.vue'
import AdminUsuarios from '../views/AdminUsuarios.vue'
import AdminMetricas from '../views/AdminMetricas.vue'
import EditReservations from '../views/EditReservations.vue'

const routes = [
  {
    path: '/',
    name: 'Home',
    redirect: '/login'
  },
  {
    path: '/login',
    name: 'Login',
    component: Login
  },
  {
    path: '/salones',
    name: 'ClassroomList',
    component: ClassroomList,
    meta: { requiresAuth: true }
  },
  {
    path: '/aula/:id',
    name: 'ClassroomDetail',
    component: ClassroomDetail,
    meta: { requiresAuth: true }
  },
  {
    path: '/reservas',
    name: 'MyReservations',
    component: () => import('../views/MyReservations.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/admin/salones',
    name: 'AdminSalones',
    component: AdminSalones,
    meta: { requiresAuth: true, requiresAdmin: true }
  },
  {
    path: '/admin/reservas',
    name: 'AdminReservas',
    component: AdminReservas,
    meta: { requiresAuth: true, requiresAdmin: true }
  },
  {
    path: '/admin/asignaturas',
    name: 'AdminAsignaturas',
    component: AdminAsignaturas,
    meta: { requiresAuth: true, requiresAdmin: true }
  },
  {
    path: '/admin/usuarios',
    name: 'AdminUsuarios',
    component: AdminUsuarios,
    meta: { requiresAuth: true, requiresAdmin: true }
  },
  {
    path: '/admin/metricas',
    name: 'AdminMetricas',
    component: AdminMetricas,
    meta: { requiresAuth: true, requiresAdmin: true }
  },
  {
    path: '/reservas/editar',
    name: 'EditReservations',
    component: EditReservations,
    meta: { requiresAuth: true }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// Navigation guards
router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()
  
  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    next('/login')
  } else if (to.meta.requiresAdmin && !authStore.isAdmin) {
    next('/salones')
  } else if (to.meta.requiresGuest && authStore.isAuthenticated) {
    next('/salones')
  } else {
    next()
  }
})

export default router
