# Proyecto Vue 3 + Tailwind CSS

Proyecto frontend configurado con las últimas versiones de Vue 3, Vite 5 y Tailwind CSS 3.

## 🚀 Características

- ✅ **Vue 3.4+** - Framework JavaScript progresivo con Composition API
- ✅ **Vite 5** - Herramienta de construcción ultrarrápida con HMR
- ✅ **Tailwind CSS 3.4** - Framework CSS de utilidades completamente configurado
- ✅ **PostCSS** - Procesador CSS con autoprefixer
- ✅ **Hot Module Replacement** - Recarga instantánea durante el desarrollo

## 📦 Instalación

Las dependencias ya están instaladas. Si necesitas reinstalar:

```bash
npm install
```

## 🛠️ Comandos Disponibles

### Modo Desarrollo
Inicia el servidor de desarrollo con hot-reload:
```bash
npm run dev
```
El servidor estará disponible en `http://localhost:5173/`

### Compilación para Producción
Compila y minifica para producción:
```bash
npm run build
```
Los archivos optimizados se generarán en la carpeta `dist/`

### Vista Previa de Producción
Previsualiza la compilación de producción localmente:
```bash
npm run preview
```

## 📁 Estructura del Proyecto

```
FRONTEND/
├── public/              # Archivos estáticos
│   └── vite.svg        # Logo de Vite
├── src/
│   ├── components/     # Componentes Vue reutilizables
│   │   └── Card.vue    # Componente de tarjeta de ejemplo
│   ├── App.vue         # Componente raíz con ejemplo de Tailwind
│   ├── main.js         # Punto de entrada de la aplicación
│   └── style.css       # Estilos globales con directivas de Tailwind
├── index.html          # Plantilla HTML
├── package.json        # Dependencias y scripts
├── vite.config.js      # Configuración de Vite
├── tailwind.config.js  # Configuración de Tailwind CSS
└── postcss.config.js   # Configuración de PostCSS
```

## 🎨 Usando Tailwind CSS

Tailwind CSS está completamente configurado y listo para usar. Ejemplo:

```vue
<template>
  <div class="flex items-center justify-center min-h-screen bg-gradient-to-r from-blue-500 to-purple-600">
    <div class="bg-white rounded-lg shadow-xl p-8">
      <h1 class="text-3xl font-bold text-gray-800 mb-4">
        ¡Hola Mundo!
      </h1>
      <button class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded">
        Botón de ejemplo
      </button>
    </div>
  </div>
</template>
```

## 📚 Recursos

- [Documentación de Vue 3](https://vuejs.org/)
- [Documentación de Vite](https://vitejs.dev/)
- [Documentación de Tailwind CSS](https://tailwindcss.com/)
- [Tailwind CSS Cheat Sheet](https://nerdcave.com/tailwind-cheat-sheet)

## 💡 Componentes de Ejemplo

El proyecto incluye un componente `Card.vue` en `src/components/` que demuestra:
- Props de Vue
- Clases de Tailwind CSS
- Transiciones y efectos hover
- Estructura semántica

## 🔥 Características de Tailwind Configuradas

- ✅ Autoprefixer para compatibilidad con navegadores
- ✅ Purga automática de CSS no utilizado en producción
- ✅ Escaneo de archivos `.vue`, `.js`, `.ts`, `.jsx`, `.tsx`
- ✅ Hot reload de configuración
- ✅ Utilidades personalizables en `tailwind.config.js`

## 📝 Notas

- El proyecto usa ESM (ES Modules)
- Vue 3 con Composition API
- Configuración mínima y lista para escalar
- Optimizado para desarrollo y producción

---

**¡Tu proyecto Vue + Tailwind está listo para usar! 🎉**

Para comenzar, ejecuta:
```bash
npm run dev
```
