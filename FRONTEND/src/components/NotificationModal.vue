<script setup>
import { useNotificationStore } from '../stores/notification'

const notification = useNotificationStore()

const iconPaths = {
    success: 'M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z',
    error: 'M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z',
    warning: 'M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z',
    info: 'M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z'
}

const bgColors = {
    success: 'bg-green-100 dark:bg-green-900/30',
    error: 'bg-red-100 dark:bg-red-900/30',
    warning: 'bg-yellow-100 dark:bg-yellow-900/30',
    info: 'bg-blue-100 dark:bg-blue-900/30'
}

const iconColors = {
    success: 'text-green-600 dark:text-green-400',
    error: 'text-red-600 dark:text-red-400',
    warning: 'text-yellow-600 dark:text-yellow-400',
    info: 'text-blue-600 dark:text-blue-400'
}

const buttonColors = {
    success: 'bg-green-600 hover:bg-green-700 focus:ring-green-500',
    error: 'bg-red-600 hover:bg-red-700 focus:ring-red-500',
    warning: 'bg-yellow-600 hover:bg-yellow-700 focus:ring-yellow-500',
    info: 'bg-blue-600 hover:bg-blue-700 focus:ring-blue-500'
}
</script>

<template>
    <Teleport to="body">
        <Transition enter-active-class="transition ease-out duration-300" enter-from-class="opacity-0"
            enter-to-class="opacity-100" leave-active-class="transition ease-in duration-200"
            leave-from-class="opacity-100" leave-to-class="opacity-0">
            <div v-if="notification.show" class="fixed inset-0 z-[200] overflow-y-auto">
                <div class="flex min-h-full items-center justify-center p-4 text-center">
                    <!-- Overlay -->
                    <div class="fixed inset-0 bg-gray-500/75 dark:bg-gray-900/80 transition-opacity"
                        @click="notification.close()"></div>

                    <!-- Modal -->
                    <Transition enter-active-class="transition ease-out duration-300"
                        enter-from-class="opacity-0 translate-y-4 sm:translate-y-0 sm:scale-95"
                        enter-to-class="opacity-100 translate-y-0 sm:scale-100"
                        leave-active-class="transition ease-in duration-200"
                        leave-from-class="opacity-100 translate-y-0 sm:scale-100"
                        leave-to-class="opacity-0 translate-y-4 sm:translate-y-0 sm:scale-95">
                        <div v-if="notification.show"
                            class="relative transform overflow-hidden rounded-xl bg-white dark:bg-gray-800 text-left shadow-xl transition-all sm:my-8 sm:w-full sm:max-w-md">
                            <div class="p-6">
                                <div class="flex items-start gap-4">
                                    <!-- Icon -->
                                    <div
                                        :class="[bgColors[notification.type], 'flex-shrink-0 flex items-center justify-center h-12 w-12 rounded-full']">
                                        <svg :class="[iconColors[notification.type], 'h-6 w-6']" fill="none"
                                            stroke="currentColor" viewBox="0 0 24 24">
                                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                                :d="iconPaths[notification.type]" />
                                        </svg>
                                    </div>

                                    <!-- Content -->
                                    <div class="flex-1 pt-0.5">
                                        <h3 class="text-lg font-semibold text-gray-900 dark:text-white">
                                            {{ notification.title }}
                                        </h3>
                                        <p class="mt-2 text-sm text-gray-600 dark:text-gray-300">
                                            {{ notification.message }}
                                        </p>
                                    </div>
                                </div>
                            </div>

                            <!-- Footer -->
                            <div class="bg-gray-50 dark:bg-gray-700/50 px-6 py-4">
                                <button @click="notification.close()"
                                    :class="[buttonColors[notification.type], 'w-full inline-flex justify-center rounded-lg px-4 py-2.5 text-sm font-semibold text-white shadow-sm focus:outline-none focus:ring-2 focus:ring-offset-2 dark:focus:ring-offset-gray-800 transition-colors']">
                                    Aceptar
                                </button>
                            </div>
                        </div>
                    </Transition>
                </div>
            </div>
        </Transition>
    </Teleport>
</template>
