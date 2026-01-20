<script setup>
defineProps({
  title: {
    type: String,
    required: true
  },
  description: {
    type: String,
    default: ''
  },
  icon: {
    type: String,
    default: '✨'
  }
})
</script>

<template>
  <div class="bg-white rounded-xl shadow-lg p-6 hover:shadow-2xl transition-shadow duration-300">
    <div class="flex items-center mb-4">
      <span class="text-4xl mr-3">{{ icon }}</span>
      <h3 class="text-2xl font-bold text-gray-800">{{ title }}</h3>
    </div>
    <p class="text-gray-600 leading-relaxed">{{ description }}</p>
  </div>
</template>
