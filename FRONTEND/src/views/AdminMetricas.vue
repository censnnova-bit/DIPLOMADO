<script setup>
import { ref, onMounted, computed } from 'vue'
import Header from '../components/Header.vue'
import api from '../services/api'
import jsPDF from 'jspdf'
import html2canvas from 'html2canvas'
import {
    Chart as ChartJS,
    CategoryScale,
    LinearScale,
    BarElement,
    Title,
    Tooltip,
    Legend,
    ArcElement,
    PointElement,
    LineElement,
    Filler
} from 'chart.js'
import { Bar, Doughnut, Line } from 'vue-chartjs'

// Registrar componentes de Chart.js
ChartJS.register(
    CategoryScale,
    LinearScale,
    BarElement,
    Title,
    Tooltip,
    Legend,
    ArcElement,
    PointElement,
    LineElement,
    Filler
)

const loading = ref(true)
const reservas = ref([])
const salones = ref([])
const usuarios = ref([])

// Estadísticas generales
const stats = ref({
    totalReservas: 0,
    reservasConfirmadas: 0,
    reservasPendientes: 0,
    reservasCanceladas: 0,
    salonMasUsado: '',
    horaPico: ''
})

// Datos para gráficos
const reservasPorSalon = ref({})
const reservasPorHora = ref({})
const reservasPorDia = ref({})
const reservasPorEstado = ref({})
const reservasPorMes = ref({})

onMounted(async () => {
    await cargarDatos()
})

// Función para cargar todas las reservas (manejando paginación)
const cargarTodasReservas = async () => {
    let todasReservas = []
    let nextUrl = null
    let page = 1

    do {
        const response = await api.getReservas({ page, page_size: 100 })
        const data = response.data

        if (data.results) {
            todasReservas = [...todasReservas, ...data.results]
            nextUrl = data.next
            page++
        } else {
            // Sin paginación
            todasReservas = Array.isArray(data) ? data : []
            nextUrl = null
        }
    } while (nextUrl && page <= 20) // Límite de seguridad

    return todasReservas
}

const cargarDatos = async () => {
    loading.value = true
    try {
        // Cargar todas las reservas (sin límite de paginación)
        const [todasReservas, salonesRes, usuariosRes] = await Promise.all([
            cargarTodasReservas(),
            api.getSalones({ page_size: 100 }),
            api.getUsuarios({ page_size: 100 })
        ])

        reservas.value = todasReservas
        salones.value = salonesRes.data.results || salonesRes.data || []
        usuarios.value = usuariosRes.data.results || usuariosRes.data || []

        calcularEstadisticas()
    } catch (error) {
        console.error('Error cargando datos:', error)
    } finally {
        loading.value = false
    }
}

const calcularEstadisticas = () => {
    const reservasArray = Array.isArray(reservas.value) ? reservas.value : []

    // Estadísticas generales
    stats.value.totalReservas = reservasArray.length
    stats.value.reservasConfirmadas = reservasArray.filter(r => r.estado === 'confirmada').length
    stats.value.reservasPendientes = reservasArray.filter(r => r.estado === 'pendiente').length
    stats.value.reservasCanceladas = reservasArray.filter(r => r.estado === 'cancelada').length

    // Reservas por salón
    const porSalon = {}
    reservasArray.forEach(r => {
        // Buscar nombre del salón en la lista de salones cargados
        const salonObj = salones.value.find(s => s.id === r.salon)
        const salonNombre = r.salon_nombre || (salonObj ? salonObj.nombre : `Salón ${r.salon}`)
        porSalon[salonNombre] = (porSalon[salonNombre] || 0) + 1
    })
    reservasPorSalon.value = porSalon

    // Encontrar salón más usado
    const salonMasUsadoEntry = Object.entries(porSalon).sort((a, b) => b[1] - a[1])[0]
    stats.value.salonMasUsado = salonMasUsadoEntry ? salonMasUsadoEntry[0] : 'N/A'

    // Reservas por hora
    const porHora = {}
    for (let i = 6; i <= 22; i++) {
        porHora[`${i}:00`] = 0
    }
    reservasArray.forEach(r => {
        if (r.hora_inicio) {
            const hora = parseInt(r.hora_inicio.split(':')[0])
            const key = `${hora}:00`
            if (porHora[key] !== undefined) {
                porHora[key]++
            }
        }
    })
    reservasPorHora.value = porHora

    // Encontrar hora pico
    const horaPicoEntry = Object.entries(porHora).sort((a, b) => b[1] - a[1])[0]
    stats.value.horaPico = horaPicoEntry && horaPicoEntry[1] > 0 ? horaPicoEntry[0] : 'N/A'

    // Reservas por día de la semana
    const diasSemana = ['Domingo', 'Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado']
    const porDia = {
        'Lunes': 0, 'Martes': 0, 'Miércoles': 0,
        'Jueves': 0, 'Viernes': 0, 'Sábado': 0, 'Domingo': 0
    }
    reservasArray.forEach(r => {
        if (r.fecha) {
            // Parsear fecha correctamente (YYYY-MM-DD)
            const [year, month, day] = r.fecha.split('-').map(Number)
            const fecha = new Date(year, month - 1, day)
            const diaSemana = diasSemana[fecha.getDay()]
            porDia[diaSemana]++
        }
    })
    reservasPorDia.value = porDia

    // Reservas por estado
    reservasPorEstado.value = {
        'Confirmadas': stats.value.reservasConfirmadas,
        'Pendientes': stats.value.reservasPendientes,
        'Canceladas': stats.value.reservasCanceladas,
        'Completadas': reservasArray.filter(r => r.estado === 'completada').length
    }

    // Reservas por mes (últimos 6 meses)
    const meses = ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic']
    const porMes = {}
    const hoy = new Date()
    for (let i = 5; i >= 0; i--) {
        const fecha = new Date(hoy.getFullYear(), hoy.getMonth() - i, 1)
        const key = `${meses[fecha.getMonth()]} ${fecha.getFullYear()}`
        porMes[key] = 0
    }
    reservasArray.forEach(r => {
        if (r.fecha) {
            // Parsear fecha correctamente (YYYY-MM-DD)
            const [year, month] = r.fecha.split('-').map(Number)
            const key = `${meses[month - 1]} ${year}`
            if (porMes[key] !== undefined) {
                porMes[key]++
            }
        }
    })
    reservasPorMes.value = porMes
}

// Configuración de gráficos
const chartColors = {
    primary: '#B90A0A',
    primaryLight: 'rgba(185, 10, 10, 0.7)',
    secondary: '#3B82F6',
    success: '#10B981',
    warning: '#F59E0B',
    danger: '#EF4444',
    purple: '#8B5CF6',
    pink: '#EC4899'
}

// Datos para gráfico de barras - Reservas por Salón
const chartDataSalones = computed(() => ({
    labels: Object.keys(reservasPorSalon.value),
    datasets: [{
        label: 'Reservas',
        data: Object.values(reservasPorSalon.value),
        backgroundColor: chartColors.primary,
        borderColor: chartColors.primary,
        borderWidth: 1,
        borderRadius: 8
    }]
}))

// Datos para gráfico de líneas - Reservas por Hora
const chartDataHoras = computed(() => ({
    labels: Object.keys(reservasPorHora.value),
    datasets: [{
        label: 'Reservas por Hora',
        data: Object.values(reservasPorHora.value),
        fill: true,
        backgroundColor: 'rgba(185, 10, 10, 0.1)',
        borderColor: chartColors.primary,
        tension: 0.4,
        pointBackgroundColor: chartColors.primary,
        pointBorderColor: '#fff',
        pointBorderWidth: 2,
        pointRadius: 4
    }]
}))

// Datos para gráfico de dona - Estados
const chartDataEstados = computed(() => ({
    labels: Object.keys(reservasPorEstado.value),
    datasets: [{
        data: Object.values(reservasPorEstado.value),
        backgroundColor: [chartColors.success, chartColors.warning, chartColors.danger, chartColors.secondary],
        borderWidth: 0,
        hoverOffset: 10
    }]
}))

// Datos para gráfico de barras - Por día de semana
const chartDataDias = computed(() => ({
    labels: ['Lun', 'Mar', 'Mié', 'Jue', 'Vie', 'Sáb', 'Dom'],
    datasets: [{
        label: 'Reservas',
        data: [
            reservasPorDia.value['Lunes'],
            reservasPorDia.value['Martes'],
            reservasPorDia.value['Miércoles'],
            reservasPorDia.value['Jueves'],
            reservasPorDia.value['Viernes'],
            reservasPorDia.value['Sábado'],
            reservasPorDia.value['Domingo']
        ],
        backgroundColor: [
            chartColors.primary,
            chartColors.secondary,
            chartColors.success,
            chartColors.warning,
            chartColors.purple,
            chartColors.pink,
            chartColors.danger
        ],
        borderRadius: 8
    }]
}))

// Datos para gráfico de líneas - Tendencia mensual
const chartDataMeses = computed(() => ({
    labels: Object.keys(reservasPorMes.value),
    datasets: [{
        label: 'Reservas Mensuales',
        data: Object.values(reservasPorMes.value),
        fill: true,
        backgroundColor: 'rgba(59, 130, 246, 0.1)',
        borderColor: chartColors.secondary,
        tension: 0.4,
        pointBackgroundColor: chartColors.secondary,
        pointBorderColor: '#fff',
        pointBorderWidth: 2,
        pointRadius: 5
    }]
}))

// Opciones comunes para gráficos de barras
const barChartOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
        legend: { display: false },
        tooltip: {
            backgroundColor: 'rgba(0, 0, 0, 0.8)',
            padding: 12,
            cornerRadius: 8
        }
    },
    scales: {
        y: {
            beginAtZero: true,
            grid: { color: 'rgba(0, 0, 0, 0.05)' },
            ticks: { precision: 0 }
        },
        x: {
            grid: { display: false }
        }
    }
}

// Opciones para gráfico de líneas
const lineChartOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
        legend: { display: false },
        tooltip: {
            backgroundColor: 'rgba(0, 0, 0, 0.8)',
            padding: 12,
            cornerRadius: 8
        }
    },
    scales: {
        y: {
            beginAtZero: true,
            grid: { color: 'rgba(0, 0, 0, 0.05)' },
            ticks: { precision: 0 }
        },
        x: {
            grid: { display: false }
        }
    }
}

// Opciones para gráfico de dona
const doughnutOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
        legend: {
            position: 'bottom',
            labels: {
                padding: 20,
                usePointStyle: true,
                pointStyle: 'circle'
            }
        },
        tooltip: {
            backgroundColor: 'rgba(0, 0, 0, 0.8)',
            padding: 12,
            cornerRadius: 8
        }
    },
    cutout: '65%'
}

// Porcentaje de uso
const porcentajeConfirmadas = computed(() => {
    if (stats.value.totalReservas === 0) return 0
    return Math.round((stats.value.reservasConfirmadas / stats.value.totalReservas) * 100)
})

// Exportar a PDF
const exportando = ref(false)
const exportarPDF = async () => {
    exportando.value = true
    try {
        const elemento = document.getElementById('metricas-content')
        if (!elemento) return

        // Capturar el contenido como imagen con alta resolución
        const canvas = await html2canvas(elemento, {
            scale: 2,
            useCORS: true,
            logging: false,
            backgroundColor: '#ffffff'
        })

        const imgData = canvas.toDataURL('image/png', 1.0)

        // Crear PDF en formato landscape para mejor visualización
        const pdf = new jsPDF('l', 'mm', 'a4')

        const pdfWidth = pdf.internal.pageSize.getWidth()
        const pdfHeight = pdf.internal.pageSize.getHeight()

        // Fecha actual
        const fecha = new Date()
        const fechaFormateada = fecha.toLocaleDateString('es-CO', {
            year: 'numeric',
            month: 'long',
            day: 'numeric',
            hour: '2-digit',
            minute: '2-digit'
        })

        // Título del PDF
        pdf.setFontSize(16)
        pdf.setTextColor(185, 10, 10)
        pdf.text('GECOS - Reporte de Métricas', pdfWidth / 2, 12, { align: 'center' })

        pdf.setFontSize(10)
        pdf.setTextColor(100, 100, 100)
        pdf.text(`Fecha de generación: ${fechaFormateada}`, pdfWidth / 2, 18, { align: 'center' })

        // Calcular dimensiones para que TODO quepa en una página
        const imgWidth = canvas.width
        const imgHeight = canvas.height
        const startY = 22
        const marginX = 5
        const availableWidth = pdfWidth - (marginX * 2)
        const availableHeight = pdfHeight - startY - 8

        // Escalar para que quepa todo en una página
        const scaleX = availableWidth / imgWidth
        const scaleY = availableHeight / imgHeight
        const scale = Math.min(scaleX, scaleY)

        const finalWidth = imgWidth * scale
        const finalHeight = imgHeight * scale
        const imgX = (pdfWidth - finalWidth) / 2

        // Añadir imagen - todo en una página
        pdf.addImage(imgData, 'PNG', imgX, startY, finalWidth, finalHeight)

        // Pie de página
        pdf.setFontSize(8)
        pdf.setTextColor(150, 150, 150)
        pdf.text('Sistema GECOS - Gestión de Espacios | FESC', pdfWidth / 2, pdfHeight - 3, { align: 'center' })

        // Descargar
        const nombreArchivo = `GECOS_Metricas_${fecha.toISOString().split('T')[0]}.pdf`
        pdf.save(nombreArchivo)

    } catch (error) {
        console.error('Error exportando PDF:', error)
    } finally {
        exportando.value = false
    }
}
</script>

<template>
    <div class="min-h-screen bg-gray-50 dark:bg-gray-900 transition-colors duration-200">
        <Header />

        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
            <!-- Header -->
            <div class="mb-8">
                <div class="flex items-center justify-between">
                    <div class="flex items-center gap-3">
                        <div class="bg-[#B90A0A] p-3 rounded-xl shadow-lg">
                            <svg class="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                    d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
                            </svg>
                        </div>
                        <div>
                            <h1 class="text-3xl font-bold text-gray-800 dark:text-white">Panel de Métricas</h1>
                            <p class="text-gray-500 dark:text-gray-400">Estadísticas y análisis del uso de espacios</p>
                        </div>
                    </div>
                    <!-- Botón Exportar PDF -->
                    <button @click="exportarPDF" :disabled="exportando || loading"
                        class="flex items-center gap-2 bg-[#B90A0A] hover:bg-red-700 text-white px-4 py-2 rounded-lg shadow-md transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed">
                        <svg v-if="!exportando" class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                        </svg>
                        <svg v-else class="w-5 h-5 animate-spin" fill="none" viewBox="0 0 24 24">
                            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4">
                            </circle>
                            <path class="opacity-75" fill="currentColor"
                                d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z">
                            </path>
                        </svg>
                        {{ exportando ? 'Exportando...' : 'Exportar PDF' }}
                    </button>
                </div>
            </div>

            <!-- Loading -->
            <div v-if="loading" class="flex justify-center items-center py-20">
                <div class="animate-spin rounded-full h-16 w-16 border-4 border-[#B90A0A] border-t-transparent"></div>
            </div>

            <div v-else id="metricas-content">
                <!-- Cards de Estadísticas -->
                <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
                    <!-- Total Reservas -->
                    <div
                        class="bg-white dark:bg-gray-800 rounded-2xl shadow-lg p-6 border border-gray-100 dark:border-gray-700 transform hover:scale-105 transition-transform duration-300">
                        <div class="flex items-center justify-between">
                            <div>
                                <p class="text-gray-500 dark:text-gray-400 text-sm font-medium">Total Reservas</p>
                                <p class="text-4xl font-bold text-gray-800 dark:text-white mt-1">{{ stats.totalReservas
                                }}</p>
                            </div>
                            <div class="bg-blue-100 dark:bg-blue-900/30 p-4 rounded-xl">
                                <svg class="w-8 h-8 text-blue-600 dark:text-blue-400" fill="none" stroke="currentColor"
                                    viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                        d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                                </svg>
                            </div>
                        </div>
                        <div class="mt-4 flex items-center text-sm">
                            <span class="text-green-500 font-semibold">{{ porcentajeConfirmadas }}%</span>
                            <span class="text-gray-400 ml-2">confirmadas</span>
                        </div>
                    </div>

                    <!-- Confirmadas -->
                    <div
                        class="bg-white dark:bg-gray-800 rounded-2xl shadow-lg p-6 border border-gray-100 dark:border-gray-700 transform hover:scale-105 transition-transform duration-300">
                        <div class="flex items-center justify-between">
                            <div>
                                <p class="text-gray-500 dark:text-gray-400 text-sm font-medium">Confirmadas</p>
                                <p class="text-4xl font-bold text-green-600 dark:text-green-400 mt-1">{{
                                    stats.reservasConfirmadas }}</p>
                            </div>
                            <div class="bg-green-100 dark:bg-green-900/30 p-4 rounded-xl">
                                <svg class="w-8 h-8 text-green-600 dark:text-green-400" fill="none"
                                    stroke="currentColor" viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                        d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                                </svg>
                            </div>
                        </div>
                        <div class="mt-4 h-2 bg-gray-200 dark:bg-gray-700 rounded-full overflow-hidden">
                            <div class="h-full bg-green-500 rounded-full transition-all duration-500"
                                :style="{ width: `${porcentajeConfirmadas}%` }"></div>
                        </div>
                    </div>

                    <!-- Salón más usado -->
                    <div
                        class="bg-white dark:bg-gray-800 rounded-2xl shadow-lg p-6 border border-gray-100 dark:border-gray-700 transform hover:scale-105 transition-transform duration-300">
                        <div class="flex items-center justify-between">
                            <div>
                                <p class="text-gray-500 dark:text-gray-400 text-sm font-medium">Salón Más Usado</p>
                                <p class="text-xl font-bold text-gray-800 dark:text-white mt-1 truncate">{{
                                    stats.salonMasUsado }}</p>
                            </div>
                            <div class="bg-purple-100 dark:bg-purple-900/30 p-4 rounded-xl">
                                <svg class="w-8 h-8 text-purple-600 dark:text-purple-400" fill="none"
                                    stroke="currentColor" viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                        d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
                                </svg>
                            </div>
                        </div>
                    </div>

                    <!-- Hora Pico -->
                    <div
                        class="bg-white dark:bg-gray-800 rounded-2xl shadow-lg p-6 border border-gray-100 dark:border-gray-700 transform hover:scale-105 transition-transform duration-300">
                        <div class="flex items-center justify-between">
                            <div>
                                <p class="text-gray-500 dark:text-gray-400 text-sm font-medium">Hora Pico</p>
                                <p class="text-4xl font-bold text-orange-600 dark:text-orange-400 mt-1">{{
                                    stats.horaPico }}</p>
                            </div>
                            <div class="bg-orange-100 dark:bg-orange-900/30 p-4 rounded-xl">
                                <svg class="w-8 h-8 text-orange-600 dark:text-orange-400" fill="none"
                                    stroke="currentColor" viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                        d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                                </svg>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Gráficos -->
                <div class="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
                    <!-- Reservas por Salón -->
                    <div
                        class="bg-white dark:bg-gray-800 rounded-2xl shadow-lg p-6 border border-gray-100 dark:border-gray-700">
                        <h3 class="text-lg font-bold text-gray-800 dark:text-white mb-4 flex items-center">
                            <svg class="w-5 h-5 text-[#B90A0A] mr-2" fill="none" stroke="currentColor"
                                viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                    d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
                            </svg>
                            Reservas por Salón
                        </h3>
                        <div class="h-64">
                            <Bar :data="chartDataSalones" :options="barChartOptions" />
                        </div>
                    </div>

                    <!-- Estado de Reservas -->
                    <div
                        class="bg-white dark:bg-gray-800 rounded-2xl shadow-lg p-6 border border-gray-100 dark:border-gray-700">
                        <h3 class="text-lg font-bold text-gray-800 dark:text-white mb-4 flex items-center">
                            <svg class="w-5 h-5 text-[#B90A0A] mr-2" fill="none" stroke="currentColor"
                                viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                    d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
                            </svg>
                            Estado de Reservas
                        </h3>
                        <div class="h-64">
                            <Doughnut :data="chartDataEstados" :options="doughnutOptions" />
                        </div>
                    </div>

                    <!-- Reservas por Hora -->
                    <div
                        class="bg-white dark:bg-gray-800 rounded-2xl shadow-lg p-6 border border-gray-100 dark:border-gray-700">
                        <h3 class="text-lg font-bold text-gray-800 dark:text-white mb-4 flex items-center">
                            <svg class="w-5 h-5 text-[#B90A0A] mr-2" fill="none" stroke="currentColor"
                                viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                    d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                            </svg>
                            Distribución por Hora
                        </h3>
                        <div class="h-64">
                            <Line :data="chartDataHoras" :options="lineChartOptions" />
                        </div>
                    </div>

                    <!-- Reservas por Día -->
                    <div
                        class="bg-white dark:bg-gray-800 rounded-2xl shadow-lg p-6 border border-gray-100 dark:border-gray-700">
                        <h3 class="text-lg font-bold text-gray-800 dark:text-white mb-4 flex items-center">
                            <svg class="w-5 h-5 text-[#B90A0A] mr-2" fill="none" stroke="currentColor"
                                viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                    d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                            </svg>
                            Reservas por Día de la Semana
                        </h3>
                        <div class="h-64">
                            <Bar :data="chartDataDias" :options="barChartOptions" />
                        </div>
                    </div>
                </div>

                <!-- Tendencia Mensual (Full Width) -->
                <div
                    class="bg-white dark:bg-gray-800 rounded-2xl shadow-lg p-6 border border-gray-100 dark:border-gray-700 mb-8">
                    <h3 class="text-lg font-bold text-gray-800 dark:text-white mb-4 flex items-center">
                        <svg class="w-5 h-5 text-[#B90A0A] mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                d="M7 12l3-3 3 3 4-4M8 21l4-4 4 4M3 4h18M4 4h16v12a1 1 0 01-1 1H5a1 1 0 01-1-1V4z" />
                        </svg>
                        Tendencia de Reservas (Últimos 6 meses)
                    </h3>
                    <div class="h-80">
                        <Line :data="chartDataMeses" :options="lineChartOptions" />
                    </div>
                </div>

                <!-- Información adicional -->
                <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
                    <div class="bg-gradient-to-br from-[#B90A0A] to-red-700 rounded-2xl shadow-lg p-6 text-white">
                        <div class="flex items-center mb-4">
                            <svg class="w-10 h-10 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                    d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
                            </svg>
                            <div>
                                <p class="text-white/80 text-sm">Total Usuarios</p>
                                <p class="text-3xl font-bold">{{ usuarios.length }}</p>
                            </div>
                        </div>
                    </div>

                    <div class="bg-gradient-to-br from-blue-600 to-blue-800 rounded-2xl shadow-lg p-6 text-white">
                        <div class="flex items-center mb-4">
                            <svg class="w-10 h-10 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                    d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
                            </svg>
                            <div>
                                <p class="text-white/80 text-sm">Total Salones</p>
                                <p class="text-3xl font-bold">{{ salones.length }}</p>
                            </div>
                        </div>
                    </div>

                    <div class="bg-gradient-to-br from-green-600 to-green-800 rounded-2xl shadow-lg p-6 text-white">
                        <div class="flex items-center mb-4">
                            <svg class="w-10 h-10 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                    d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                            </svg>
                            <div>
                                <p class="text-white/80 text-sm">Tasa de Éxito</p>
                                <p class="text-3xl font-bold">{{ porcentajeConfirmadas }}%</p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>
