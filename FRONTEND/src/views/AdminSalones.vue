<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import Header from '../components/Header.vue'
import api from '../services/api'

const authStore = useAuthStore()
const router = useRouter()

// Verificar que sea admin
if (!authStore.isAdmin) {
  router.push('/salones')
}

const salones = ref([])
const loading = ref(false)
const showModal = ref(false)
const editingId = ref(null)

const salonForm = ref({
  nombre: '',
  codigo: '',
  tipo: 'aula',
  bloque: '',
  piso: '',
  capacidad: 30,
  descripcion: '',
  tiene_proyector: false,
  tiene_aire_acondicionado: false,
  tiene_computadores: false,
  tiene_smart_tv: false,
  tiene_audio: false,
  tiene_wifi: true,
  imagen_url: '',
  estado: 'disponible'
})

const tiposSalon = [
  { value: 'aula', label: 'Aula' },
  { value: 'laboratorio', label: 'Laboratorio' },
  { value: 'auditorio', label: 'Auditorio' },
  { value: 'sala_conferencias', label: 'Sala de Conferencias' }
]

onMounted(() => {
  loadSalones()
})

const loadSalones = async () => {
  loading.value = true
  try {
    const response = await api.getSalones()
    salones.value = response.data.results || response.data
  } catch (err) {
    console.error('Error cargando salones:', err)
    alert('Error al cargar los salones')
  } finally {
    loading.value = false
  }
}

const openCreateModal = () => {
  editingId.value = null
  resetForm()
  showModal.value = true
}

const openEditModal = (salon) => {
  editingId.value = salon.id
  salonForm.value = {
    nombre: salon.nombre,
    codigo: salon.codigo,
    tipo: salon.tipo,
    bloque: salon.bloque,
    piso: salon.piso,
    capacidad: salon.capacidad,
    descripcion: salon.descripcion || '',
    tiene_proyector: salon.tiene_proyector,
    tiene_aire_acondicionado: salon.tiene_aire_acondicionado,
    tiene_computadores: salon.tiene_computadores,
    tiene_smart_tv: salon.tiene_smart_tv,
    tiene_audio: salon.tiene_audio,
    tiene_wifi: salon.tiene_wifi,
    imagen_url: salon.imagen_url || '',
    estado: salon.estado
  }
  showModal.value = true
}

const resetForm = () => {
  salonForm.value = {
    nombre: '',
    codigo: '',
    tipo: 'aula',
    bloque: '',
    piso: '',
    capacidad: 30,
    descripcion: '',
    tiene_proyector: false,
    tiene_aire_acondicionado: false,
    tiene_computadores: false,
    tiene_smart_tv: false,
    tiene_audio: false,
    tiene_wifi: true,
    imagen_url: '',
    estado: 'disponible'
  }
}

const saveSalon = async () => {
  try {
    if (editingId.value) {
      await api.updateSalon(editingId.value, salonForm.value)
      alert('Salón actualizado exitosamente')
    } else {
      await api.createSalon(salonForm.value)
      alert('Salón creado exitosamente')
    }
    showModal.value = false
    loadSalones()
  } catch (err) {
    console.error('Error guardando salón:', err)
    alert(err.response?.data?.error || 'Error al guardar el salón')
  }
}

const deleteSalon = async (id, nombre) => {
  if (!confirm(`¿Está seguro de eliminar el salón "${nombre}"?`)) return
  
  try {
    await api.deleteSalon(id)
    alert('Salón eliminado exitosamente')
    loadSalones()
  } catch (err) {
    console.error('Error eliminando salón:', err)
    alert('Error al eliminar el salón')
  }
}
</script>

<template>
  <div class="min-h-screen bg-white dark:bg-gray-900">
    <Header />
    
    <main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div class="flex justify-between items-center mb-6">
        <div>
          <h1 class="text-3xl font-bold text-gray-900 dark:text-white">Administrar Salones</h1>
          <p class="text-gray-600 dark:text-gray-400 mt-1">Crear, editar y eliminar salones</p>
        </div>
        <button @click="openCreateModal" class="bg-[#B90A0A] hover:bg-[#8f0606] text-white font-bold py-2 px-6 rounded-lg shadow-md transition">
          <svg class="w-5 h-5 inline mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"/>
          </svg>
          Nuevo Salón
        </button>
      </div>

      <!-- Loading -->
      <div v-if="loading" class="text-center py-12">
        <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-[#B90A0A] mx-auto"></div>
      </div>

      <!-- Tabla de Salones -->
      <div v-else class="bg-white dark:bg-gray-800 shadow-md rounded-lg overflow-hidden">
        <table class="min-w-full divide-y divide-gray-200 dark:divide-gray-700">
          <thead class="bg-gray-50 dark:bg-gray-700">
            <tr>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">Código</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">Nombre</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">Tipo</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">Bloque</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">Capacidad</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">Estado</th>
              <th class="px-6 py-3 text-right text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">Acciones</th>
            </tr>
          </thead>
          <tbody class="bg-white dark:bg-gray-800 divide-y divide-gray-200 dark:divide-gray-700">
            <tr v-for="salon in salones" :key="salon.id" class="hover:bg-gray-50 dark:hover:bg-gray-700">
              <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900 dark:text-white">{{ salon.codigo }}</td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900 dark:text-white">{{ salon.nombre }}</td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-400">{{ salon.tipo }}</td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-400">{{ salon.bloque }}</td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-400">{{ salon.capacidad }}</td>
              <td class="px-6 py-4 whitespace-nowrap">
                <span :class="{
                  'bg-green-100 text-green-800': salon.estado === 'disponible',
                  'bg-yellow-100 text-yellow-800': salon.estado === 'ocupado',
                  'bg-red-100 text-red-800': salon.estado === 'mantenimiento'
                }" class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full">
                  {{ salon.estado }}
                </span>
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                <button @click="openEditModal(salon)" class="text-blue-600 hover:text-blue-900 dark:text-blue-400 mr-3">
                  Editar
                </button>
                <button @click="deleteSalon(salon.id, salon.nombre)" class="text-red-600 hover:text-red-900 dark:text-red-400">
                  Eliminar
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </main>

    <!-- Modal -->
    <div v-if="showModal" class="fixed inset-0 z-50 overflow-y-auto" @click.self="showModal = false">
      <div class="flex items-center justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:block sm:p-0">
        <div class="fixed inset-0 bg-gray-500 bg-opacity-75 transition-opacity"></div>
        
        <div class="inline-block align-bottom bg-white dark:bg-gray-800 rounded-lg text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-2xl sm:w-full">
          <form @submit.prevent="saveSalon">
            <div class="bg-white dark:bg-gray-800 px-4 pt-5 pb-4 sm:p-6 sm:pb-4">
              <h3 class="text-lg font-bold text-gray-900 dark:text-white mb-4">
                {{ editingId ? 'Editar Salón' : 'Nuevo Salón' }}
              </h3>
              
              <div class="grid grid-cols-2 gap-4">
                <div>
                  <label class="block text-sm font-medium text-gray-700 dark:text-gray-300">Nombre *</label>
                  <input v-model="salonForm.nombre" required type="text" class="mt-1 block w-full rounded-md border-gray-300 dark:border-gray-600 dark:bg-gray-700 dark:text-white shadow-sm focus:border-[#B90A0A] focus:ring-[#B90A0A]">
                </div>
                
                <div>
                  <label class="block text-sm font-medium text-gray-700 dark:text-gray-300">Código *</label>
                  <input v-model="salonForm.codigo" required type="text" class="mt-1 block w-full rounded-md border-gray-300 dark:border-gray-600 dark:bg-gray-700 dark:text-white shadow-sm focus:border-[#B90A0A] focus:ring-[#B90A0A]">
                </div>
                
                <div>
                  <label class="block text-sm font-medium text-gray-700 dark:text-gray-300">Tipo *</label>
                  <select v-model="salonForm.tipo" required class="mt-1 block w-full rounded-md border-gray-300 dark:border-gray-600 dark:bg-gray-700 dark:text-white shadow-sm focus:border-[#B90A0A] focus:ring-[#B90A0A]">
                    <option v-for="tipo in tiposSalon" :key="tipo.value" :value="tipo.value">{{ tipo.label }}</option>
                  </select>
                </div>
                
                <div>
                  <label class="block text-sm font-medium text-gray-700 dark:text-gray-300">Estado *</label>
                  <select v-model="salonForm.estado" required class="mt-1 block w-full rounded-md border-gray-300 dark:border-gray-600 dark:bg-gray-700 dark:text-white shadow-sm focus:border-[#B90A0A] focus:ring-[#B90A0A]">
                    <option value="disponible">Disponible</option>
                    <option value="ocupado">Ocupado</option>
                    <option value="mantenimiento">Mantenimiento</option>
                  </select>
                </div>
                
                <div>
                  <label class="block text-sm font-medium text-gray-700 dark:text-gray-300">Bloque *</label>
                  <input v-model="salonForm.bloque" required type="text" class="mt-1 block w-full rounded-md border-gray-300 dark:border-gray-600 dark:bg-gray-700 dark:text-white shadow-sm focus:border-[#B90A0A] focus:ring-[#B90A0A]">
                </div>
                
                <div>
                  <label class="block text-sm font-medium text-gray-700 dark:text-gray-300">Piso *</label>
                  <input v-model="salonForm.piso" required type="text" class="mt-1 block w-full rounded-md border-gray-300 dark:border-gray-600 dark:bg-gray-700 dark:text-white shadow-sm focus:border-[#B90A0A] focus:ring-[#B90A0A]">
                </div>
                
                <div>
                  <label class="block text-sm font-medium text-gray-700 dark:text-gray-300">Capacidad *</label>
                  <input v-model.number="salonForm.capacidad" required type="number" min="1" class="mt-1 block w-full rounded-md border-gray-300 dark:border-gray-600 dark:bg-gray-700 dark:text-white shadow-sm focus:border-[#B90A0A] focus:ring-[#B90A0A]">
                </div>
                
                <div>
                  <label class="block text-sm font-medium text-gray-700 dark:text-gray-300">URL Imagen</label>
                  <input v-model="salonForm.imagen_url" type="url" class="mt-1 block w-full rounded-md border-gray-300 dark:border-gray-600 dark:bg-gray-700 dark:text-white shadow-sm focus:border-[#B90A0A] focus:ring-[#B90A0A]">
                </div>
                
                <div class="col-span-2">
                  <label class="block text-sm font-medium text-gray-700 dark:text-gray-300">Descripción</label>
                  <textarea v-model="salonForm.descripcion" rows="2" class="mt-1 block w-full rounded-md border-gray-300 dark:border-gray-600 dark:bg-gray-700 dark:text-white shadow-sm focus:border-[#B90A0A] focus:ring-[#B90A0A]"></textarea>
                </div>
                
                <div class="col-span-2">
                  <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Equipamiento</label>
                  <div class="grid grid-cols-3 gap-3">
                    <label class="flex items-center">
                      <input v-model="salonForm.tiene_proyector" type="checkbox" class="rounded text-[#B90A0A] focus:ring-[#B90A0A]">
                      <span class="ml-2 text-sm text-gray-700 dark:text-gray-300">Proyector</span>
                    </label>
                    <label class="flex items-center">
                      <input v-model="salonForm.tiene_aire_acondicionado" type="checkbox" class="rounded text-[#B90A0A] focus:ring-[#B90A0A]">
                      <span class="ml-2 text-sm text-gray-700 dark:text-gray-300">Aire Acondicionado</span>
                    </label>
                    <label class="flex items-center">
                      <input v-model="salonForm.tiene_computadores" type="checkbox" class="rounded text-[#B90A0A] focus:ring-[#B90A0A]">
                      <span class="ml-2 text-sm text-gray-700 dark:text-gray-300">Computadores</span>
                    </label>
                    <label class="flex items-center">
                      <input v-model="salonForm.tiene_smart_tv" type="checkbox" class="rounded text-[#B90A0A] focus:ring-[#B90A0A]">
                      <span class="ml-2 text-sm text-gray-700 dark:text-gray-300">Smart TV</span>
                    </label>
                    <label class="flex items-center">
                      <input v-model="salonForm.tiene_audio" type="checkbox" class="rounded text-[#B90A0A] focus:ring-[#B90A0A]">
                      <span class="ml-2 text-sm text-gray-700 dark:text-gray-300">Sistema de Audio</span>
                    </label>
                    <label class="flex items-center">
                      <input v-model="salonForm.tiene_wifi" type="checkbox" class="rounded text-[#B90A0A] focus:ring-[#B90A0A]">
                      <span class="ml-2 text-sm text-gray-700 dark:text-gray-300">WiFi</span>
                    </label>
                  </div>
                </div>
              </div>
            </div>
            
            <div class="bg-gray-50 dark:bg-gray-700 px-4 py-3 sm:px-6 sm:flex sm:flex-row-reverse">
              <button type="submit" class="w-full inline-flex justify-center rounded-md border border-transparent shadow-sm px-4 py-2 bg-[#B90A0A] text-base font-medium text-white hover:bg-[#8f0606] focus:outline-none sm:ml-3 sm:w-auto sm:text-sm">
                {{ editingId ? 'Actualizar' : 'Crear' }}
              </button>
              <button type="button" @click="showModal = false" class="mt-3 w-full inline-flex justify-center rounded-md border border-gray-300 dark:border-gray-600 shadow-sm px-4 py-2 bg-white dark:bg-gray-800 text-base font-medium text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-700 focus:outline-none sm:mt-0 sm:ml-3 sm:w-auto sm:text-sm">
                Cancelar
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>
