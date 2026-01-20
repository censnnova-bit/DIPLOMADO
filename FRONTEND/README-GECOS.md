# 🏫 GECOS - Sistema de Gestión de Espacios

Sistema web para la gestión y reserva de aulas y espacios académicos desarrollado con Vue 3, Vite y Tailwind CSS.

## ✨ Características

### 🎯 Vista de Listado de Aulas
- **Grid responsivo** de tarjetas de aulas
- **Filtros avanzados**: bloque/piso, fecha, capacidad, recursos
- **Estados visuales**: Disponible, Ocupado, Mantenimiento, Clase próxima
- **Barras de ocupación** horaria en tiempo real
- **Dark mode** integrado
- **Paginación** funcional

### 📅 Vista de Detalle con Calendario
- **Panel de información** completa del aula
- **Calendario semanal** interactivo
- **Estados de reserva**: Libre, Ocupado, Tu Selección, Reservado
- **Navegación** entre semanas
- **Modal de confirmación** de reserva
- **Breadcrumb** de navegación

## 🚀 Inicio Rápido

### Prerrequisitos
- Node.js 16+ y npm

### Instalación

El proyecto ya está configurado. Para reinstalar dependencias:

```bash
cd FRONTEND
npm install
```

### Desarrollo

```bash
npm run dev
```

Abre http://localhost:5174 en tu navegador

### Compilación

```bash
npm run build
```

### Vista Previa

```bash
npm run preview
```

## 📁 Estructura del Proyecto

```
FRONTEND/
├── src/
│   ├── components/
│   │   ├── Header.vue           # Header con navegación y dark mode
│   │   └── ClassroomCard.vue    # Tarjeta de aula reutilizable
│   ├── views/
│   │   ├── ClassroomList.vue    # Vista principal (listado)
│   │   └── ClassroomDetail.vue  # Vista de detalle con calendario
│   ├── router/
│   │   └── index.js             # Configuración de rutas
│   ├── App.vue                  # Componente raíz
│   ├── main.js                  # Punto de entrada
│   └── style.css                # Estilos globales (Tailwind)
├── public/                      # Archivos estáticos
├── index.html                   # Template HTML
├── vite.config.js               # Config de Vite
├── tailwind.config.js           # Config de Tailwind
└── package.json                 # Dependencias

```

## 🎨 Tecnologías

- **Vue 3.5.26** - Framework JavaScript progresivo
- **Vue Router 4** - Enrutamiento oficial de Vue
- **Vite 5.4.21** - Build tool ultrarrápido
- **Tailwind CSS 3.4.19** - Framework CSS de utilidades
- **PostCSS + Autoprefixer** - Procesamiento CSS

## 🧭 Rutas

| Ruta | Componente | Descripción |
|------|-----------|-------------|
| `/` | Redirect | Redirige a /salones |
| `/salones` | ClassroomList | Listado de aulas con filtros |
| `/aula/:id` | ClassroomDetail | Detalle de aula con calendario |
| `/reservas` | MyReservations | Mis reservas (placeholder) |

## 🎨 Paleta de Colores

```css
--primary: #B90A0A        /* Rojo corporativo */
--primary-dark: #8f0606   /* Hover states */
--green-500: #10b981      /* Disponible */
--yellow-500: #eab308     /* Ocupado/Próximo */
--red-500: #ef4444        /* Mantenimiento */
--blue-500: #3b82f6       /* Selección usuario */
```

## 📦 Componentes Principales

### Header.vue
- Navegación responsive
- Toggle dark mode
- Logo y branding GECOS
- Efecto wave decorativo

### ClassroomCard.vue
- Props dinámicas para datos de aula
- Estados visuales (badges)
- Barras de ocupación horaria
- Botones contextuales según estado
- Transiciones y hover effects

### ClassroomList.vue
- Sistema de filtros
- Grid responsivo (1/2/3 columnas)
- Mock data de 6 aulas
- Paginación
- Footer corporativo

### ClassroomDetail.vue
- Panel lateral con info del aula
- Calendario semanal 5 días x 5 horas
- Interacción con slots de tiempo
- Modal de confirmación
- Breadcrumb navigation

## 🔧 Características Técnicas

### Responsivo
- Mobile-first design
- Breakpoints: sm, md, lg, xl
- Grid adaptativo
- Menú hamburguesa en móvil

### Dark Mode
- Toggle manual en header
- Persistencia con localStorage (pendiente)
- Colores optimizados para ambos modos

### Accesibilidad
- Navegación por teclado
- Labels semánticos
- ARIA attributes
- Contrast ratios optimizados

### Performance
- Code splitting con lazy loading
- Imágenes optimizadas
- CSS purgado en producción
- Tree shaking automático

## 🛠️ Desarrollo

### Agregar una nueva vista

1. Crear archivo en `src/views/NuevaVista.vue`
2. Agregar ruta en `src/router/index.js`
3. Actualizar navegación en Header si necesario

### Agregar un componente

1. Crear archivo en `src/components/NuevoComponente.vue`
2. Importar y usar en la vista deseada

### Mock Data

Actualmente usa datos estáticos en cada vista. Para conectar con backend:

1. Crear servicio API en `src/services/api.js`
2. Reemplazar datos estáticos con llamadas API
3. Agregar manejo de loading y errores

## 📝 Próximas Funcionalidades

- [ ] Conexión con API backend
- [ ] Autenticación de usuarios
- [ ] Persistencia de reservas
- [ ] Notificaciones
- [ ] Vista "Mis Reservas" funcional
- [ ] Drag & drop en calendario
- [ ] Exportar horarios a PDF
- [ ] Integración con calendario Google/Outlook
- [ ] Sistema de permisos (admin/docente/estudiante)
- [ ] Dashboard de estadísticas

## 🐛 Solución de Problemas

### El servidor no inicia
```bash
# Limpiar node_modules y reinstalar
rm -rf node_modules package-lock.json
npm install
```

### Errores de Tailwind
```bash
# Verificar configuración en tailwind.config.js
# Asegurar que style.css tiene las directivas @tailwind
```

### Rutas no funcionan
```bash
# Verificar que vue-router está instalado
npm install vue-router@4
```

## 📸 Screenshots

### Vista de Listado
- Grid de 6 aulas con diferentes estados
- Filtros funcionales
- Paginación

### Vista de Detalle
- Calendario semanal interactivo
- Panel de información del aula
- Modal de confirmación

## 👥 Créditos

**Fundación de Estudios Superiores Comfanorte FESC**
"Comprometidos Con Calidad y Excelencia"

---

**Desarrollado con** ❤️ usando Vue 3 + Tailwind CSS
