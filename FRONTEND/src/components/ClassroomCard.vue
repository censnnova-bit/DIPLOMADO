<script setup>
import { ref } from 'vue'

const props = defineProps({
  classroom: {
    type: Object,
    required: true
  }
})

const getStatusColor = (status) => {
  const colors = {
    available: 'bg-white/95 text-green-700',
    occupied: 'bg-white/95 text-yellow-700',
    maintenance: 'bg-red-100 text-red-800 border border-red-200',
    soon: 'bg-white/95 text-yellow-700'
  }
  return colors[status] || colors.available
}

const getStatusIcon = (status) => {
  return status === 'available' ? 'animate-pulse' : ''
}
</script>

<template>
  <div class="classroom-card bg-white dark:bg-gray-800 rounded-xl shadow-md hover:shadow-xl border border-gray-200 dark:border-gray-700 overflow-hidden flex flex-col h-full group transition-all duration-300">
    <!-- Image -->
    <div class="relative h-48 bg-gray-200 dark:bg-gray-700 overflow-hidden">
      <img 
        :alt="classroom.name" 
        :src="classroom.image" 
        class="w-full h-full object-cover transition-transform duration-700 group-hover:scale-110"
        :class="{ 'filter grayscale': classroom.status === 'maintenance' }"
      />
      <div class="absolute inset-0 bg-gradient-to-t from-black/50 to-transparent opacity-60"></div>
      
      <!-- Status badge -->
      <div 
        :class="getStatusColor(classroom.status)"
        class="absolute top-3 right-3 text-xs font-bold px-3 py-1.5 rounded-full shadow-sm flex items-center backdrop-blur-sm"
      >
        <span 
          :class="getStatusIcon(classroom.status)"
          class="w-2 h-2 rounded-full mr-2"
          :style="{ backgroundColor: classroom.statusColor }"
        ></span>
        {{ classroom.statusText }}
      </div>
    </div>

    <!-- Content -->
    <div class="p-5 flex-grow" :class="{ 'opacity-75': classroom.status === 'maintenance' }">
      <div class="flex justify-between items-start mb-3">
        <h3 class="text-xl font-display font-bold text-gray-900 dark:text-white group-hover:text-[#B90A0A] transition-colors">
          {{ classroom.name }}
        </h3>
        <span class="text-xs font-bold font-mono text-gray-500 dark:text-gray-400 bg-gray-100 dark:bg-gray-700 px-2 py-1 rounded border border-gray-200 dark:border-gray-600">
          {{ classroom.floor }}
        </span>
      </div>

      <!-- Features -->
      <div class="flex items-center space-x-4 text-sm text-gray-600 dark:text-gray-300 mb-5">
        <div class="flex items-center" title="Capacidad">
          <svg class="w-5 h-5 mr-1.5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z"/>
          </svg>
          {{ classroom.capacity }}
        </div>
        <div v-for="feature in classroom.features" :key="feature.name" class="flex items-center" :title="feature.name">
          <svg class="w-5 h-5 mr-1.5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" :d="feature.icon"/>
          </svg>
          Si
        </div>
      </div>

      <!-- Availability bar -->
      <div class="mb-4">
        <p class="text-[10px] font-bold text-gray-400 uppercase tracking-widest mb-2">Estado Actual</p>
        <div v-if="classroom.status !== 'maintenance'" class="flex space-x-1 h-2.5 overflow-hidden rounded-full bg-gray-100 dark:bg-gray-700">
          <div 
            v-for="(slot, index) in classroom.schedule" 
            :key="index"
            :class="slot.status === 'occupied' ? 'bg-red-500/80' : 'bg-green-500/80'"
            class="flex-1"
            :title="slot.time"
          ></div>
        </div>
        <div v-else class="w-full bg-gray-100 dark:bg-gray-700 rounded-lg p-3 text-center text-xs font-medium text-gray-500 dark:text-gray-400 italic border border-dashed border-gray-300 dark:border-gray-600">
          Fuera de servicio por reparaciones
        </div>
        <div v-if="classroom.status !== 'maintenance'" class="flex justify-between text-[10px] text-gray-400 mt-1 font-mono">
          <span>08:00</span>
          <span>12:00</span>
          <span>18:00</span>
        </div>
      </div>
    </div>

    <!-- Action button -->
    <div class="px-5 pb-5 mt-auto">
      <router-link 
        v-if="classroom.status === 'available'"
        :to="`/aula/${classroom.id}`"
        class="w-full bg-[#B90A0A] dark:bg-gray-800 border border-[#B90A0A] text-white font-bold py-2.5 rounded-lg transition-all duration-300 flex justify-center items-center shadow-sm hover:shadow-md"
      >
        Reservar Aula
      </router-link>
      <router-link 
        v-else-if="classroom.status === 'occupied' || classroom.status === 'soon'"
        :to="`/aula/${classroom.id}`"
        class="w-full bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-600 text-gray-600 dark:text-gray-300 hover:border-[#B90A0A] hover:text-[#B90A0A] font-bold py-2.5 rounded-lg transition-all duration-300 flex justify-center items-center shadow-sm hover:shadow-md"
      >
        Ver Detalles
      </router-link>
      <button 
        v-else
        disabled
        class="w-full bg-gray-50 dark:bg-gray-700 border-2 border-transparent text-gray-400 font-bold py-2.5 rounded-lg cursor-not-allowed"
      >
        No Disponible
      </button>
    </div>
  </div>
</template>

<style scoped>
.classroom-card {
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.classroom-card:hover {
  transform: translateY(-4px);
}
</style>
