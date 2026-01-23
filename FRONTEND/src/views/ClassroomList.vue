<script setup>
import { ref, onMounted, watch } from 'vue'
import Header from '../components/Header.vue'
import AdminNotifications from '../components/AdminNotifications.vue'
import ClassroomCard from '../components/ClassroomCard.vue'
import api from '../services/api'

const classrooms = ref([])
const loading = ref(true)
const error = ref(null)

// Filtros
const filters = ref({
  tipo: '',
  bloque: '',
  estado: ''
})

const tiposDisponibles = [
  { value: '', label: 'Todos' },
  { value: 'aula', label: 'Aula' },
  { value: 'laboratorio', label: 'Laboratorio' },
  { value: 'auditorio', label: 'Auditorio' },
  { value: 'sala_conferencias', label: 'Sala de Conferencias' }
]

const estadosDisponibles = [
  { value: '', label: 'Todos' },
  { value: 'disponible', label: 'Disponible' },
  { value: 'ocupado', label: 'Ocupado' },
  { value: 'mantenimiento', label: 'Mantenimiento' }
]

onMounted(async () => {
  await loadClassrooms()
})

// Observar cambios en los filtros
watch(() => filters.value.tipo, () => {
  loadClassrooms()
})

watch(() => filters.value.estado, () => {
  loadClassrooms()
})

watch(() => filters.value.bloque, () => {
  loadClassrooms()
})

const loadClassrooms = async () => {
  try {
    loading.value = true
    error.value = null

    const params = {}
    if (filters.value.tipo) params.tipo = filters.value.tipo
    if (filters.value.bloque) params.bloque = filters.value.bloque
    if (filters.value.estado) params.estado = filters.value.estado

    // Enviar fecha actual local para obtener el horario correcto
    const today = new Date()
    const year = today.getFullYear()
    const month = String(today.getMonth() + 1).padStart(2, '0')
    const day = String(today.getDate()).padStart(2, '0')
    params.fecha = `${year}-${month}-${day}`

    const response = await api.getSalones(params)
    // El backend devuelve una respuesta paginada con 'results'
    const salones = response.data.results || response.data
    classrooms.value = salones.map(salon => ({
      id: salon.id,
      name: salon.nombre,
      floor: salon.piso,
      capacity: salon.capacidad,
      status: salon.status,
      statusText: salon.statusText,
      statusColor: salon.statusColor,
      image: salon.imagen || salon.imagen_url,
      bloque: salon.bloque,
      tipo: salon.tipo,
      features: salon.features,
      schedule: salon.schedule
    }))
  } catch (err) {
    console.error('Error completo:', err)
    console.error('Error response:', err.response)
    error.value = err.response?.data?.detail || err.message || 'Error al cargar los salones'
  } finally {
    loading.value = false
  }
}

const getStatusText = (status) => {
  const statusMap = {
    'disponible': 'Disponible',
    'ocupado': 'Ocupado',
    'mantenimiento': 'Mantenimiento'
  }
  return statusMap[status] || status
}

const getStatusColor = (status) => {
  const colorMap = {
    'disponible': '#10b981',
    'ocupado': '#eab308',
    'mantenimiento': '#ef4444'
  }
  return colorMap[status] || '#6b7280'
}

const getFeatures = (salon) => {
  const features = []
  if (salon.tiene_aire_acondicionado) {
    features.push({ name: 'Aire Acondicionado', icon: 'M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6' })
  }
  if (salon.tiene_proyector) {
    features.push({ name: 'Proyector', icon: 'M15 10l4.553-2.276A1 1 0 0121 8.618v6.764a1 1 0 01-1.447.894L15 14M5 18h8a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z' })
  }
  if (salon.tiene_computadores) {
    features.push({ name: 'Computadores', icon: 'M9.75 17L9 20l-1 1h8l-1-1-.75-3M3 13h18M5 17h14a2 2 0 002-2V5a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z' })
  }
  if (salon.tiene_smart_tv) {
    features.push({ name: 'Smart TV', icon: 'M9.75 17L9 20l-1 1h8l-1-1-.75-3M3 13h18M5 17h14a2 2 0 002-2V5a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z' })
  }
  if (salon.tiene_audio) {
    features.push({ name: 'Sistema de Audio', icon: 'M11 5.882V19.24a1.76 1.76 0 01-3.417.592l-2.147-6.15M18 13a3 3 0 100-6M5.436 13.683A4.001 4.001 0 017 6h1.832c4.1 0 7.625-1.234 9.168-3v14c-1.543-1.766-5.067-3-9.168-3H7a3.988 3.988 0 01-1.564-.317z' })
  }
  if (salon.tiene_wifi) {
    features.push({ name: 'WiFi', icon: 'M8.111 16.404a5.5 5.5 0 017.778 0M12 20h.01m-7.08-7.071c3.904-3.905 10.236-3.905 14.141 0M1.394 9.393c5.857-5.857 15.355-5.857 21.213 0' })
  }
  return features
}

const generateSchedule = () => {
  // Generar un horario de 10 slots (8am - 6pm)
  const schedule = []
  for (let i = 0; i < 10; i++) {
    schedule.push({
      time: `${8 + i}:00`,
      status: Math.random() > 0.3 ? 'free' : 'occupied'
    })
  }
  return schedule
}
</script>

<template>
  <div class="min-h-screen bg-white dark:bg-gray-900 flex flex-col">
    <Header />
    <AdminNotifications />

    <main class="flex-grow max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 md:pt-4 pb-12 w-full">
      <!-- Title -->
      <div class="mb-8 flex flex-col md:flex-row md:items-end justify-between gap-4">
        <div>
          <h1 class="text-3xl font-display font-bold text-gray-900 dark:text-white mb-2">Disponibilidad de Salones</h1>
          <p class="text-gray-600 dark:text-gray-400">Gestione y reserve los espacios académicos para sus clases.</p>
        </div>
      </div>

      <!-- Filters -->
      <section
        class="bg-white dark:bg-gray-800 rounded-xl shadow-md p-6 mb-8 border border-gray-200 dark:border-gray-700 relative overflow-hidden">
        <div class="absolute top-0 left-0 w-1 h-full bg-[#B90A0A]"></div>

        <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
          <!-- Tipo -->
          <div class="relative">
            <label class="block text-xs font-semibold text-gray-500 dark:text-gray-400 uppercase tracking-wider mb-1">
              Tipo de Salón
            </label>
            <select v-model="filters.tipo"
              class="block w-full pl-3 pr-3 py-2.5 text-base border-gray-300 dark:border-gray-600 focus:outline-none focus:ring-[#B90A0A] focus:border-[#B90A0A] sm:text-sm rounded-lg bg-gray-50 dark:bg-gray-700 text-gray-900 dark:text-white">
              <option v-for="tipo in tiposDisponibles" :key="tipo.value" :value="tipo.value">
                {{ tipo.label }}
              </option>
            </select>
          </div>

          <!-- Estado -->
          <div class="relative">
            <label class="block text-xs font-semibold text-gray-500 dark:text-gray-400 uppercase tracking-wider mb-1">
              Estado
            </label>
            <select v-model="filters.estado"
              class="block w-full pl-3 pr-3 py-2.5 text-base border-gray-300 dark:border-gray-600 focus:outline-none focus:ring-[#B90A0A] focus:border-[#B90A0A] sm:text-sm rounded-lg bg-gray-50 dark:bg-gray-700 text-gray-900 dark:text-white">
              <option v-for="estado in estadosDisponibles" :key="estado.value" :value="estado.value">
                {{ estado.label }}
              </option>
            </select>
          </div>

          <!-- Bloque -->
          <div class="relative">
            <label class="block text-xs font-semibold text-gray-500 dark:text-gray-400 uppercase tracking-wider mb-1">
              Bloque
            </label>
            <input v-model="filters.bloque" type="text" placeholder="Ej: Bloque A"
              class="block w-full pl-3 pr-3 py-2.5 text-base border-gray-300 dark:border-gray-600 focus:outline-none focus:ring-[#B90A0A] focus:border-[#B90A0A] sm:text-sm rounded-lg bg-gray-50 dark:bg-gray-700 text-gray-900 dark:text-white" />
          </div>
        </div>

        <div class="mt-4 text-xs text-gray-500 dark:text-gray-400 italic">
          Los filtros se aplican automáticamente al cambiar los valores
        </div>
      </section>

      <!-- Loading State -->
      <div v-if="loading" class="text-center py-12">
        <div class="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-primary"></div>
        <p class="mt-4 text-gray-600 dark:text-gray-400">Cargando salones...</p>
      </div>

      <!-- Error State -->
      <div v-else-if="error"
        class="bg-red-50 dark:bg-red-900/30 border border-red-400 dark:border-red-700 rounded-lg p-6 mb-6">
        <div class="flex items-start">
          <svg class="w-6 h-6 text-red-700 dark:text-red-400 mr-3 flex-shrink-0" fill="none" stroke="currentColor"
            viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
              d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
          </svg>
          <div class="flex-1">
            <h3 class="text-red-800 dark:text-red-300 font-semibold mb-2">Error al cargar los salones</h3>
            <p class="text-red-700 dark:text-red-400 text-sm">{{ error }}</p>
            <button @click="loadClassrooms"
              class="mt-4 bg-red-600 hover:bg-red-700 text-white px-4 py-2 rounded-lg text-sm transition-colors">
              Reintentar
            </button>
          </div>
        </div>
      </div>

      <!-- Empty State -->
      <div v-else-if="classrooms.length === 0" class="text-center py-12">
        <svg class="mx-auto h-12 w-12 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
            d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
        </svg>
        <p class="mt-4 text-gray-600 dark:text-gray-400">No se encontraron salones</p>
      </div>

      <!-- Classrooms Grid -->
      <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <ClassroomCard v-for="classroom in classrooms" :key="classroom.id" :classroom="classroom" />
      </div>
    </main>

    <!-- Footer -->
    <footer class="bg-white dark:bg-gray-800 border-t border-gray-200 dark:border-gray-700 mt-auto">
      <div class="max-w-7xl mx-auto py-8 px-4 sm:px-6 lg:px-8">
        <div class="flex flex-col md:flex-row justify-between items-center">
          <div class="mb-4 md:mb-0 text-center md:text-left">
            <p class="text-sm font-semibold text-gray-600 dark:text-gray-300">
              © 2026 Fundación de Estudios Superiores Comfanorte FESC.
            </p>
            <p class="text-xs text-gray-400 dark:text-gray-500 mt-1 italic">
              "Comprometidos Con Calidad y Excelencia"
            </p>
          </div>
        </div>
      </div>
    </footer>
  </div>
</template>
