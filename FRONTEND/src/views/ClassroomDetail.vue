<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import Header from '../components/Header.vue'
import { useNotificationStore } from '../stores/notification'
import api from '../services/api'

const route = useRoute()
const router = useRouter()
const notification = useNotificationStore()
const classroomId = route.params.id

const classroom = ref(null)
const loading = ref(true)
const error = ref(null)
const reservas = ref([])

// Calendar data
const currentDate = ref(new Date())
const currentWeek = ref({
  start: '',
  end: '',
  month: ''
})

const weekDays = ref([])

const generateWeek = () => {
  const days = ['Dom', 'Lun', 'Mar', 'Mié', 'Jue', 'Vie', 'Sáb']
  const months = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']

  const startOfWeek = new Date(currentDate.value)
  startOfWeek.setDate(startOfWeek.getDate() - startOfWeek.getDay() + 1) // Lunes

  weekDays.value = []
  for (let i = 0; i < 5; i++) {
    const date = new Date(startOfWeek)
    date.setDate(date.getDate() + i)

    // Obtener fecha local en formato YYYY-MM-DD
    const year = date.getFullYear()
    const month = String(date.getMonth() + 1).padStart(2, '0')
    const dayStr = String(date.getDate()).padStart(2, '0')
    const fullDate = `${year}-${month}-${dayStr}`

    weekDays.value.push({
      day: days[date.getDay()],
      date: date.getDate(),
      fullDate: fullDate,
      month: date.getMonth(),
      year: date.getFullYear()
    })
  }

  const endOfWeek = new Date(startOfWeek)
  endOfWeek.setDate(endOfWeek.getDate() + 4)

  currentWeek.value = {
    start: startOfWeek.getDate(),
    end: endOfWeek.getDate(),
    month: months[startOfWeek.getMonth()]
  }
}

const timeSlots = ref([])
const schedule = ref([])

const generateTimeSlots = () => {
  timeSlots.value = []
  for (let hour = 6; hour <= 22; hour++) {
    timeSlots.value.push(`${hour.toString().padStart(2, '0')}:00`)
  }
}

const initializeSchedule = () => {
  schedule.value = []
  const now = new Date()

  for (let i = 0; i < timeSlots.value.length; i++) {
    const daySlots = []
    const slotTimeStr = timeSlots.value[i]

    for (let j = 0; j < weekDays.value.length; j++) {
      const dayInfo = weekDays.value[j]
      const slotDateTime = new Date(`${dayInfo.fullDate}T${slotTimeStr}:00`)

      let status = 'free'

      // Si el slot es en el pasado (menor a ahora), marcar como 'past'
      if (slotDateTime < now) {
        status = 'past'
      }

      daySlots.push({ status: status, label: '', time: '' })
    }
    schedule.value.push(daySlots)
  }
}

const showModal = ref(false)
const selectedSlot = ref(null)
const reservaForm = ref({
  asignatura: '',
  notas: ''
})
const submitting = ref(false)
const asignaturas = ref([])

onMounted(async () => {
  await loadClassroom()
  generateWeek()
  generateTimeSlots()
  initializeSchedule()
  await loadReservas()
  await loadAsignaturas()
})

const loadAsignaturas = async () => {
  try {
    const response = await api.getAsignaturas()
    asignaturas.value = response.data.results || response.data
  } catch (err) {
    console.error('Error cargando asignaturas:', err)
  }
}

const loadClassroom = async () => {
  try {
    loading.value = true
    const response = await api.getSalon(classroomId)
    classroom.value = {
      id: response.data.id,
      name: response.data.nombre,
      code: response.data.codigo,
      block: response.data.bloque,
      floor: response.data.piso,
      description: response.data.descripcion || 'Salón académico',
      capacity: response.data.capacidad,
      status: response.data.estado,
      image: response.data.imagen || response.data.imagen_url,
      equipment: buildEquipment(response.data)
    }
  } catch (err) {
    console.error('Error cargando salón:', err)
    error.value = 'No se pudo cargar la información del salón'
  } finally {
    loading.value = false
  }
}

const buildEquipment = (salon) => {
  const equipment = []
  if (salon.tiene_proyector) {
    equipment.push({ icon: 'M15 10l4.553-2.276A1 1 0 0121 8.618v6.764a1 1 0 01-1.447.894L15 14M5 18h8a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z', name: 'Proyector' })
  }
  if (salon.tiene_aire_acondicionado) {
    equipment.push({ icon: 'M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6', name: 'Aire Acondicionado' })
  }
  if (salon.tiene_computadores) {
    equipment.push({ icon: 'M9.75 17L9 20l-1 1h8l-1-1-.75-3M3 13h18M5 17h14a2 2 0 002-2V5a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z', name: 'Computadores' })
  }
  if (salon.tiene_smart_tv) {
    equipment.push({ icon: 'M9.75 17L9 20l-1 1h8l-1-1-.75-3M3 13h18M5 17h14a2 2 0 002-2V5a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z', name: 'Smart TV' })
  }
  if (salon.tiene_audio) {
    equipment.push({ icon: 'M11 5.882V19.24a1.76 1.76 0 01-3.417.592l-2.147-6.15M18 13a3 3 0 100-6M5.436 13.683A4.001 4.001 0 017 6h1.832c4.1 0 7.625-1.234 9.168-3v14c-1.543-1.766-5.067-3-9.168-3H7a3.988 3.988 0 01-1.564-.317z', name: 'Sistema de Audio' })
  }
  if (salon.tiene_wifi) {
    equipment.push({ icon: 'M8.111 16.404a5.5 5.5 0 017.778 0M12 20h.01m-7.08-7.071c3.904-3.905 10.236-3.905 14.141 0M1.394 9.393c5.857-5.857 15.355-5.857 21.213 0', name: 'WiFi Alta Velocidad' })
  }
  return equipment
}

const loadReservas = async () => {
  try {
    const response = await api.getReservasPorSalon(classroomId)
    reservas.value = response.data.results || response.data
    updateScheduleWithReservas()
  } catch (err) {
    console.error('Error cargando reservas:', err)
  }
}

const updateScheduleWithReservas = () => {
  reservas.value.forEach(reserva => {
    // Filtrar reservas canceladas (case insensitive)
    if (reserva.estado && reserva.estado.toLowerCase() === 'cancelada') return

    const dayIndex = weekDays.value.findIndex(d => d.fullDate === reserva.fecha)
    if (dayIndex === -1) return

    const horaInicio = parseInt(reserva.hora_inicio.split(':')[0])
    const horaFin = parseInt(reserva.hora_fin.split(':')[0])

    for (let hour = horaInicio; hour < horaFin; hour++) {
      const timeIndex = timeSlots.value.findIndex(t => t.startsWith(hour.toString().padStart(2, '0')))
      if (timeIndex !== -1 && schedule.value[timeIndex] && schedule.value[timeIndex][dayIndex]) {
        schedule.value[timeIndex][dayIndex] = {
          status: 'occupied',
          label: reserva.asignatura || 'Reservado',
          reservaId: reserva.id
        }
      }
    }
  })
}

const clearSelection = () => {
  schedule.value.forEach((row, rIdx) => {
    row.forEach((cell, cIdx) => {
      if (cell.status === 'selected') {
        schedule.value[rIdx][cIdx] = { status: 'free', label: '', time: '' }
      }
    })
  })
  selectedSlot.value = null
}

const updateSelectedSlotObject = (startRow, endRow, col) => {
  // Asumimos timeSlots formato "HH:00"
  const startTimeStr = timeSlots.value[startRow]
  // Calcular fin
  let endTimeStr = '19:00'
  if (endRow + 1 < timeSlots.value.length) {
    endTimeStr = timeSlots.value[endRow + 1]
  } else {
    // Si es el último slot, sumar una hora
    const lastTime = parseInt(timeSlots.value[endRow].split(':')[0])
    endTimeStr = `${(lastTime + 1).toString().padStart(2, '0')}:00`
  }

  selectedSlot.value = {
    timeIndex: startRow,
    dayIndex: col,
    time: startTimeStr,
    endTime: endTimeStr,
    day: weekDays.value[col],
    fecha: weekDays.value[col].fullDate
  }

  // Actualizar visualmente todos los slots seleccionados
  for (let r = startRow; r <= endRow; r++) {
    schedule.value[r][col] = {
      status: 'selected',
      label: 'Seleccionado',
      time: `${startTimeStr} - ${endTimeStr}`
    }
  }
}

const updateSelectionVisuals = (startRow, endRow, col) => {
  // Limpiar solo la columna actual (o reiniciar toda la tabla si queremos ser estrictos con 1 selección)
  schedule.value.forEach((row, idx) => {
    // Como solo permitimos selección en un día a la vez
    if (row[col].status === 'selected') {
      row[col] = { status: 'free', label: '', time: '' }
    }
  })

  updateSelectedSlotObject(startRow, endRow, col)
}

const removeSlot = (timeIndex, dayIndex) => {
  // Obtenemos los índices seleccionados actuales para ese día
  let selectedIndices = []
  schedule.value.forEach((row, rIdx) => {
    if (row[dayIndex] && row[dayIndex].status === 'selected') {
      selectedIndices.push(rIdx)
    }
  })

  // Si no hay selección o solo hay uno, limpiar todo
  if (selectedIndices.length <= 1) {
    clearSelection()
    return
  }

  const minRow = Math.min(...selectedIndices)
  const maxRow = Math.max(...selectedIndices)

  const isFirst = timeIndex === minRow
  const isLast = timeIndex === maxRow

  if (isFirst) {
    // Quitar el primero, mantener el resto
    updateSelectionVisuals(minRow + 1, maxRow, dayIndex)
  } else if (isLast) {
    // Quitar el último
    updateSelectionVisuals(minRow, maxRow - 1, dayIndex)
  } else {
    // Es del medio. Usuario quiere quitar una del medio.
    notification.warning("Para mantener la reserva continua, por favor elimina horas desde el inicio o el final de la selección.")
  }
}

const handleSlotClick = (timeIndex, dayIndex, slot) => {
  // Si clic en seleccionado, manejar eliminación (opcional, si queremos que clic en celda también elimine)
  // Pero el usuario pidió botón eliminar específico. Dejemos que el slot seleccionado
  // solo actúe si se hace clic en una celda LIBRE para extender/mover.
  // Sin embargo, para consistencia, si hace clic en "selected", no haremos nada aquí,
  // delegando la acción al botón 'X'.
  if (slot.status !== 'free' && slot.status !== 'selected') return
  if (slot.status === 'selected') return // Acción manejada por botón X

  // 1. Encontrar selección actual en este día
  let currentSelection = []
  schedule.value.forEach((row, rIdx) => {
    if (row[dayIndex] && row[dayIndex].status === 'selected') {
      currentSelection.push(rIdx)
    }
  })

  // Verificar si hay selección en OTROS días y borrarla
  let otherDaySelection = false
  schedule.value.forEach((row, rIdx) => {
    row.forEach((cell, cIdx) => {
      if (cell.status === 'selected' && cIdx !== dayIndex) {
        otherDaySelection = true
      }
    })
  })

  if (otherDaySelection) {
    clearSelection()
    currentSelection = []
  }

  // 2. Lógica de selección
  if (currentSelection.length === 0) {
    // Nueva selección
    updateSelectedSlotObject(timeIndex, timeIndex, dayIndex)
  } else {
    // Extender o reiniciar selección en el mismo día
    const minRow = Math.min(...currentSelection)
    const maxRow = Math.max(...currentSelection)

    const newMin = Math.min(minRow, timeIndex)
    const newMax = Math.max(maxRow, timeIndex)

    // Verificar disponibilidad en el nuevo rango
    let isRangeFree = true
    for (let r = newMin; r <= newMax; r++) {
      const cell = schedule.value[r][dayIndex]
      if (cell.status !== 'free' && cell.status !== 'selected') {
        isRangeFree = false
        break
      }
    }

    if (isRangeFree) {
      // Limpiar para refrescar
      schedule.value.forEach((row, rIdx) => {
        if (row[dayIndex].status === 'selected') {
          row[dayIndex] = { status: 'free', label: '', time: '' }
        }
      })
      updateSelectedSlotObject(newMin, newMax, dayIndex)
    } else {
      // Alertar sobre espacio
      notification.warning("No se pueden agendar reservas con espacios ocupados entre medias. Se iniciará una nueva selección.")
      // No continuo, reiniciar
      clearSelection()
      updateSelectedSlotObject(timeIndex, timeIndex, dayIndex)
    }
  }
}

const confirmReservation = () => {
  if (!selectedSlot.value) {
    notification.warning('Por favor, seleccione un horario primero')
    return
  }
  showModal.value = true
}

const submitReservation = async () => {
  if (!reservaForm.value.asignatura) {
    notification.warning('Por favor, ingrese la asignatura')
    return
  }

  try {
    submitting.value = true
    const data = {
      salon: classroomId,
      fecha: selectedSlot.value.fecha,
      hora_inicio: selectedSlot.value.time,
      hora_fin: selectedSlot.value.endTime,
      motivo: reservaForm.value.asignatura,
      descripcion: reservaForm.value.notas || '',
      numero_asistentes: 1
    }

    await api.createReserva(data)
    showModal.value = false
    reservaForm.value = { asignatura: '', notas: '' }
    selectedSlot.value = null

    // Recargar reservas
    await loadReservas()
    initializeSchedule()
    updateScheduleWithReservas()

    notification.success('¡Reserva creada exitosamente!')
  } catch (err) {
    console.error('Error creando reserva:', err)
    notification.error(err.response?.data?.error || err.response?.data?.detail || 'Error al crear la reserva')
  } finally {
    submitting.value = false
  }
}

const cancelarReserva = async (reservaId) => {
  if (!confirm('¿Está seguro de que desea eliminar esta reserva permanentemente?')) return

  try {
    await api.cancelarReserva(reservaId)
    await loadReservas()
    initializeSchedule()
    updateScheduleWithReservas()
    notification.success('Reserva eliminada exitosamente')
  } catch (err) {
    console.error('Error eliminando reserva:', err)
    notification.error('Error al eliminar la reserva')
  }
}

const navigateWeek = (direction) => {
  currentDate.value.setDate(currentDate.value.getDate() + (direction * 7))
  generateWeek()
  initializeSchedule()
  updateScheduleWithReservas()
}
</script>

<template>
  <div class="min-h-screen bg-white dark:bg-gray-900 flex flex-col">
    <Header />

    <!-- Loading State -->
    <div v-if="loading" class="flex-grow flex items-center justify-center">
      <div class="text-center">
        <div class="animate-spin rounded-full h-16 w-16 border-t-2 border-b-2 border-[#B90A0A] mx-auto"></div>
        <p class="mt-4 text-gray-600 dark:text-gray-400">Cargando información...</p>
      </div>
    </div>

    <!-- Error State -->
    <div v-else-if="error" class="flex-grow flex items-center justify-center">
      <div class="text-center">
        <p class="text-red-600 dark:text-red-400">{{ error }}</p>
        <router-link to="/salones" class="mt-4 inline-block text-[#B90A0A] hover:underline">
          Volver a la lista
        </router-link>
      </div>
    </div>

    <main v-else class="flex-grow max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <!-- Breadcrumb -->
      <nav class="flex mb-6 text-sm text-gray-500 dark:text-gray-400">
        <ol class="inline-flex items-center space-x-1 md:space-x-3">
          <li class="inline-flex items-center">
            <router-link to="/" class="inline-flex items-center hover:text-[#B90A0A] dark:hover:text-red-400">
              <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                  d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6" />
              </svg>
              Inicio
            </router-link>
          </li>
          <li>
            <div class="flex items-center">
              <svg class="w-4 h-4 text-gray-400 mx-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
              </svg>
              <router-link to="/salones" class="hover:text-[#B90A0A] dark:hover:text-red-400">Reservas</router-link>
            </div>
          </li>
          <li>
            <div class="flex items-center">
              <svg class="w-4 h-4 text-gray-400 mx-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
              </svg>
              <span class="text-gray-900 dark:text-white font-medium">{{ classroom.name }}</span>
            </div>
          </li>
        </ol>
      </nav>

      <!-- Main Content Grid -->
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <!-- Left Sidebar: Classroom Info -->
        <div class="lg:col-span-1 space-y-6">
          <div
            class="bg-white dark:bg-gray-800 rounded-lg shadow-md overflow-hidden border border-gray-200 dark:border-gray-700">
            <!-- Image -->
            <div class="relative h-48 bg-gray-300">
              <img :src="classroom.image" :alt="classroom.name" class="w-full h-full object-cover" />
              <div
                class="absolute top-2 right-2 bg-green-500 text-white text-xs font-bold px-2 py-1 rounded-full shadow-sm">
                DISPONIBLE
              </div>
            </div>

            <!-- Info -->
            <div class="p-6">
              <h2 class="text-2xl font-bold text-gray-900 dark:text-white mb-2">{{ classroom.name }}</h2>
              <p class="text-gray-500 dark:text-gray-400 text-sm mb-4">
                {{ classroom.block }}, {{ classroom.floor }}. {{ classroom.description }}
              </p>

              <div class="flex items-center mb-4 text-gray-700 dark:text-gray-300">
                <svg class="w-5 h-5 text-[#B90A0A] mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                    d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
                </svg>
                <span class="font-medium">Capacidad: {{ classroom.capacity }} Personas</span>
              </div>

              <hr class="border-gray-200 dark:border-gray-600 my-4" />

              <h3 class="text-sm font-semibold text-gray-900 dark:text-white uppercase tracking-wider mb-3">
                Equipamiento
              </h3>
              <ul class="space-y-2">
                <li v-for="(item, index) in classroom.equipment" :key="index"
                  class="flex items-center text-sm text-gray-600 dark:text-gray-300">
                  <svg class="w-5 h-5 text-gray-400 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" :d="item.icon" />
                  </svg>
                  {{ item.name }}
                </li>
              </ul>
            </div>

            <!-- Action Button -->
            <div class="bg-gray-50 dark:bg-gray-700 px-6 py-4 border-t border-gray-200 dark:border-gray-600">
              <button @click="confirmReservation"
                class="w-full bg-[#B90A0A] hover:bg-[#8f0606] text-white font-bold py-3 px-4 rounded shadow transition transform active:scale-95 flex justify-center items-center">
                <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                    d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                </svg>
                Confirmar Reserva
              </button>
            </div>
          </div>

          <!-- Info Box -->
          <div class="bg-blue-50 dark:bg-blue-900/20 border border-blue-100 dark:border-blue-900 rounded-lg p-4">
            <div class="flex items-start">
              <svg class="w-5 h-5 text-blue-500 mr-3 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                  d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
          </div>
        </div>

        <!-- Right Section: Calendar -->
        <div class="lg:col-span-2">
          <div
            class="bg-white dark:bg-gray-800 rounded-lg shadow-md border border-gray-200 dark:border-gray-700 h-full flex flex-col">
            <!-- Calendar Header -->
            <div
              class="p-4 border-b border-gray-200 dark:border-gray-600 flex flex-col sm:flex-row justify-between items-center bg-gray-50 dark:bg-gray-700 rounded-t-lg">
              <div class="flex items-center space-x-4 mb-3 sm:mb-0">
                <button @click="navigateWeek(-1)"
                  class="p-1 rounded-full hover:bg-gray-200 dark:hover:bg-gray-600 text-gray-600 dark:text-gray-300">
                  <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
                  </svg>
                </button>
                <h2 class="text-lg font-bold text-gray-800 dark:text-white">
                  Semana del {{ currentWeek.start }} - {{ currentWeek.end }} {{ currentWeek.month }}
                </h2>
                <button @click="navigateWeek(1)"
                  class="p-1 rounded-full hover:bg-gray-200 dark:hover:bg-gray-600 text-gray-600 dark:text-gray-300">
                  <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
                  </svg>
                </button>
              </div>

              <!-- Legend -->
              <div class="flex items-center space-x-2">
                <div class="flex items-center mr-4">
                  <span class="w-3 h-3 rounded-full bg-green-100 border border-green-500 mr-2"></span>
                  <span class="text-xs text-gray-500 dark:text-gray-400">Libre</span>
                </div>
                <div class="flex items-center mr-4">
                  <span class="w-3 h-3 rounded-full bg-red-100 border border-red-500 mr-2"></span>
                  <span class="text-xs text-gray-500 dark:text-gray-400">Ocupado</span>
                </div>
                <div class="flex items-center">
                  <span class="w-3 h-3 rounded-full bg-blue-500 mr-2"></span>
                  <span class="text-xs text-gray-500 dark:text-gray-400">Tu Selección</span>
                </div>
              </div>
            </div>

            <!-- Calendar Grid -->
            <div class="flex-grow overflow-auto p-4">
              <div class="min-w-[600px]">
                <!-- Day Headers -->
                <div class="grid grid-cols-6 gap-2 mb-2">
                  <div class="text-center"></div>
                  <div v-for="day in weekDays" :key="day.date"
                    :class="day.date === '16' ? 'border-b-2 border-[#B90A0A]' : 'border-b-2 border-transparent'"
                    class="text-center font-semibold text-gray-700 dark:text-gray-300 pb-2">
                    {{ day.day }} {{ day.date }}
                  </div>
                </div>

                <!-- Time Slots -->
                <div class="relative space-y-2">
                  <div v-for="(slots, timeIndex) in schedule" :key="timeIndex" class="grid grid-cols-6 gap-2 h-16">
                    <!-- Time Label -->
                    <div class="text-right pr-4 text-xs text-gray-400 -mt-2">
                      {{ timeSlots[timeIndex] }}
                    </div>

                    <!-- Day Slots -->
                    <template v-for="(slot, dayIndex) in slots" :key="`${timeIndex}-${dayIndex}`">
                      <!-- Skip cells (for rowspan/colspan) -->
                      <div v-if="slot.status === 'skip'" class="hidden"></div>

                      <!-- Past time -->
                      <div v-else-if="slot.status === 'past'"
                        class="bg-gray-200 dark:bg-gray-800 border border-gray-300 dark:border-gray-700 rounded p-1 flex items-center justify-center cursor-not-allowed opacity-60"
                        title="Horario pasado">
                      </div>

                      <!-- Occupied -->
                      <div v-else-if="slot.status === 'occupied'" :class="slot.rowspan ? 'row-span-2' : ''"
                        class="bg-red-50 dark:bg-red-900/30 border border-red-200 dark:border-red-800 rounded p-1 flex items-center justify-center cursor-not-allowed opacity-75">
                        <span class="text-[10px] text-red-800 dark:text-red-300 font-bold text-center">
                          {{ slot.label }}
                        </span>
                      </div>

                      <!-- Selected/Reserved by user -->
                      <div v-else-if="slot.status === 'selected'"
                        class="bg-[#B90A0A] text-white border border-[#B90A0A] rounded p-2 flex flex-col justify-center shadow-lg transform scale-105 z-10 cursor-pointer relative group">
                        <button @click.stop="removeSlot(timeIndex, dayIndex)"
                          class="absolute -top-2 -right-2 bg-white text-[#B90A0A] rounded-full w-5 h-5 flex items-center justify-center shadow cursor-pointer hover:bg-gray-100">
                          <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                              d="M6 18L18 6M6 6l12 12" />
                          </svg>
                        </button>
                        <span class="text-xs font-bold text-center">{{ slot.label }}</span>
                        <span class="text-[10px] text-center opacity-80">{{ slot.time }}</span>
                      </div>

                      <!-- Reserved by admin -->
                      <div v-else-if="slot.status === 'reserved'" :class="slot.colspan ? 'col-span-2' : ''"
                        class="bg-gray-100 dark:bg-gray-700 border border-gray-300 dark:border-gray-600 rounded p-1 flex items-center justify-center cursor-not-allowed opacity-50">
                        <span class="text-[10px] text-gray-500 font-bold text-center">
                          {{ slot.label }}
                        </span>
                      </div>

                      <!-- Free/Available -->
                      <button v-else @click="handleSlotClick(timeIndex, dayIndex, slot)"
                        class="group bg-green-50 dark:bg-green-900/10 border border-green-200 dark:border-green-800/30 rounded hover:border-[#B90A0A] hover:bg-white dark:hover:bg-gray-700 transition flex items-center justify-center relative">
                        <svg class="w-5 h-5 text-[#B90A0A] hidden group-hover:block" fill="none" stroke="currentColor"
                          viewBox="0 0 24 24">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
                        </svg>
                      </button>
                    </template>
                  </div>
                </div>
              </div>
            </div>

            <!-- Calendar Footer -->
            <div
              class="p-4 bg-gray-50 dark:bg-gray-700 rounded-b-lg border-t border-gray-200 dark:border-gray-600 text-right">
              <span class="text-xs text-gray-500 dark:text-gray-400 italic">
                Haga clic y arrastre para seleccionar múltiples horas
              </span>
            </div>
          </div>
        </div>
      </div>
    </main>

    <!-- Footer -->
    <footer class="bg-white dark:bg-gray-800 border-t border-gray-200 dark:border-gray-700 mt-auto">
      <div class="max-w-7xl mx-auto py-8 px-4 sm:px-6 lg:px-8 text-center">
        <h5 class="text-lg font-bold text-gray-800 dark:text-gray-200 mb-4">
          Fundación de Estudios Superiores Comfanorte <span class="text-[#B90A0A]">FESC</span>. "Comprometidos Con
          Calidad y
          Excelencia"
        </h5>
        <div class="flex flex-col md:flex-row justify-center space-y-4 md:space-y-0 md:space-x-4">
          <a href="#"
            class="bg-[#B90A0A] hover:bg-[#8f0606] text-white px-6 py-2 rounded-md text-sm font-medium transition">
            Carnet Digital
          </a>
          <a href="#"
            class="bg-[#B90A0A] hover:bg-[#8f0606] text-white px-6 py-2 rounded-md text-sm font-medium transition">
            Ver Política de Protección de Datos
          </a>
        </div>
        <p class="mt-8 text-xs text-gray-400">© 2023 GECOS FESC. Todos los derechos reservados.</p>
      </div>
    </footer>

    <!-- Confirmation Modal -->
    <div v-if="showModal" class="fixed inset-0 z-50 overflow-y-auto" @click.self="showModal = false">
      <div class="flex items-end justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:block sm:p-0">
        <div class="fixed inset-0 bg-gray-500 bg-opacity-75 transition-opacity"></div>

        <div
          class="inline-block align-bottom bg-white dark:bg-gray-800 rounded-lg text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-lg sm:w-full">
          <div class="bg-white dark:bg-gray-800 px-4 pt-5 pb-4 sm:p-6 sm:pb-4">
            <div class="sm:flex sm:items-start">
              <div
                class="mx-auto flex-shrink-0 flex items-center justify-center h-12 w-12 rounded-full bg-red-100 sm:mx-0 sm:h-10 sm:w-10">
                <svg class="w-6 h-6 text-[#B90A0A]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                    d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                </svg>
              </div>
              <div class="mt-3 text-center sm:mt-0 sm:ml-4 sm:text-left w-full">
                <h3 class="text-lg leading-6 font-medium text-gray-900 dark:text-white">
                  Confirmar Reserva
                </h3>
                <div class="mt-2">
                  <p class="text-sm text-gray-500 dark:text-gray-400 mb-4" v-if="selectedSlot">
                    Está a punto de reservar el <strong>{{ classroom.name }}</strong> para el <strong>{{
                      selectedSlot.day.day }} {{ selectedSlot.day.date }}</strong> de <strong>{{ selectedSlot.time
                      }}</strong> a <strong>{{ selectedSlot.endTime }}</strong>.
                  </p>
                  <form @submit.prevent="submitReservation" class="space-y-4">
                    <div>
                      <label class="block text-sm font-medium text-gray-700 dark:text-gray-300">Asignatura *</label>
                      <select v-model="reservaForm.asignatura" required
                        class="mt-1 block w-full pl-3 pr-10 py-2 text-base border-gray-300 dark:border-gray-600 dark:bg-gray-700 dark:text-white focus:outline-none focus:ring-[#B90A0A] focus:border-[#B90A0A] sm:text-sm rounded-md">
                        <option value="" disabled>Seleccione una asignatura</option>
                        <option v-for="asignatura in asignaturas" :key="asignatura.id" :value="asignatura.nombre">
                          {{ asignatura.nombre }} <span v-if="asignatura.codigo">({{ asignatura.codigo }})</span>
                        </option>
                      </select>
                    </div>
                    <div>
                      <label class="block text-sm font-medium text-gray-700 dark:text-gray-300">Notas
                        Adicionales</label>
                      <textarea v-model="reservaForm.notas" rows="3"
                        class="shadow-sm focus:ring-[#B90A0A] focus:border-[#B90A0A] mt-1 block w-full sm:text-sm border border-gray-300 dark:border-gray-600 dark:bg-gray-700 dark:text-white rounded-md"
                        placeholder="Necesito proyector extra..."></textarea>
                    </div>
                  </form>
                </div>
              </div>
            </div>
          </div>
          <div class="bg-gray-50 dark:bg-gray-700 px-4 py-3 sm:px-6 sm:flex sm:flex-row-reverse">
            <button @click="submitReservation" :disabled="submitting" type="button"
              class="w-full inline-flex justify-center rounded-md border border-transparent shadow-sm px-4 py-2 bg-[#B90A0A] text-base font-medium text-white hover:bg-[#8f0606] focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500 sm:ml-3 sm:w-auto sm:text-sm disabled:opacity-50 disabled:cursor-not-allowed">
              {{ submitting ? 'Guardando...' : 'Confirmar' }}
            </button>
            <button @click="showModal = false" :disabled="submitting" type="button"
              class="mt-3 w-full inline-flex justify-center rounded-md border border-gray-300 dark:border-gray-500 shadow-sm px-4 py-2 bg-white dark:bg-gray-800 text-base font-medium text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 sm:mt-0 sm:ml-3 sm:w-auto sm:text-sm">
              Cancelar
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
