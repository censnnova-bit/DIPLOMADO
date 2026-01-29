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

// Verificar que sea admin
if (!authStore.isAdmin) {
    router.push('/salones')
}

const asignaturas = ref([])
const loading = ref(false)
const showModal = ref(false)
const editingId = ref(null)

const form = ref({
    nombre: ''
})

onMounted(() => {
    loadAsignaturas()
})

const loadAsignaturas = async () => {
    loading.value = true
    try {
        const response = await api.getAsignaturas()
        asignaturas.value = response.data.results || response.data
    } catch (err) {
        console.error('Error cargando asignaturas:', err)
        notification.error('Error al cargar las asignaturas')
    } finally {
        loading.value = false
    }
}

const openCreateModal = () => {
    editingId.value = null
    resetForm()
    showModal.value = true
}

const openEditModal = (item) => {
    editingId.value = item.id
    form.value = {
        nombre: item.nombre
    }
    showModal.value = true
}

const resetForm = () => {
    form.value = {
        nombre: ''
    }
}

const saveAsignatura = async () => {
    try {
        if (editingId.value) {
            await api.updateAsignatura(editingId.value, form.value)
            notification.success('Asignatura actualizada exitosamente')
        } else {
            await api.createAsignatura(form.value)
            notification.success('Asignatura creada exitosamente')
        }
        showModal.value = false
        loadAsignaturas()
    } catch (err) {
        console.error('Error guardando asignatura:', err)
        notification.error(err.response?.data?.error || 'Error al guardar la asignatura')
    }
}

const deleteAsignatura = async (id, nombre) => {
    if (!confirm(`¿Está seguro de eliminar la asignatura "${nombre}"?`)) return

    try {
        await api.deleteAsignatura(id)
        notification.success('Asignatura eliminada exitosamente')
        loadAsignaturas()
    } catch (err) {
        console.error('Error eliminando asignatura:', err)
        notification.error('Error al eliminar la asignatura')
    }
}
</script>

<template>
    <div class="min-h-screen bg-white dark:bg-gray-900">
        <Header />

        <main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
            <div class="flex justify-between items-center mb-6">
                <div>
                    <h1 class="text-3xl font-bold text-gray-900 dark:text-white">Gestión de Asignaturas</h1>
                    <p class="text-gray-600 dark:text-gray-400 mt-1">Crear, editar y eliminar asignaturas del sistema
                    </p>
                </div>
                <button @click="openCreateModal"
                    class="bg-[#B90A0A] hover:bg-[#8f0606] text-white font-bold py-2 px-6 rounded-lg shadow-md transition">
                    <svg class="w-5 h-5 inline mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
                    </svg>
                    Nueva Asignatura
                </button>
            </div>

            <!-- Loading -->
            <div v-if="loading" class="text-center py-12">
                <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-[#B90A0A] mx-auto"></div>
            </div>

            <!-- Tabla -->
            <div v-else class="bg-white dark:bg-gray-800 shadow-md rounded-lg overflow-hidden">
                <table class="min-w-full divide-y divide-gray-200 dark:divide-gray-700">
                    <thead class="bg-gray-50 dark:bg-gray-700">
                        <tr>
                            <th
                                class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                                Código</th>
                            <th
                                class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                                Nombre</th>
                            <th
                                class="px-6 py-3 text-right text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                                Acciones</th>
                        </tr>
                    </thead>
                    <tbody class="bg-white dark:bg-gray-800 divide-y divide-gray-200 dark:divide-gray-700">
                        <tr v-for="item in asignaturas" :key="item.id" class="hover:bg-gray-50 dark:hover:bg-gray-700">
                            <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900 dark:text-white">{{
                                item.codigo || '--' }}</td>
                            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900 dark:text-white">{{ item.nombre
                                }}</td>
                            <td class="px-6 py-4 whitespace-nowrap text-sm">
                                <div class="flex justify-end space-x-2">
                                    <button @click="openEditModal(item)"
                                        class="text-blue-600 hover:text-blue-800 dark:text-blue-400 dark:hover:text-blue-300 font-medium transition-colors"
                                        title="Editar asignatura">
                                        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                                d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                                        </svg>
                                    </button>
                                    <button @click="deleteAsignatura(item.id, item.nombre)"
                                        class="text-red-600 hover:text-red-800 dark:text-red-400 dark:hover:text-red-300 font-medium transition-colors"
                                        title="Eliminar asignatura">
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

                <div v-if="asignaturas.length === 0" class="p-8 text-center text-gray-500 dark:text-gray-400">
                    No hay asignaturas registradas.
                </div>
            </div>
        </main>

        <!-- Modal -->
        <div v-if="showModal" class="fixed inset-0 z-50 overflow-y-auto" @click.self="showModal = false">
            <div class="flex items-center justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:block sm:p-0">
                <div class="fixed inset-0 bg-gray-500 bg-opacity-75 transition-opacity"></div>

                <div
                    class="inline-block align-bottom bg-white dark:bg-gray-800 rounded-lg text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-lg sm:w-full">
                    <form @submit.prevent="saveAsignatura">
                        <div class="bg-white dark:bg-gray-800 px-4 pt-5 pb-4 sm:p-6 sm:pb-4">
                            <h3 class="text-lg font-bold text-gray-900 dark:text-white mb-4">
                                {{ editingId ? 'Editar Asignatura' : 'Nueva Asignatura' }}
                            </h3>

                            <div class="space-y-4">
                                <div>
                                    <label class="block text-sm font-medium text-gray-700 dark:text-gray-300">Nombre
                                        *</label>
                                    <input v-model="form.nombre" required type="text"
                                        class="mt-1 block w-full rounded-md border-gray-300 dark:border-gray-600 dark:bg-gray-700 dark:text-white shadow-sm focus:border-[#B90A0A] focus:ring-[#B90A0A]">
                                </div>
                            </div>
                        </div>

                        <div class="bg-gray-50 dark:bg-gray-700 px-4 py-3 sm:px-6 sm:flex sm:flex-row-reverse">
                            <button type="submit"
                                class="w-full inline-flex justify-center rounded-md border border-transparent shadow-sm px-4 py-2 bg-[#B90A0A] text-base font-medium text-white hover:bg-[#8f0606] focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-[#B90A0A] sm:ml-3 sm:w-auto sm:text-sm">
                                Guardar
                            </button>
                            <button type="button" @click="showModal = false"
                                class="mt-3 w-full inline-flex justify-center rounded-md border border-gray-300 dark:border-gray-600 shadow-sm px-4 py-2 bg-white dark:bg-gray-800 text-base font-medium text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 sm:mt-0 sm:ml-3 sm:w-auto sm:text-sm">
                                Cancelar
                            </button>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    </div>
</template>
