import axios from 'axios'

const API_URL = 'http://localhost:8069/api'

// Configurar axios para incluir el token en todas las peticiones
axios.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token')
    if (token) {
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
    return axios.put(`${API_URL}/salones/${id}/`, data)
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
    return axios.get(`${API_URL}/reservas/`, { params: { salon: salonId } })
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

  confirmarReserva(id) {
    return axios.post(`${API_URL}/reservas/${id}/confirmar/`)
  },

  // Usuarios
  getUsuario() {
    return axios.get(`${API_URL}/usuarios/me/`)
  }
}
