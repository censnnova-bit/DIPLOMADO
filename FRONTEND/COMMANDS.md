# 🚀 Comandos Útiles - Vue + Tailwind

## Comandos Básicos

### Iniciar desarrollo
```bash
npm run dev
```

### Compilar para producción
```bash
npm run build
```

### Previsualizar build de producción
```bash
npm run preview
```

## Gestión de Dependencias

### Actualizar dependencias
```bash
npm update
```

### Ver dependencias desactualizadas
```bash
npm outdated
```

### Instalar una nueva dependencia
```bash
npm install nombre-del-paquete
```

### Instalar como dependencia de desarrollo
```bash
npm install -D nombre-del-paquete
```

## Comandos de Tailwind

### Regenerar archivo de configuración
```bash
npx tailwindcss init
```

### Ver todas las clases disponibles
```bash
npx tailwindcss --help
```

## Utilidades de Proyecto

### Limpiar cache y reinstalar
```bash
rm -rf node_modules package-lock.json
npm install
```

### Ver tamaño del build
```bash
npm run build
du -sh dist/
```

### Analizar dependencias
```bash
npm list --depth=0
```

## Debugging

### Ver versiones instaladas
```bash
npm list vue vite tailwindcss
```

### Limpiar cache de npm
```bash
npm cache clean --force
```

### Verificar problemas
```bash
npm doctor
```

## Git (opcional)

### Inicializar repositorio
```bash
git init
git add .
git commit -m "Initial commit: Vue 3 + Tailwind CSS project"
```

## Tailwind CSS Play CDN (para pruebas rápidas)
Agrega esto en el `<head>` de index.html solo para desarrollo:
```html
<script src="https://cdn.tailwindcss.com"></script>
```
⚠️ **No usar en producción** - Solo para prototipos rápidos

## Crear Componentes Nuevos

### Estructura recomendada
```bash
# Componente funcional
src/components/MiComponente.vue

# Composable (lógica reutilizable)
src/composables/useMiLogica.js

# Utilidades
src/utils/helpers.js
```

## Hot Tips 🔥

1. **Reiniciar dev server:** Ctrl+C y luego `npm run dev`
2. **Limpiar dist:** `rm -rf dist`
3. **Puerto diferente:** `npm run dev -- --port 3000`
4. **Abrir automáticamente:** `npm run dev -- --open`
5. **Ver en red local:** `npm run dev -- --host`

## Solución de Problemas Comunes

### Error: "Cannot find module"
```bash
rm -rf node_modules package-lock.json
npm install
```

### Tailwind no aplica estilos
1. Verificar `src/style.css` contiene las directivas @tailwind
2. Verificar que `main.js` importa `./style.css`
3. Limpiar cache: Ctrl+Shift+R en el navegador

### Puerto 5173 ocupado
```bash
npm run dev -- --port 5174
```

### Build muy grande
1. Verificar que no estés importando toda una librería
2. Usar imports específicos: `import { ref } from 'vue'`
3. El CSS de Tailwind se purga automáticamente en producción

---

**¿Necesitas ayuda?**
- Vue: https://vuejs.org/guide/
- Vite: https://vitejs.dev/guide/
- Tailwind: https://tailwindcss.com/docs
