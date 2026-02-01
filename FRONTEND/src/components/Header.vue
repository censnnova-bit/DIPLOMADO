<script setup>
import { ref, onMounted, computed } from 'vue'
import { useAuthStore } from '../stores/auth'
import { useRouter, useRoute } from 'vue-router'

const isDark = ref(false)
const authStore = useAuthStore()
const router = useRouter()
const route = useRoute()

// Función para determinar si una ruta está activa
const isActive = (path) => {
  return route.path === path || route.path.startsWith(path + '/')
}

// Inicializar dark mode desde localStorage
onMounted(() => {
  const savedTheme = localStorage.getItem('theme')

  if (savedTheme === 'dark') {
    isDark.value = true
    document.documentElement.classList.add('dark')
  } else {
    isDark.value = false
    document.documentElement.classList.remove('dark')
  }
})

const toggleDarkMode = () => {
  isDark.value = !isDark.value

  if (isDark.value) {
    document.documentElement.classList.add('dark')
    localStorage.setItem('theme', 'dark')
  } else {
    document.documentElement.classList.remove('dark')
    localStorage.setItem('theme', 'light')
  }
}

const handleLogout = async () => {
  await authStore.logout()
}
</script>

<template>
  <header class="sticky top-0 z-50 drop-shadow-md">
    <div class="bg-[#B90A0A] relative z-10">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex items-center justify-between h-20">
          <!-- Logo -->
          <div class="flex items-center space-x-4">
            <div class="flex items-center gap-3">
              <div class="bg-white/10 p-2 rounded-lg backdrop-blur-sm border border-white/20 hidden sm:block">
                <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                    d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" />
                </svg>
              </div>
              <div class="flex flex-col">
                <span class="font-display font-black text-white text-3xl tracking-wider leading-none">GECOS</span>
                <span class="text-white/90 text-[0.6rem] font-bold uppercase tracking-[0.2em] mt-1">Gestión de
                  Espacios</span>
              </div>
            </div>
          </div>

          <!-- Desktop Navigation -->
          <nav v-if="authStore.isAuthenticated" class="hidden md:flex items-center space-x-2">
            <router-link to="/salones"
              :class="isActive('/salones') ? 'bg-white text-[#B90A0A] shadow-sm font-bold' : 'text-white hover:bg-white/10 font-semibold'"
              class="px-4 py-2 rounded-lg text-sm transition-all duration-200 transform hover:scale-105">
              Salones
            </router-link>

            <router-link v-if="authStore.isAdmin" to="/admin/salones"
              :class="isActive('/admin/salones') ? 'bg-white text-[#B90A0A] shadow-sm font-bold' : 'text-white hover:bg-white/10 font-semibold'"
              class="px-4 py-2 rounded-lg text-sm transition-all duration-200 transform hover:scale-105">
              Gestionar Salones
            </router-link>

            <router-link v-if="authStore.isAdmin" to="/admin/reservas"
              :class="isActive('/admin/reservas') ? 'bg-white text-[#B90A0A] shadow-sm font-bold' : 'text-white hover:bg-white/10 font-semibold'"
              class="px-4 py-2 rounded-lg text-sm transition-all duration-200 transform hover:scale-105">
              Gest. Reservas
            </router-link>

            <router-link v-if="authStore.isAdmin" to="/admin/asignaturas"
              :class="isActive('/admin/asignaturas') ? 'bg-white text-[#B90A0A] shadow-sm font-bold' : 'text-white hover:bg-white/10 font-semibold'"
              class="px-4 py-2 rounded-lg text-sm transition-all duration-200 transform hover:scale-105">
              Gest. Asignaturas
            </router-link>

            <router-link v-if="authStore.isAdmin" to="/admin/usuarios"
              :class="isActive('/admin/usuarios') ? 'bg-white text-[#B90A0A] shadow-sm font-bold' : 'text-white hover:bg-white/10 font-semibold'"
              class="px-4 py-2 rounded-lg text-sm transition-all duration-200 transform hover:scale-105">
              Gest. Usuarios
            </router-link>

            <router-link v-if="authStore.isAdmin" to="/admin/metricas"
              :class="isActive('/admin/metricas') ? 'bg-white text-[#B90A0A] shadow-sm font-bold' : 'text-white hover:bg-white/10 font-semibold'"
              class="px-4 py-2 rounded-lg text-sm transition-all duration-200 transform hover:scale-105 flex items-center gap-1">
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                  d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
              </svg>
              Métricas
            </router-link>

            <router-link v-if="!authStore.isAdmin" to="/reservas"
              :class="isActive('/reservas') && !isActive('/reservas/editar') ? 'bg-white text-[#B90A0A] shadow-sm font-bold' : 'text-white hover:bg-white/10 font-semibold'"
              class="px-4 py-2 rounded-lg text-sm transition-all duration-200 transform hover:scale-105">
              Mis Reservas
            </router-link>

            <!-- Link de edición para Admin y Docente (todos los auth) -->
            <router-link to="/reservas/editar"
              :class="isActive('/reservas/editar') ? 'bg-white text-[#B90A0A] shadow-sm font-bold' : 'text-white hover:bg-white/10 font-semibold'"
              class="px-4 py-2 rounded-lg text-sm transition-all duration-200 transform hover:scale-105">
              Editar Reservas
            </router-link>

            <div class="h-6 w-px bg-white/20 mx-2"></div>

            <!-- User info -->
            <div class="text-white text-sm px-3 py-1.5 bg-white/10 rounded-lg">
              <span class="font-semibold">{{ authStore.user?.first_name || authStore.user?.username }}</span>
              <span class="text-white/70 text-xs ml-2">({{ authStore.user?.rol }})</span>
            </div>

            <button @click="toggleDarkMode" class="text-white hover:bg-white/10 p-2 rounded-lg transition-colors"
              title="Cambiar tema">
              <!-- Luna cuando está en modo claro (para activar el oscuro) -->
              <svg v-if="!isDark" class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                  d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z" />
              </svg>
              <!-- Sol cuando está en modo oscuro (para activar el claro) -->
              <svg v-if="isDark" class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                  d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z" />
              </svg>
            </button>
            <button @click="handleLogout"
              class="text-white hover:bg-white/10 px-4 py-2 rounded-lg text-sm font-semibold transition-all duration-200 flex items-center group">
              <svg class="w-4 h-4 mr-2 group-hover:-translate-x-1 transition-transform" fill="none"
                stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                  d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
              </svg>
              Cerrar Sesión
            </button>
          </nav>

          <!-- Mobile menu button -->
          <div class="md:hidden">
            <button class="text-white hover:bg-white/10 p-2 rounded-lg focus:outline-none transition-colors"
              type="button">
              <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
              </svg>
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Wave effect -->
    <div class="text-[#B90A0A] w-full leading-[0] relative z-10">
      <svg class="block w-full h-8 md:h-12 lg:h-14" preserveAspectRatio="none" viewBox="0 0 1440 100">
        <path d="M0,0 L1440,0 L1440,30 Q720,100 0,30 Z" fill="currentColor"></path>
      </svg>
    </div>
  </header>
</template>
