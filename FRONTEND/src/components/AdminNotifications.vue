<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import api from '../services/api'

const authStore = useAuthStore()
const router = useRouter()
const reservasOcupadas = ref([])
const showNotificaciones = ref(false)

onMounted(async () => {
  if (authStore.isAdmin) {
    await cargarReservasOcupadas()
  }
})

const cargarReservasOcupadas = async () => {
  try {
    const response = await api.getReservas({ estado: 'confirmada' })
    const today = new Date()
    const reservas = response.data.results || response.data

    // Filtrar reservas del día actual
    reservasOcupadas.value = reservas.filter(r => {
      const fechaReserva = new Date(r.fecha)
      return fechaReserva.toDateString() === today.toDateString()
    })

    if (reservasOcupadas.value.length > 0) {
      showNotificaciones.value = true
    }
  } catch (err) {
    console.error('Error cargando notificaciones:', err)
  }
}

const cerrarNotificaciones = () => {
  showNotificaciones.value = false
}
</script>

<template>
  <!-- Notificaciones para Admin -->
  <div v-if="showNotificaciones && reservasOcupadas.length > 0"
    class="fixed top-20 right-4 z-50 w-96 bg-white dark:bg-gray-800 shadow-2xl rounded-lg border-l-4 border-[#B90A0A] animate-slide-in">
    <div class="p-4">
      <div class="flex justify-between items-start mb-3">
        <div>
          <h3 class="text-lg font-bold text-gray-900 dark:text-white flex items-center">
            <svg class="w-5 h-5 text-[#B90A0A] mr-2" fill="currentColor" viewBox="0 0 20 20">
              <path
                d="M10 2a6 6 0 00-6 6v3.586l-.707.707A1 1 0 004 14h12a1 1 0 00.707-1.707L16 11.586V8a6 6 0 00-6-6zM10 18a3 3 0 01-3-3h6a3 3 0 01-3 3z" />
            </svg>
            Salones Ocupados Hoy
          </h3>
          <p class="text-sm text-gray-600 dark:text-gray-400">{{ reservasOcupadas.length }} reserva(s) activa(s)</p>
        </div>
        <button @click="cerrarNotificaciones" class="text-gray-400 hover:text-gray-600 dark:hover:text-gray-300">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
      </div>

      <div class="space-y-2 max-h-64 overflow-y-auto">
        <div v-for="reserva in reservasOcupadas" :key="reserva.id" class="bg-gray-50 dark:bg-gray-700 p-3 rounded-lg">
          <p class="text-sm font-semibold text-gray-900 dark:text-white">{{ reserva.motivo }}</p>
          <p class="text-xs text-gray-600 dark:text-gray-400 mt-1">
            {{ reserva.hora_inicio.substring(0, 5) }} - {{ reserva.hora_fin.substring(0, 5) }}
          </p>
          <p class="text-xs text-gray-500 dark:text-gray-500 mt-1">
            {{ reserva.usuario_nombre || 'Usuario no especificado' }}
          </p>
        </div>
      </div>

      <router-link to="/admin/reservas" @click="cerrarNotificaciones"
        class="block mt-3 text-center text-sm text-[#B90A0A] font-semibold hover:underline">
        Ver todas las reservas →
      </router-link>
    </div>
  </div>
</template>

<style scoped>
@keyframes slide-in {
  from {
    transform: translateX(100%);
    opacity: 0;
  }

  to {
    transform: translateX(0);
    opacity: 1;
  }
}

.animate-slide-in {
  animation: slide-in 0.3s ease-out;
}
</style>
