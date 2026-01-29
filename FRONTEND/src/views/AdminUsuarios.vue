<template>
    <div class="min-h-screen bg-gray-50 dark:bg-gray-900 transition-colors duration-200">
        <Header />

        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
            <!-- Título -->
            <div class="mb-8">
                <h1 class="text-3xl font-bold text-gray-900 dark:text-white">
                    Gestión de Usuarios
                </h1>
                <p class="mt-2 text-gray-600 dark:text-gray-400">
                    Administra los usuarios docentes del sistema
                </p>
            </div>

            <!-- Formulario para crear nuevo docente -->
            <div class="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6 mb-8">
                <h2 class="text-xl font-semibold text-gray-900 dark:text-white mb-6">
                    Crear Nuevo Docente
                </h2>

                <form @submit.prevent="crearDocente" class="space-y-6">
                    <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                        <!-- Usuario -->
                        <div>
                            <label for="username"
                                class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                                Usuario *
                            </label>
                            <input id="username" v-model="nuevoDocente.username" type="text" required
                                class="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-500 dark:bg-gray-700 dark:text-white"
                                placeholder="Ej: docente2" />
                        </div>

                        <!-- Contraseña -->
                        <div>
                            <label for="password"
                                class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                                Contraseña *
                            </label>
                            <input id="password" v-model="nuevoDocente.password" type="password" required minlength="6"
                                class="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-500 dark:bg-gray-700 dark:text-white"
                                placeholder="Mínimo 6 caracteres" />
                        </div>

                        <!-- Primer Nombre -->
                        <div>
                            <label for="first_name"
                                class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                                Primer Nombre *
                            </label>
                            <input id="first_name" v-model="nuevoDocente.first_name" type="text" required
                                class="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-500 dark:bg-gray-700 dark:text-white"
                                placeholder="Ej: Juan" />
                        </div>

                        <!-- Primer Apellido -->
                        <div>
                            <label for="last_name"
                                class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                                Primer Apellido *
                            </label>
                            <input id="last_name" v-model="nuevoDocente.last_name" type="text" required
                                class="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-500 dark:bg-gray-700 dark:text-white"
                                placeholder="Ej: Pérez" />
                        </div>

                        <!-- Documento -->
                        <div>
                            <label for="documento"
                                class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                                Documento de Identidad *
                            </label>
                            <input id="documento" v-model="nuevoDocente.documento" type="text" required
                                class="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-500 dark:bg-gray-700 dark:text-white"
                                placeholder="Ej: 1234567890" />
                        </div>

                        <!-- Email (opcional) -->
                        <div>
                            <label for="email" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                                Email
                            </label>
                            <input id="email" v-model="nuevoDocente.email" type="email"
                                class="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-500 dark:bg-gray-700 dark:text-white"
                                placeholder="docente@gecos.com" />
                        </div>

                        <!-- Teléfono (opcional) -->
                        <div>
                            <label for="telefono"
                                class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                                Teléfono
                            </label>
                            <input id="telefono" v-model="nuevoDocente.telefono" type="tel"
                                class="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-500 dark:bg-gray-700 dark:text-white"
                                placeholder="3001234567" />
                        </div>
                    </div>

                    <!-- Mensajes de error -->
                    <div v-if="error"
                        class="bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg p-4">
                        <p class="text-red-800 dark:text-red-200">{{ error }}</p>
                    </div>

                    <!-- Mensajes de éxito -->
                    <div v-if="success"
                        class="bg-green-50 dark:bg-green-900/20 border border-green-200 dark:border-green-800 rounded-lg p-4">
                        <p class="text-green-800 dark:text-green-200">{{ success }}</p>
                    </div>

                    <!-- Botones -->
                    <div class="flex justify-end space-x-4">
                        <button type="button" @click="limpiarFormulario"
                            class="px-6 py-2 border border-gray-300 dark:border-gray-600 rounded-lg text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors">
                            Limpiar
                        </button>
                        <button type="submit" :disabled="loading"
                            class="px-6 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg disabled:opacity-50 disabled:cursor-not-allowed transition-colors">
                            {{ loading ? 'Creando...' : 'Crear Docente' }}
                        </button>
                    </div>
                </form>
            </div>

            <!-- Lista de docentes -->
            <div class="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6">
                <h2 class="text-xl font-semibold text-gray-900 dark:text-white mb-6">
                    Docentes Registrados
                </h2>

                <div v-if="loadingList" class="text-center py-8">
                    <p class="text-gray-600 dark:text-gray-400">Cargando docentes...</p>
                </div>

                <div v-else-if="docentes.length === 0" class="text-center py-8">
                    <p class="text-gray-600 dark:text-gray-400">No hay docentes registrados</p>
                </div>

                <div v-else class="overflow-x-auto">
                    <table class="min-w-full divide-y divide-gray-200 dark:divide-gray-700">
                        <thead class="bg-gray-50 dark:bg-gray-900">
                            <tr>
                                <th
                                    class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                                    Usuario
                                </th>
                                <th
                                    class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                                    Nombre Completo
                                </th>
                                <th
                                    class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                                    Documento
                                </th>
                                <th
                                    class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                                    Email
                                </th>
                                <th
                                    class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                                    Teléfono
                                </th>
                                <th
                                    class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                                    Estado
                                </th>
                                <th
                                    class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                                    Acciones
                                </th>
                            </tr>
                        </thead>
                        <tbody class="bg-white dark:bg-gray-800 divide-y divide-gray-200 dark:divide-gray-700">
                            <tr v-for="docente in docentes" :key="docente.id"
                                class="hover:bg-gray-50 dark:hover:bg-gray-700">
                                <td
                                    class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900 dark:text-white">
                                    {{ docente.username }}
                                </td>
                                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-600 dark:text-gray-300">
                                    {{ docente.first_name }} {{ docente.last_name }}
                                </td>
                                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-600 dark:text-gray-300">
                                    {{ docente.documento }}
                                </td>
                                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-600 dark:text-gray-300">
                                    {{ docente.email || '-' }}
                                </td>
                                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-600 dark:text-gray-300">
                                    {{ docente.telefono || '-' }}
                                </td>
                                <td class="px-6 py-4 whitespace-nowrap text-sm">
                                    <span
                                        :class="docente.is_active ? 'bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-400' : 'bg-red-100 text-red-800 dark:bg-red-900/30 dark:text-red-400'"
                                        class="px-2 py-1 rounded-full text-xs font-medium">
                                        {{ docente.is_active ? 'Activo' : 'Inactivo' }}
                                    </span>
                                </td>
                                <td class="px-6 py-4 whitespace-nowrap text-sm">
                                    <div class="flex space-x-2">
                                        <button @click="editarDocente(docente)"
                                            class="text-blue-600 hover:text-blue-800 dark:text-blue-400 dark:hover:text-blue-300 font-medium transition-colors"
                                            title="Editar docente">
                                            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                                    d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                                            </svg>
                                        </button>
                                        <button @click="confirmarEliminar(docente)"
                                            class="text-red-600 hover:text-red-800 dark:text-red-400 dark:hover:text-red-300 font-medium transition-colors"
                                            title="Eliminar docente">
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
                </div>
            </div>
        </div>

        <!-- Modal de Edición -->
        <div v-if="mostrarModalEditar"
            class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
            <div class="bg-white dark:bg-gray-800 rounded-lg shadow-xl max-w-2xl w-full max-h-[90vh] overflow-y-auto">
                <div class="p-6">
                    <h3 class="text-xl font-semibold text-gray-900 dark:text-white mb-4">
                        Editar Docente
                    </h3>

                    <form @submit.prevent="guardarEdicion" class="space-y-4">
                        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                            <div>
                                <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                                    Usuario
                                </label>
                                <input v-model="docenteEditando.username" type="text" disabled
                                    class="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-gray-100 dark:bg-gray-700 dark:text-gray-400 cursor-not-allowed" />
                            </div>

                            <div>
                                <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                                    Primer Nombre *
                                </label>
                                <input v-model="docenteEditando.first_name" type="text" required
                                    class="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-500 dark:bg-gray-700 dark:text-white" />
                            </div>

                            <div>
                                <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                                    Primer Apellido *
                                </label>
                                <input v-model="docenteEditando.last_name" type="text" required
                                    class="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-500 dark:bg-gray-700 dark:text-white" />
                            </div>

                            <div>
                                <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                                    Documento *
                                </label>
                                <input v-model="docenteEditando.documento" type="text" required
                                    class="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-500 dark:bg-gray-700 dark:text-white" />
                            </div>

                            <div>
                                <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                                    Email
                                </label>
                                <input v-model="docenteEditando.email" type="email"
                                    class="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-500 dark:bg-gray-700 dark:text-white" />
                            </div>

                            <div>
                                <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                                    Teléfono
                                </label>
                                <input v-model="docenteEditando.telefono" type="tel"
                                    class="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-500 dark:bg-gray-700 dark:text-white" />
                            </div>
                        </div>

                        <div v-if="errorEditar"
                            class="bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg p-4">
                            <p class="text-red-800 dark:text-red-200">{{ errorEditar }}</p>
                        </div>

                        <div class="flex justify-end space-x-3 pt-4">
                            <button type="button" @click="cerrarModalEditar"
                                class="px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors">
                                Cancelar
                            </button>
                            <button type="submit" :disabled="loadingEditar"
                                class="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg disabled:opacity-50 disabled:cursor-not-allowed transition-colors">
                                {{ loadingEditar ? 'Guardando...' : 'Guardar Cambios' }}
                            </button>
                        </div>
                    </form>
                </div>
            </div>
        </div>

        <!-- Modal de Confirmación de Eliminación -->
        <div v-if="mostrarModalEliminar"
            class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
            <div class="bg-white dark:bg-gray-800 rounded-lg shadow-xl max-w-md w-full p-6">
                <h3 class="text-xl font-semibold text-gray-900 dark:text-white mb-4">
                    Confirmar Eliminación
                </h3>
                <p class="text-gray-600 dark:text-gray-400 mb-6">
                    ¿Estás seguro de que deseas eliminar al docente <strong>{{ docenteAEliminar?.username }}</strong>?
                    Esta acción no se puede deshacer.
                </p>

                <div v-if="errorEliminar"
                    class="bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg p-4 mb-4">
                    <p class="text-red-800 dark:text-red-200">{{ errorEliminar }}</p>
                </div>

                <div class="flex justify-end space-x-3">
                    <button type="button" @click="cerrarModalEliminar"
                        class="px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors">
                        Cancelar
                    </button>
                    <button @click="eliminarDocente" :disabled="loadingEliminar"
                        class="px-4 py-2 bg-red-600 hover:bg-red-700 text-white rounded-lg disabled:opacity-50 disabled:cursor-not-allowed transition-colors">
                        {{ loadingEliminar ? 'Eliminando...' : 'Eliminar' }}
                    </button>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import Header from '../components/Header.vue'
import api from '../services/api'

const router = useRouter()

const nuevoDocente = ref({
    username: '',
    password: '',
    first_name: '',
    last_name: '',
    documento: '',
    email: '',
    telefono: ''
})

const docentes = ref([])
const loading = ref(false)
const loadingList = ref(false)
const error = ref('')
const success = ref('')

// Estados para edición
const mostrarModalEditar = ref(false)
const docenteEditando = ref(null)
const loadingEditar = ref(false)
const errorEditar = ref('')

// Estados para eliminación
const mostrarModalEliminar = ref(false)
const docenteAEliminar = ref(null)
const loadingEliminar = ref(false)
const errorEliminar = ref('')

const crearDocente = async () => {
    error.value = ''
    success.value = ''
    loading.value = true

    try {
        const response = await api.crearDocente(nuevoDocente.value)
        success.value = `¡Docente ${response.data.username} creado exitosamente!`
        limpiarFormulario()
        await cargarDocentes()

        // Limpiar mensaje de éxito después de 5 segundos
        setTimeout(() => {
            success.value = ''
        }, 5000)
    } catch (err) {
        console.error('Error al crear docente:', err)
        if (err.response?.data) {
            // Formatear errores del servidor
            const errores = err.response.data
            error.value = Object.entries(errores)
                .map(([campo, mensajes]) => `${campo}: ${Array.isArray(mensajes) ? mensajes.join(', ') : mensajes}`)
                .join(' | ')
        } else {
            error.value = 'Error al crear el docente. Por favor, verifica los datos.'
        }
    } finally {
        loading.value = false
    }
}

const limpiarFormulario = () => {
    nuevoDocente.value = {
        username: '',
        password: '',
        first_name: '',
        last_name: '',
        documento: '',
        email: '',
        telefono: ''
    }
    error.value = ''
}

const cargarDocentes = async () => {
    loadingList.value = true
    try {
        const response = await api.getUsuarios()
        console.log('Respuesta usuarios:', response.data)

        // Manejar tanto arrays como objetos paginados
        let usuarios = []
        if (Array.isArray(response.data)) {
            usuarios = response.data
        } else if (response.data.results) {
            // Respuesta paginada
            usuarios = response.data.results
        } else {
            console.error('Formato de respuesta inesperado:', response.data)
            usuarios = []
        }

        // Filtrar solo docentes (excluir admins)
        docentes.value = usuarios.filter(u => u.rol === 'docente')
    } catch (err) {
        console.error('Error al cargar docentes:', err)
    } finally {
        loadingList.value = false
    }
}

const editarDocente = (docente) => {
    docenteEditando.value = { ...docente }
    mostrarModalEditar.value = true
    errorEditar.value = ''
}

const cerrarModalEditar = () => {
    mostrarModalEditar.value = false
    docenteEditando.value = null
    errorEditar.value = ''
}

const guardarEdicion = async () => {
    errorEditar.value = ''
    loadingEditar.value = true

    try {
        const { id, username, rol, is_active, fecha_creacion, ...datosActualizables } = docenteEditando.value
        await api.actualizarUsuario(id, datosActualizables)

        success.value = `¡Docente ${username} actualizado exitosamente!`
        cerrarModalEditar()
        await cargarDocentes()

        setTimeout(() => {
            success.value = ''
        }, 5000)
    } catch (err) {
        console.error('Error al actualizar docente:', err)
        if (err.response?.data) {
            const errores = err.response.data
            errorEditar.value = Object.entries(errores)
                .map(([campo, mensajes]) => `${campo}: ${Array.isArray(mensajes) ? mensajes.join(', ') : mensajes}`)
                .join(' | ')
        } else {
            errorEditar.value = 'Error al actualizar el docente. Por favor, verifica los datos.'
        }
    } finally {
        loadingEditar.value = false
    }
}

const confirmarEliminar = (docente) => {
    docenteAEliminar.value = docente
    mostrarModalEliminar.value = true
    errorEliminar.value = ''
}

const cerrarModalEliminar = () => {
    mostrarModalEliminar.value = false
    docenteAEliminar.value = null
    errorEliminar.value = ''
}

const eliminarDocente = async () => {
    errorEliminar.value = ''
    loadingEliminar.value = true

    try {
        await api.eliminarUsuario(docenteAEliminar.value.id)

        success.value = `¡Docente ${docenteAEliminar.value.username} eliminado exitosamente!`
        cerrarModalEliminar()
        await cargarDocentes()

        setTimeout(() => {
            success.value = ''
        }, 5000)
    } catch (err) {
        console.error('Error al eliminar docente:', err)
        if (err.response?.data) {
            const errores = err.response.data
            errorEliminar.value = typeof errores === 'string' ? errores : JSON.stringify(errores)
        } else {
            errorEliminar.value = 'Error al eliminar el docente. Puede que tenga reservas asociadas.'
        }
    } finally {
        loadingEliminar.value = false
    }
}

onMounted(() => {
    cargarDocentes()
})
</script>

<style scoped>
/* Estilos adicionales si son necesarios */
</style>
