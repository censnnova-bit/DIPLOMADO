import axios from 'axios'

// Usamos la variable de entorno si existe, o '/api' por defecto para producción relativa,
// o el localhost explícito (puerto 8000) para desarrollo local sin docker.
const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api'

// Configurar axios para incluir el token en todas las peticiones EXCEPT en login
axios.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token')
    if (token && !config.url.includes('/login/')) {
      config.headers.Authorization = `Token ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

export default {
  // Autenticación
  login(credentials) {
    return axios.post(`${API_URL}/login/`, credentials)
  },
  
  logout() {
    return axios.post(`${API_URL}/logout/`)
  },

  // Salones
  getSalones(params = {}) {
    return axios.get(`${API_URL}/salones/`, { params })
  },

  getSalon(id) {
    return axios.get(`${API_URL}/salones/${id}/`)
  },

  createSalon(data) {
    return axios.post(`${API_URL}/salones/`, data)
  },

  updateSalon(id, data) {
    return axios.patch(`${API_URL}/salones/${id}/`, data)
  },

  deleteSalon(id) {
    return axios.delete(`${API_URL}/salones/${id}/`)
  },

  getSalonesDisponibles(fecha, horaInicio, horaFin) {
    return axios.get(`${API_URL}/salones/disponibles/`, {
      params: { fecha, hora_inicio: horaInicio, hora_fin: horaFin }
    })
  },

  // Reservas
  getReservas(params = {}) {
    return axios.get(`${API_URL}/reservas/`, { params })
  },

  getMisReservas() {
    return axios.get(`${API_URL}/reservas/mis_reservas/`)
  },

  getReservasPorSalon(salonId) {
    return axios.get(`${API_URL}/reservas/`, { 
      params: { 
        salon: salonId,
        timestamp: new Date().getTime() // Cache buster
      } 
    })
  },

  createReserva(data) {
    return axios.post(`${API_URL}/reservas/`, data)
  },

  cancelarReserva(id) {
    return axios.post(`${API_URL}/reservas/${id}/cancelar/`)
  },

  updateReserva(id, data) {
    return axios.patch(`${API_URL}/reservas/${id}/`, data)
  },

  // Asignaturas
  getAsignaturas() {
    return axios.get(`${API_URL}/asignaturas/`)
  },
  
  createAsignatura(data) {
    return axios.post(`${API_URL}/asignaturas/`, data)
  },
  
  updateAsignatura(id, data) {
    return axios.put(`${API_URL}/asignaturas/${id}/`, data)
  },
  
  deleteAsignatura(id) {
    return axios.delete(`${API_URL}/asignaturas/${id}/`)
  },

  confirmarReserva(id) {
    return axios.post(`${API_URL}/reservas/${id}/confirmar/`)
  },

  // Usuarios
  getUsuario() {
    return axios.get(`${API_URL}/usuarios/me/`)
  },

  getUsuarios(params = {}) {
    return axios.get(`${API_URL}/usuarios/`, { params })
  },

  crearDocente(data) {
    return axios.post(`${API_URL}/usuarios/crear_docente/`, data)
  },

  actualizarUsuario(id, data) {
    return axios.patch(`${API_URL}/usuarios/${id}/`, data)
  },

  eliminarUsuario(id) {
    return axios.delete(`${API_URL}/usuarios/${id}/`)
  },

  // Métodos genéricos para peticiones HTTP
  get(url, config = {}) {
    return axios.get(`${API_URL}${url}`, config)
  },

  post(url, data, config = {}) {
    return axios.post(`${API_URL}${url}`, data, config)
  },

  put(url, data, config = {}) {
    return axios.put(`${API_URL}${url}`, data, config)
  },

  patch(url, data, config = {}) {
    return axios.patch(`${API_URL}${url}`, data, config)
  },

  delete(url, config = {}) {
    return axios.delete(`${API_URL}${url}`, config)
  }
}
