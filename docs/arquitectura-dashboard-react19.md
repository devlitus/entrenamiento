# Guía de Diseño - Dashboard Neural Trainer

## 🎨 Sistema de Diseño

### Paleta de Colores

#### Colores Primarios
```css
/* Azul Principal - Para acciones primarias y elementos destacados */
--blue-50: #eff6ff;
--blue-100: #dbeafe;
--blue-500: #3b82f6;
--blue-600: #2563eb;
--blue-700: #1d4ed8;

/* Grises - Para texto, bordes y fondos */
--gray-50: #f9fafb;
--gray-100: #f3f4f6;
--gray-200: #e5e7eb;
--gray-300: #d1d5db;
--gray-600: #4b5563;
--gray-700: #374151;
--gray-900: #111827;
```

#### Colores de Estado
```css
/* Verde - Éxito, completado */
--green-100: #dcfce7;
--green-500: #22c55e;
--green-600: #16a34a;

/* Rojo - Error, peligro */
--red-100: #fee2e2;
--red-500: #ef4444;
--red-600: #dc2626;

/* Amarillo - Advertencia */
--yellow-100: #fef3c7;
--yellow-500: #eab308;
--yellow-600: #ca8a04;
```

### Tipografía

#### Jerarquía de Texto
```css
/* Títulos principales */
.text-3xl { font-size: 1.875rem; font-weight: 700; } /* H1 */
.text-2xl { font-size: 1.5rem; font-weight: 600; }   /* H2 */
.text-xl { font-size: 1.25rem; font-weight: 600; }   /* H3 */
.text-lg { font-size: 1.125rem; font-weight: 500; }  /* H4 */

/* Texto de contenido */
.text-base { font-size: 1rem; }      /* Texto normal */
.text-sm { font-size: 0.875rem; }    /* Texto secundario */
.text-xs { font-size: 0.75rem; }     /* Texto pequeño */
```

### Espaciado y Layout

#### Sistema de Espaciado (Tailwind)
```css
/* Espacios internos (padding) */
p-2: 0.5rem    p-4: 1rem      p-6: 1.5rem
p-8: 2rem      p-12: 3rem

/* Márgenes */
m-2: 0.5rem    m-4: 1rem      m-6: 1.5rem
m-8: 2rem      m-12: 3rem

/* Espacios entre elementos */
space-x-2: 0.5rem    space-x-4: 1rem    space-x-6: 1.5rem
space-y-2: 0.5rem    space-y-4: 1rem    space-y-6: 1.5rem
```

#### Bordes y Sombras
```css
/* Bordes redondeados */
rounded-lg: 0.5rem     /* Componentes estándar */
rounded-xl: 0.75rem    /* Cards y contenedores */
rounded-full: 9999px   /* Botones circulares, badges */

/* Sombras */
shadow-sm: 0 1px 2px rgba(0, 0, 0, 0.05)      /* Elementos sutiles */
shadow: 0 1px 3px rgba(0, 0, 0, 0.1)          /* Cards estándar */
shadow-lg: 0 10px 15px rgba(0, 0, 0, 0.1)     /* Modales, dropdowns */
```

---

## 🧩 Componentes de Diseño

### 1. Layout Principal

#### Estructura Visual
```
┌─────────────────────────────────────────────────────────┐
│ Header (bg-white, border-b border-gray-200)            │
├─────────────────────────────────────────────────────────┤
│ Sidebar │ Main Content Area                            │
│ (w-64)  │ (flex-1, bg-gray-50)                        │
│ Dark    │                                              │
│ Theme   │ ┌─────────────────────────────────────────┐ │
│         │ │ Content Cards                           │ │
│         │ │ (bg-white, rounded-lg, shadow-sm)       │ │
│         │ └─────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────┘
```

#### Header
- **Fondo**: Blanco (`bg-white`)
- **Borde inferior**: Gris claro (`border-b border-gray-200`)
- **Altura**: 64px (`h-16`)
- **Padding**: Horizontal 24px (`px-6`)

#### Sidebar
- **Ancho**: 256px (`w-64`) / 64px (`w-16`) colapsado
- **Fondo**: Gris oscuro (`bg-gray-900`)
- **Texto**: Blanco (`text-white`)
- **Transición**: Suave (`transition-all duration-300`)

### 2. Componentes Base

#### Botones
```css
/* Botón Primario */
.btn-primary {
  background: #2563eb;
  color: white;
  padding: 0.5rem 1rem;
  border-radius: 0.5rem;
  font-weight: 500;
  transition: all 0.2s;
}
.btn-primary:hover { background: #1d4ed8; }

/* Botón Secundario */
.btn-secondary {
  background: #f3f4f6;
  color: #374151;
  border: 1px solid #d1d5db;
}
.btn-secondary:hover { background: #e5e7eb; }
```

#### Cards
```css
.card {
  background: white;
  border-radius: 0.5rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  border: 1px solid #e5e7eb;
  padding: 1.5rem;
}
```

#### Inputs
```css
.input {
  width: 100%;
  padding: 0.5rem 0.75rem;
  border: 1px solid #d1d5db;
  border-radius: 0.5rem;
  font-size: 0.875rem;
}
.input:focus {
  outline: none;
  border-color: #2563eb;
  box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.1);
}
```

### 3. Widgets Especializados

#### Metric Cards
```css
.metric-card {
  background: white;
  padding: 1.5rem;
  border-radius: 0.5rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  border: 1px solid #e5e7eb;
}

.metric-value {
  font-size: 1.875rem;
  font-weight: 700;
  color: #111827;
  margin-bottom: 0.25rem;
}

.metric-label {
  font-size: 0.875rem;
  color: #6b7280;
  font-weight: 500;
}
```

#### Status Badges
```css
/* Badge de Éxito */
.badge-success {
  background: #dcfce7;
  color: #166534;
  padding: 0.25rem 0.75rem;
  border-radius: 9999px;
  font-size: 0.75rem;
  font-weight: 500;
}

/* Badge de Error */
.badge-error {
  background: #fee2e2;
  color: #991b1b;
}

/* Badge de Advertencia */
.badge-warning {
  background: #fef3c7;
  color: #92400e;
}
```

### 4. Gráficos y Visualizaciones

#### Contenedor de Gráficos
```css
.chart-container {
  background: white;
  border-radius: 0.5rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  border: 1px solid #e5e7eb;
}

.chart-header {
  padding: 1.5rem 1.5rem 0;
  border-bottom: 1px solid #e5e7eb;
}

.chart-content {
  padding: 1.5rem;
  height: 400px; /* Altura estándar para gráficos */
}
```

#### Colores para Gráficos
```css
/* Líneas de métricas */
--chart-primary: #2563eb;    /* Azul - Accuracy */
--chart-secondary: #dc2626;  /* Rojo - Loss */
--chart-success: #16a34a;    /* Verde - Validation */
--chart-warning: #ca8a04;    /* Amarillo - Warning */
```

---

## 📱 Responsive Design

### Breakpoints
```css
/* Mobile First */
sm: 640px    /* Tablet pequeña */
md: 768px    /* Tablet */
lg: 1024px   /* Desktop pequeño */
xl: 1280px   /* Desktop */
2xl: 1536px  /* Desktop grande */
```

### Adaptaciones por Dispositivo

#### Mobile (< 768px)
- Sidebar se convierte en overlay
- Header se simplifica (solo título y menú hamburguesa)
- Cards ocupan ancho completo
- Gráficos se ajustan verticalmente

#### Tablet (768px - 1024px)
- Sidebar colapsado por defecto
- Grid de 2 columnas para cards
- Gráficos mantienen proporción

#### Desktop (> 1024px)
- Layout completo con sidebar expandido
- Grid de 3-4 columnas para cards
- Gráficos en tamaño completo

---

## 🎯 Estados Interactivos

### Hover States
```css
/* Botones */
.btn:hover { transform: translateY(-1px); }

/* Cards */
.card:hover { box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); }

/* Links de navegación */
.nav-link:hover { background: rgba(255, 255, 255, 0.1); }
```

### Focus States
```css
/* Elementos focusables */
.focusable:focus {
  outline: 2px solid #2563eb;
  outline-offset: 2px;
}
```

### Loading States
```css
/* Skeleton loading */
.skeleton {
  background: linear-gradient(90deg, #f3f4f6 25%, #e5e7eb 50%, #f3f4f6 75%);
  background-size: 200% 100%;
  animation: loading 1.5s infinite;
}

@keyframes loading {
  0% { background-position: 200% 0; }
  100% { background-position: -200% 0; }
}
```

---

## ✨ Animaciones y Transiciones

### Transiciones Estándar
```css
/* Transición suave para la mayoría de elementos */
.transition-smooth { transition: all 0.2s ease-in-out; }

/* Transición para sidebar */
.sidebar-transition { transition: width 0.3s ease-in-out; }

/* Fade in/out */
.fade-enter { opacity: 0; transform: translateY(10px); }
.fade-enter-active { opacity: 1; transform: translateY(0); }
```

### Micro-interacciones
```css
/* Botón con efecto de escala */
.btn-scale:active { transform: scale(0.98); }

/* Card con elevación en hover */
.card-lift:hover { transform: translateY(-2px); }
```

---

## 🔧 Utilidades de Tailwind Más Usadas

### Layout
```css
/* Flexbox */
flex items-center justify-between
flex-col space-y-4
flex-wrap gap-4

/* Grid */
grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3
gap-6

/* Posicionamiento */
relative absolute inset-0
sticky top-0
```

### Espaciado
```css
/* Padding y margin comunes */
p-4 px-6 py-4
m-4 mx-auto my-8
space-x-4 space-y-6
```

### Colores más usados
```css
/* Fondos */
bg-white bg-gray-50 bg-gray-900
bg-blue-600 bg-green-100 bg-red-100

/* Texto */
text-gray-900 text-gray-600 text-gray-400
text-blue-600 text-green-600 text-red-600

/* Bordes */
border border-gray-200 border-gray-300
border-blue-500 border-green-500
```

---

## 📋 Checklist de Diseño

### ✅ Consistencia Visual
- [ ] Paleta de colores aplicada consistentemente
- [ ] Tipografía jerárquica clara
- [ ] Espaciado uniforme entre elementos
- [ ] Bordes redondeados consistentes

### ✅ Usabilidad
- [ ] Contraste adecuado (WCAG AA)
- [ ] Estados de hover/focus visibles
- [ ] Feedback visual para acciones
- [ ] Loading states implementados

### ✅ Responsive
- [ ] Funciona en mobile (320px+)
- [ ] Adaptación en tablet
- [ ] Optimizado para desktop
- [ ] Sidebar responsive

### ✅ Accesibilidad
- [ ] Navegación por teclado
- [ ] Textos alternativos en imágenes
- [ ] Roles ARIA apropiados
- [ ] Contraste de colores adecuado

---

*Esta guía se enfoca únicamente en los aspectos visuales y de diseño del dashboard. Para implementación técnica, consultar la documentación de desarrollo.*