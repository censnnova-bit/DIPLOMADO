import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useNotificationStore = defineStore('notification', () => {
  const show = ref(false)
  const message = ref('')
  const type = ref('info') // 'success', 'error', 'warning', 'info'
  const title = ref('')

  function showNotification(msg, notificationType = 'info', notificationTitle = '') {
    message.value = msg
    type.value = notificationType
    title.value = notificationTitle || getDefaultTitle(notificationType)
    show.value = true
  }

  function getDefaultTitle(type) {
    switch (type) {
      case 'success':
        return '¡Éxito!'
      case 'error':
        return 'Error'
      case 'warning':
        return 'Advertencia'
      default:
        return 'Información'
    }
  }

  function success(msg, title = '') {
    showNotification(msg, 'success', title)
  }

  function error(msg, title = '') {
    showNotification(msg, 'error', title)
  }

  function warning(msg, title = '') {
    showNotification(msg, 'warning', title)
  }

  function info(msg, title = '') {
    showNotification(msg, 'info', title)
  }

  function close() {
    show.value = false
  }

  return {
    show,
    message,
    type,
    title,
    showNotification,
    success,
    error,
    warning,
    info,
    close
  }
})
