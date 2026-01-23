<script setup>
import { ref, onMounted } from 'vue'
import Header from '../components/Header.vue'
import { useNotificationStore } from '../stores/notification'
import api from '../services/api'

const notification = useNotificationStore()
const reservas = ref([])
const loading = ref(true)

onMounted(async () => {
    try {
        const response = await api.getMisReservas()
        reservas.value = response.data
    } catch (err) {
        console.error('Error cargando reservas:', err)
    } finally {
        loading.value = false
    }
})

const cancelarReserva = async (reservaId) => {
    if (!confirm('¿Está seguro de que desea cancelar su reserva?')) return

    try {
        await api.cancelarReserva(reservaId)
        // Recargar
        const response = await api.getMisReservas()
        reservas.value = response.data
        notification.success('Reserva cancelada exitosamente')
    } catch (err) {
        console.error('Error cancelando reserva:', err)
        notification.error(err.response?.data?.error || 'Error al cancelar la reserva')
    }
}

const formatDate = (dateStr) => {
    return new Date(dateStr + 'T00:00:00').toLocaleDateString('es-CO', {
        weekday: 'long', year: 'numeric', month: 'long', day: 'numeric'
    })
}

const getEstadoClass = (estado) => {
    const classes = {
        pendiente: 'bg-yellow-100 text-yellow-800',
        confirmada: 'bg-green-100 text-green-800',
        cancelada: 'bg-gray-100 text-gray-800',
        completada: 'bg-blue-100 text-blue-800'
    }
    return classes[estado] || 'bg-gray-100 text-gray-800'
}
</script>

<template>
    <div class="min-h-screen bg-white dark:bg-gray-900">
        <Header />

        <main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
            <h1 class="text-3xl font-bold text-gray-900 dark:text-white mb-6">Mis Reservas</h1>

            <div v-if="loading" class="text-center py-12">
                <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-[#B90A0A] mx-auto"></div>
            </div>

            <div v-else-if="reservas.length === 0"
                class="text-center py-12 bg-white dark:bg-gray-800 rounded-lg shadow border border-gray-200 dark:border-gray-700">
                <svg class="w-16 h-16 text-gray-300 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                        d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                </svg>
                <p class="text-gray-500 dark:text-gray-400 text-lg">No tienes reservas activas.</p>
                <router-link to="/salones" class="mt-4 inline-block text-[#B90A0A] font-bold hover:underline">
                    ¡Reserva un salón ahora!
                </router-link>
            </div>

            <div v-else class="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
                <div v-for="reserva in reservas" :key="reserva.id"
                    class="bg-white dark:bg-gray-800 rounded-lg shadow-md border border-gray-200 dark:border-gray-700 overflow-hidden">
                    <div class="p-5">
                        <div class="flex justify-between items-start mb-4">
                            <span :class="getEstadoClass(reserva.estado)"
                                class="px-2 py-1 text-xs font-bold rounded-full uppercase tracking-wide">
                                {{ reserva.estado }}
                            </span>
                            <span class="text-sm text-gray-500 dark:text-gray-400 font-mono">
                                {{ reserva.hora_inicio.substring(0, 5) }} - {{ reserva.hora_fin.substring(0, 5) }}
                            </span>
                        </div>

                        <h3 class="text-xl font-bold text-gray-900 dark:text-white mb-1">
                            {{ reserva.salon_detalle?.nombre || 'Salón Desconocido' }}
                        </h3>
                        <p class="text-sm text-gray-500 dark:text-gray-400 mb-4 capitalize">
                            {{ formatDate(reserva.fecha) }}
                        </p>

                        <div class="border-t border-gray-100 dark:border-gray-700 pt-4 mb-4">
                            <div class="flex items-start mb-2">
                                <span class="text-gray-400 mr-2">📚</span>
                                <span class="text-gray-700 dark:text-gray-300">{{ reserva.motivo }}</span>
                            </div>
                            <div v-if="reserva.descripcion"
                                class="text-sm text-gray-500 dark:text-gray-400 italic pl-6">
                                "{{ reserva.descripcion }}"
                            </div>
                        </div>

                        <div v-if="reserva.estado === 'pendiente' || reserva.estado === 'confirmada'" class="mt-4">
                            <button @click="cancelarReserva(reserva.id)"
                                class="w-full border border-red-500 text-red-500 hover:bg-red-50 dark:hover:bg-red-900/20 font-bold py-2 px-4 rounded transition">
                                Cancelar Reserva
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        </main>
    </div>
</template>
