<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import { useNotificationStore } from '../stores/notification'
import Header from '../components/Header.vue'
import api from '../services/api'

const authStore = useAuthStore()
const notification = useNotificationStore()
const router = useRouter()

// Verificar que sea admin
if (!authStore.isAdmin) {
  router.push('/salones')
}

const reservas = ref([])
const salones = ref([])
const loading = ref(false)
const filterEstado = ref('todas')
const currentPage = ref(1)
const canNext = ref(false)
const canPrev = ref(false)
const totalReservas = ref(0) // Opcional, para mostrar total

const estadoOptions = [
  { value: 'todas', label: 'Todas las Reservas' },
  { value: 'pendiente', label: 'Pendientes' },
  { value: 'confirmada', label: 'Confirmadas' },
  { value: 'cancelada', label: 'Canceladas' },
  { value: 'completada', label: 'Completadas' }
]

// Observar cambio de filtro para recargar desde página 1
import { watch } from 'vue'
watch(filterEstado, () => {
  currentPage.value = 1
  loadReservas()
})

onMounted(() => {
  loadReservas()
  loadSalones()
})

const loadReservas = async (page = 1) => {
  loading.value = true
  try {
    const params = { page }
    if (filterEstado.value !== 'todas') {
      params.estado = filterEstado.value
    }

    const response = await api.getReservas(params)

    // Manejo de respuesta paginada de Django REST Framework
    if (response.data.results) {
      reservas.value = response.data.results
      canNext.value = !!response.data.next
      canPrev.value = !!response.data.previous
      totalReservas.value = response.data.count
      currentPage.value = page
    } else {
      // Fallback si no hay paginación
      reservas.value = response.data
      canNext.value = false
      canPrev.value = false
    }
  } catch (err) {
    console.error('Error cargando reservas:', err)
    notification.error('Error al cargar las reservas')
  } finally {
    loading.value = false
  }
}

const nextPage = () => {
  if (canNext.value) {
    loadReservas(currentPage.value + 1)
  }
}

const prevPage = () => {
  if (canPrev.value && currentPage.value > 1) {
    loadReservas(currentPage.value - 1)
  }
}


const loadSalones = async () => {
  try {
    const response = await api.getSalones()
    salones.value = response.data.results || response.data
  } catch (err) {
    console.error('Error cargando salones:', err)
  }
}

const getSalonNombre = (salonId) => {
  const salon = salones.value.find(s => s.id === salonId)
  return salon ? salon.nombre : `Salón #${salonId}`
}

const formatDate = (dateStr) => {
  const date = new Date(dateStr)
  return date.toLocaleDateString('es-CO', {
    year: 'numeric',
    month: 'short',
    day: 'numeric'
  })
}

const formatTime = (timeStr) => {
  return timeStr.substring(0, 5)
}

const cambiarEstado = async (reservaId, nuevoEstado) => {
  if (!confirm(`¿Está seguro de cambiar el estado a "${nuevoEstado}"?`)) return

  try {
    await api.updateReserva(reservaId, { estado: nuevoEstado })
    notification.success('Estado actualizado exitosamente')
    loadReservas()
  } catch (err) {
    console.error('Error actualizando estado:', err)
    notification.error('Error al actualizar el estado')
  }
}

const eliminarReserva = async (reservaId, motivo) => {
  if (!confirm(`¿Está seguro de eliminar PERMANENTEMENTE la reserva "${motivo}"?`)) return

  try {
    await api.cancelarReserva(reservaId)
    // Forzar recarga completa
    await loadReservas()
    // Notificar éxito
    notification.success('Reserva eliminada exitosamente del sistema')
  } catch (err) {
    console.error('Error eliminando reserva:', err)
    notification.error('Error al eliminar la reserva')
  }
}

const getEstadoClass = (estado) => {
  const classes = {
    pendiente: 'bg-yellow-100 text-yellow-800',
    confirmada: 'bg-green-100 text-green-800',
    cancelada: 'bg-red-100 text-red-800',
    completada: 'bg-blue-100 text-blue-800'
  }
  return classes[estado] || 'bg-gray-100 text-gray-800'
}
</script>

<template>
  <div class="min-h-screen bg-white dark:bg-gray-900">
    <Header />

    <main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div class="mb-6">
        <h1 class="text-3xl font-bold text-gray-900 dark:text-white">Administrar Reservas</h1>
        <p class="text-gray-600 dark:text-gray-400 mt-1">Gestionar y aprobar reservas de salones</p>
      </div>

      <!-- Filtro -->
      <div class="mb-6">
        <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Filtrar por estado</label>
        <select v-model="filterEstado"
          class="w-64 rounded-md border-gray-300 dark:border-gray-600 dark:bg-gray-800 dark:text-white shadow-sm focus:border-[#B90A0A] focus:ring-[#B90A0A]">
          <option v-for="opt in estadoOptions" :key="opt.value" :value="opt.value">{{ opt.label }}</option>
        </select>
      </div>

      <!-- Loading -->
      <div v-if="loading" class="text-center py-12">
        <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-[#B90A0A] mx-auto"></div>
      </div>

      <!-- Tabla de Reservas -->
      <div v-else class="bg-white dark:bg-gray-800 shadow-md rounded-lg overflow-hidden">
        <table class="min-w-full divide-y divide-gray-200 dark:divide-gray-700">
          <thead class="bg-gray-50 dark:bg-gray-700">
            <tr>
              <th
                class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                Fecha</th>
              <th
                class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                Horario</th>
              <th
                class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                Salón</th>
              <th
                class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                Motivo</th>
              <th
                class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                Asistentes</th>
              <th
                class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                Usuario</th>
              <th
                class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                Estado</th>
              <th
                class="px-6 py-3 text-right text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                Acciones</th>
            </tr>
          </thead>
          <tbody class="bg-white dark:bg-gray-800 divide-y divide-gray-200 dark:divide-gray-700">
            <tr v-for="reserva in reservas" :key="reserva.id" class="hover:bg-gray-50 dark:hover:bg-gray-700">
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900 dark:text-white">
                {{ formatDate(reserva.fecha) }}
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-400">
                {{ formatTime(reserva.hora_inicio) }} - {{ formatTime(reserva.hora_fin) }}
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900 dark:text-white">
                {{ getSalonNombre(reserva.salon) }}
              </td>
              <td class="px-6 py-4 text-sm text-gray-900 dark:text-white max-w-xs truncate">
                {{ reserva.motivo }}
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-400">
                {{ reserva.numero_asistentes || 'N/A' }}
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-400">
                {{ reserva.usuario_nombre || 'N/A' }}
              </td>
              <td class="px-6 py-4 whitespace-nowrap">
                <span :class="getEstadoClass(reserva.estado)"
                  class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full">
                  {{ reserva.estado }}
                </span>
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm">
                <div class="flex justify-end space-x-2">
                  <button v-if="reserva.estado === 'pendiente'" @click="cambiarEstado(reserva.id, 'confirmada')"
                    class="text-green-600 hover:text-green-800 dark:text-green-400 dark:hover:text-green-300 font-medium transition-colors"
                    title="Aprobar">
                    <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
                    </svg>
                  </button>
                  <button v-if="reserva.estado === 'pendiente'" @click="cambiarEstado(reserva.id, 'cancelada')"
                    class="text-yellow-600 hover:text-yellow-800 dark:text-yellow-400 dark:hover:text-yellow-300 font-medium transition-colors"
                    title="Rechazar">
                    <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                    </svg>
                  </button>
                  <button @click="eliminarReserva(reserva.id, reserva.motivo)"
                    class="text-red-600 hover:text-red-800 dark:text-red-400 dark:hover:text-red-300 font-medium transition-colors"
                    title="Eliminar">
                    <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                        d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                    </svg>
                  </button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>

        <div v-if="reservas.length === 0" class="text-center py-8 text-gray-500 dark:text-gray-400">
          No hay reservas con el estado seleccionado.
        </div>

        <!-- Paginación -->
        <div
          class="px-6 py-4 bg-gray-50 dark:bg-gray-700 border-t border-gray-200 dark:border-gray-600 flex items-center justify-between">
          <span class="text-sm text-gray-500 dark:text-gray-400">
            Página {{ currentPage }} de {{ Math.ceil(totalReservas / 10) || 1 }} (Total: {{ totalReservas }})
          </span>
          <div class="flex space-x-2">
            <button @click="prevPage" :disabled="!canPrev"
              class="px-3 py-1 border border-gray-300 dark:border-gray-500 rounded-md text-sm font-medium text-gray-700 dark:text-gray-200 bg-white dark:bg-gray-800 hover:bg-gray-50 dark:hover:bg-gray-700 disabled:opacity-50 disabled:cursor-not-allowed">
              Anterior
            </button>
            <button @click="nextPage" :disabled="!canNext"
              class="px-3 py-1 border border-gray-300 dark:border-gray-500 rounded-md text-sm font-medium text-gray-700 dark:text-gray-200 bg-white dark:bg-gray-800 hover:bg-gray-50 dark:hover:bg-gray-700 disabled:opacity-50 disabled:cursor-not-allowed">
              Siguiente
            </button>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>
