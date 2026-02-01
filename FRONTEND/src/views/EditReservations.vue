<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import { useNotificationStore } from '../stores/notification'
import Header from '../components/Header.vue'
import api from '../services/api'

const authStore = useAuthStore()
const notification = useNotificationStore()
const router = useRouter()

const reservas = ref([])
const asignaturas = ref([])
const loading = ref(false)
const showModal = ref(false)
const editingId = ref(null)

const form = ref({
    motivo: '',
    descripcion: ''
})

onMounted(() => {
    // Security check handled by router, but double check auth
    if (!authStore.isAuthenticated) {
        router.push('/login')
        return
    }
    loadReservas()
    loadAsignaturas()
})

const loadAsignaturas = async () => {
    try {
        const response = await api.getAsignaturas()
        const raw = response.data.results || response.data
        asignaturas.value = Array.isArray(raw) ? raw.filter(a => a && a.id) : []
    } catch (err) {
        console.error('Error cargando asignaturas:', err)
        asignaturas.value = []
    }
}

const loadReservas = async () => {
    loading.value = true
    try {
        let response;
        if (authStore.isAdmin) {
            // Admin ve todas
            response = await api.getReservas()
        } else {
            // Docente ve las suyas
            response = await api.getMisReservas()
        }
        // Manejo de paginación DRF
        const raw = response.data.results || response.data
        console.log('RESERVAS RAW:', raw)
        reservas.value = Array.isArray(raw) ? raw.filter(r => r && r.id) : []
    } catch (err) {
        console.error('Error cargando reservas:', err)
        notification.error('Error al cargar las reservas')
    } finally {
        loading.value = false
    }
}

const openEditModal = (reserva) => {
    console.log('EDITAR RESERVA:', reserva);
    if (!reserva || !reserva.id) return;
    editingId.value = reserva.id
    form.value = {
        motivo: reserva.motivo ?? '',
        descripcion: reserva.descripcion ?? ''
    }
    showModal.value = true
}

const saveReserva = async () => {
    try {
        await api.updateReserva(editingId.value, {
            motivo: form.value.motivo,
            descripcion: form.value.descripcion
        })
        notification.success('Reserva actualizada correctamente')
        showModal.value = false
        loadReservas()
    } catch (err) {
        console.error('Error actualizando reserva:', err)
        notification.error('Error al actualizar la reserva. ' + (err.response?.data?.detail || ''))
    }
}

const formatDate = (dateStr) => {
    if (!dateStr) return ''
    return new Date(dateStr).toLocaleDateString()
}
</script>

<template>
    <div class="min-h-screen bg-white dark:bg-gray-900">
        <Header />

        <main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
            <div class="flex justify-between items-center mb-6">
                <div>
                    <h1 class="text-3xl font-bold text-gray-900 dark:text-white">Editar Reservas</h1>
                    <p class="text-gray-600 dark:text-gray-400 mt-1">
                        {{ authStore.isAdmin ? 'Gestionar todas las reservas' : 'Gestionar mis reservas' }}
                    </p>
                </div>
            </div>

            <!-- Loading -->
            <div v-if="loading" class="text-center py-12">
                <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-[#B90A0A] mx-auto"></div>
            </div>

            <!-- Empty State -->
            <div v-else-if="reservas.length === 0" class="text-center py-12 bg-gray-50 dark:bg-gray-800 rounded-lg">
                <p class="text-gray-500 dark:text-gray-400 text-lg">No hay reservas para mostrar.</p>
            </div>

            <!-- Tabla -->
            <div v-else class="bg-white dark:bg-gray-800 shadow-md rounded-lg overflow-hidden">
                <div class="overflow-x-auto">
                    <table class="min-w-full divide-y divide-gray-200 dark:divide-gray-700">
                        <thead class="bg-gray-50 dark:bg-gray-700">
                            <tr>
                                <th
                                    class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                                    Fecha / Hora</th>
                                <th
                                    class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                                    Salón</th>
                                <th v-if="authStore.isAdmin"
                                    class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                                    Usuario</th>
                                <th
                                    class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                                    Asignatura</th>
                                <th
                                    class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                                    Notas</th>
                                <th
                                    class="px-6 py-3 text-right text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                                    Acciones</th>
                            </tr>
                        </thead>
                        <tbody class="bg-white dark:bg-gray-800 divide-y divide-gray-200 dark:divide-gray-700">
                            <tr v-for="reserva in reservas" :key="reserva.id"
                                class="hover:bg-gray-50 dark:hover:bg-gray-700">
                                <template v-if="reserva && reserva.id">
                                    <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900 dark:text-white">
                                        <div>{{ formatDate(reserva.fecha) }}</div>
                                        <div class="text-xs text-gray-500">{{ reserva.hora_inicio }} - {{
                                            reserva.hora_fin }}</div>
                                    </td>
                                    <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900 dark:text-white">
                                        {{ reserva.salon_detalle?.nombre ?? reserva.salon ?? '-' }}
                                        <div class="text-xs text-gray-500">{{ reserva.salon_detalle?.bloque ?? '' }}
                                        </div>
                                    </td>
                                    <td v-if="authStore.isAdmin"
                                        class="px-6 py-4 whitespace-nowrap text-sm text-gray-900 dark:text-white">
                                        {{ reserva.usuario_nombre ?? (reserva.usuario ? 'Usuario ' + reserva.usuario :
                                            '-') }}
                                    </td>
                                    <td
                                        class="px-6 py-4 whitespace-nowrap text-sm text-gray-900 dark:text-white font-medium">
                                        {{ reserva.motivo ?? '-' }}
                                    </td>
                                    <td class="px-6 py-4 text-sm text-gray-500 dark:text-gray-400 max-w-xs truncate"
                                        :title="reserva.descripcion ?? ''">
                                        {{ reserva.descripcion ?? '-' }}
                                    </td>
                                    <td class="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                                        <button @click="openEditModal(reserva)"
                                            class="text-[#B90A0A] hover:text-[#8f0606] font-bold">
                                            Editar
                                        </button>
                                    </td>
                                </template>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>
        </main>

        <!-- Modal Edición -->
        <div v-if="showModal" class="fixed inset-0 z-[100] overflow-y-auto" @click.self="showModal = false">
            <div class="flex items-center justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:block sm:p-0">
                <div class="fixed inset-0 bg-gray-500 bg-opacity-75 transition-opacity"></div>
                <span class="hidden sm:inline-block sm:align-middle sm:h-screen">&#8203;</span>
                <div
                    class="inline-block align-bottom bg-white dark:bg-gray-800 rounded-lg text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-lg sm:w-full">
                    <div class="bg-white dark:bg-gray-800 px-4 pt-5 pb-4 sm:p-6 sm:pb-4">
                        <h3 class="text-lg font-medium leading-6 text-gray-900 dark:text-white mb-4">Editar Reserva</h3>
                        <form @submit.prevent="saveReserva">
                            <div class="mb-4">
                                <label
                                    class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Asignatura</label>
                                <select v-model="form.motivo" required
                                    class="mt-1 block w-full rounded-md border-gray-300 dark:border-gray-600 dark:bg-gray-700 dark:text-white shadow-sm focus:border-[#B90A0A] focus:ring-[#B90A0A]">
                                    <option value="" disabled>Seleccione una asignatura</option>
                                    <option v-for="asig in (asignaturas || [])" :key="asig.id" :value="asig.nombre">
                                        {{ asig.nombre }}
                                    </option>
                                    <!-- Opción fallback por si el motivo actual no está en la lista de asignaturas -->
                                    <option v-if="form.motivo && !asignaturas.some(a => a.nombre === form.motivo)"
                                        :value="form.motivo">
                                        {{ form.motivo }}
                                    </option>
                                </select>
                            </div>
                            <div class="mb-4">
                                <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Notas
                                    Adicionales</label>
                                <textarea v-model="form.descripcion" rows="3"
                                    class="mt-1 block w-full rounded-md border-gray-300 dark:border-gray-600 dark:bg-gray-700 dark:text-white shadow-sm focus:border-[#B90A0A] focus:ring-[#B90A0A]"></textarea>
                            </div>
                            <div class="mt-5 sm:mt-6 sm:grid sm:grid-cols-2 sm:gap-3 sm:flow-row-reverse">
                                <button type="submit"
                                    class="w-full inline-flex justify-center rounded-md border border-transparent shadow-sm px-4 py-2 bg-[#B90A0A] text-base font-medium text-white hover:bg-[#8f0606] focus:outline-none sm:ml-3 sm:w-auto sm:text-sm">
                                    Guardar
                                </button>
                                <button type="button" @click="showModal = false"
                                    class="mt-3 w-full inline-flex justify-center rounded-md border border-gray-300 dark:border-gray-600 shadow-sm px-4 py-2 bg-white dark:bg-gray-800 text-base font-medium text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-700 focus:outline-none sm:mt-0 sm:ml-3 sm:w-auto sm:text-sm">
                                    Cancelar
                                </button>
                            </div>
                        </form>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>
