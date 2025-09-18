# 🎨 **Design System - Dashboard de Entrenamiento de Modelos**

## 📋 **Índice**

1. [Identidad Visual](#-identidad-visual)
2. [Paleta de Colores](#-paleta-de-colores)
3. [Sistema Tipográfico](#-sistema-tipográfico)
4. [Espaciado y Grid](#-espaciado-y-grid)
5. [Iconografía](#-iconografía)
6. [Componentes Base](#-componentes-base)
7. [Visualización de Datos](#-visualización-de-datos)
8. [Sistema de Temas](#-sistema-de-temas)
9. [Estados y Feedback](#-estados-y-feedback)
10. [Accesibilidad](#-accesibilidad)
11. [Responsive Design](#-responsive-design)
12. [Implementación Técnica](#-implementación-técnica)

---

## 🎯 **Identidad Visual**

### **Concepto de Diseño**
- **Estilo**: Moderno, limpio, orientado a datos
- **Personalidad**: Profesional, confiable, eficiente
- **Audiencia**: Data Scientists, ML Engineers, Desarrolladores
- **Contexto**: Herramienta de monitoreo y análisis técnico

### **Principios de Diseño**
1. **Claridad**: Información clara y jerarquizada
2. **Eficiencia**: Acceso rápido a datos críticos
3. **Consistencia**: Patrones visuales uniformes
4. **Accesibilidad**: Usable por todos los usuarios
5. **Escalabilidad**: Adaptable a diferentes volúmenes de datos

---

## 🌈 **Paleta de Colores**

### **Colores Primarios**

#### **Azul Principal (Primary)**
```css
--color-primary-50: #eff6ff;
--color-primary-100: #dbeafe;
--color-primary-200: #bfdbfe;
--color-primary-300: #93c5fd;
--color-primary-400: #60a5fa;
--color-primary-500: #3b82f6;  /* Principal */
--color-primary-600: #2563eb;
--color-primary-700: #1d4ed8;
--color-primary-800: #1e40af;
--color-primary-900: #1e3a8a;
```

#### **Gris Neutro (Neutral)**
```css
--color-neutral-50: #f9fafb;
--color-neutral-100: #f3f4f6;
--color-neutral-200: #e5e7eb;
--color-neutral-300: #d1d5db;
--color-neutral-400: #9ca3af;
--color-neutral-500: #6b7280;
--color-neutral-600: #4b5563;
--color-neutral-700: #374151;
--color-neutral-800: #1f2937;
--color-neutral-900: #111827;
```

### **Colores Semánticos**

#### **Éxito (Success)**
```css
--color-success-50: #f0fdf4;
--color-success-100: #dcfce7;
--color-success-200: #bbf7d0;
--color-success-300: #86efac;
--color-success-400: #4ade80;
--color-success-500: #22c55e;  /* Principal */
--color-success-600: #16a34a;
--color-success-700: #15803d;
--color-success-800: #166534;
--color-success-900: #14532d;
```

#### **Advertencia (Warning)**
```css
--color-warning-50: #fffbeb;
--color-warning-100: #fef3c7;
--color-warning-200: #fde68a;
--color-warning-300: #fcd34d;
--color-warning-400: #fbbf24;
--color-warning-500: #f59e0b;  /* Principal */
--color-warning-600: #d97706;
--color-warning-700: #b45309;
--color-warning-800: #92400e;
--color-warning-900: #78350f;
```

#### **Error (Error)**
```css
--color-error-50: #fef2f2;
--color-error-100: #fee2e2;
--color-error-200: #fecaca;
--color-error-300: #fca5a5;
--color-error-400: #f87171;
--color-error-500: #ef4444;  /* Principal */
--color-error-600: #dc2626;
--color-error-700: #b91c1c;
--color-error-800: #991b1b;
--color-error-900: #7f1d1d;
```

#### **Información (Info)**
```css
--color-info-50: #f0f9ff;
--color-info-100: #e0f2fe;
--color-info-200: #bae6fd;
--color-info-300: #7dd3fc;
--color-info-400: #38bdf8;
--color-info-500: #0ea5e9;  /* Principal */
--color-info-600: #0284c7;
--color-info-700: #0369a1;
--color-info-800: #075985;
--color-info-900: #0c4a6e;
```

### **Colores para Gráficos**

#### **Paleta de Métricas**
```css
--chart-loss: #ef4444;        /* Rojo para loss */
--chart-accuracy: #22c55e;    /* Verde para accuracy */
--chart-validation: #3b82f6;  /* Azul para validación */
--chart-learning-rate: #f59e0b; /* Naranja para learning rate */
--chart-gradient: #8b5cf6;    /* Púrpura para gradientes */
--chart-memory: #06b6d4;      /* Cian para memoria */
--chart-cpu: #84cc16;         /* Lima para CPU */
--chart-gpu: #f97316;         /* Naranja para GPU */
```

#### **Paleta Categórica (8 colores)**
```css
--chart-cat-1: #3b82f6;  /* Azul */
--chart-cat-2: #ef4444;  /* Rojo */
--chart-cat-3: #22c55e;  /* Verde */
--chart-cat-4: #f59e0b;  /* Naranja */
--chart-cat-5: #8b5cf6;  /* Púrpura */
--chart-cat-6: #06b6d4;  /* Cian */
--chart-cat-7: #84cc16;  /* Lima */
--chart-cat-8: #f97316;  /* Naranja oscuro */
```

---

## 📝 **Sistema Tipográfico**

### **Familias Tipográficas**

#### **Fuente Principal**
```css
--font-family-sans: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
```

#### **Fuente Monoespaciada**
```css
--font-family-mono: 'JetBrains Mono', 'Fira Code', Consolas, 'Liberation Mono', Menlo, monospace;
```

### **Escala Tipográfica**

#### **Tamaños de Fuente**
```css
--text-xs: 0.75rem;    /* 12px */
--text-sm: 0.875rem;   /* 14px */
--text-base: 1rem;     /* 16px */
--text-lg: 1.125rem;   /* 18px */
--text-xl: 1.25rem;    /* 20px */
--text-2xl: 1.5rem;    /* 24px */
--text-3xl: 1.875rem;  /* 30px */
--text-4xl: 2.25rem;   /* 36px */
--text-5xl: 3rem;      /* 48px */
```

#### **Pesos de Fuente**
```css
--font-thin: 100;
--font-light: 300;
--font-normal: 400;
--font-medium: 500;
--font-semibold: 600;
--font-bold: 700;
--font-extrabold: 800;
```

#### **Alturas de Línea**
```css
--leading-none: 1;
--leading-tight: 1.25;
--leading-snug: 1.375;
--leading-normal: 1.5;
--leading-relaxed: 1.625;
--leading-loose: 2;
```

### **Jerarquía Tipográfica**

#### **Encabezados**
```css
.heading-1 {
  font-size: var(--text-4xl);
  font-weight: var(--font-bold);
  line-height: var(--leading-tight);
  letter-spacing: -0.025em;
}

.heading-2 {
  font-size: var(--text-3xl);
  font-weight: var(--font-semibold);
  line-height: var(--leading-tight);
  letter-spacing: -0.025em;
}

.heading-3 {
  font-size: var(--text-2xl);
  font-weight: var(--font-semibold);
  line-height: var(--leading-snug);
}

.heading-4 {
  font-size: var(--text-xl);
  font-weight: var(--font-medium);
  line-height: var(--leading-snug);
}
```

#### **Texto de Cuerpo**
```css
.body-large {
  font-size: var(--text-lg);
  font-weight: var(--font-normal);
  line-height: var(--leading-relaxed);
}

.body-base {
  font-size: var(--text-base);
  font-weight: var(--font-normal);
  line-height: var(--leading-normal);
}

.body-small {
  font-size: var(--text-sm);
  font-weight: var(--font-normal);
  line-height: var(--leading-normal);
}
```

#### **Texto Especializado**
```css
.caption {
  font-size: var(--text-xs);
  font-weight: var(--font-medium);
  line-height: var(--leading-normal);
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.code {
  font-family: var(--font-family-mono);
  font-size: var(--text-sm);
  font-weight: var(--font-normal);
}

.label {
  font-size: var(--text-sm);
  font-weight: var(--font-medium);
  line-height: var(--leading-normal);
}
```

---

## 📐 **Espaciado y Grid**

### **Sistema de Espaciado (8px base)**

```css
--space-0: 0;
--space-1: 0.25rem;  /* 4px */
--space-2: 0.5rem;   /* 8px */
--space-3: 0.75rem;  /* 12px */
--space-4: 1rem;     /* 16px */
--space-5: 1.25rem;  /* 20px */
--space-6: 1.5rem;   /* 24px */
--space-8: 2rem;     /* 32px */
--space-10: 2.5rem;  /* 40px */
--space-12: 3rem;    /* 48px */
--space-16: 4rem;    /* 64px */
--space-20: 5rem;    /* 80px */
--space-24: 6rem;    /* 96px */
--space-32: 8rem;    /* 128px */
```

### **Grid System**

#### **Contenedores**
```css
.container {
  width: 100%;
  margin-left: auto;
  margin-right: auto;
  padding-left: var(--space-4);
  padding-right: var(--space-4);
}

.container-sm { max-width: 640px; }
.container-md { max-width: 768px; }
.container-lg { max-width: 1024px; }
.container-xl { max-width: 1280px; }
.container-2xl { max-width: 1536px; }
```

#### **Grid Layout**
```css
.grid {
  display: grid;
  gap: var(--space-6);
}

.grid-cols-1 { grid-template-columns: repeat(1, minmax(0, 1fr)); }
.grid-cols-2 { grid-template-columns: repeat(2, minmax(0, 1fr)); }
.grid-cols-3 { grid-template-columns: repeat(3, minmax(0, 1fr)); }
.grid-cols-4 { grid-template-columns: repeat(4, minmax(0, 1fr)); }
.grid-cols-12 { grid-template-columns: repeat(12, minmax(0, 1fr)); }
```

### **Breakpoints Responsivos**

```css
/* Mobile First */
@media (min-width: 640px) { /* sm */ }
@media (min-width: 768px) { /* md */ }
@media (min-width: 1024px) { /* lg */ }
@media (min-width: 1280px) { /* xl */ }
@media (min-width: 1536px) { /* 2xl */ }
```

---

## 🎭 **Iconografía**

### **Librería de Iconos**
- **Principal**: Heroicons (outline y solid)
- **Complementaria**: Lucide React
- **Técnicos**: Tabler Icons

### **Tamaños de Iconos**
```css
--icon-xs: 1rem;    /* 16px */
--icon-sm: 1.25rem; /* 20px */
--icon-md: 1.5rem;  /* 24px */
--icon-lg: 2rem;    /* 32px */
--icon-xl: 2.5rem;  /* 40px */
```

### **Iconos por Contexto**

#### **Estados de Entrenamiento**
- **Corriendo**: ▶️ Play Circle
- **Pausado**: ⏸️ Pause Circle
- **Completado**: ✅ Check Circle
- **Error**: ❌ X Circle
- **Detenido**: ⏹️ Stop Circle

#### **Métricas y Datos**
- **Gráfico**: 📊 Chart Bar
- **Tendencia Up**: 📈 Trending Up
- **Tendencia Down**: 📉 Trending Down
- **CPU**: 🖥️ CPU Chip
- **Memoria**: 💾 Memory
- **GPU**: 🎮 Device GPU

#### **Acciones**
- **Configurar**: ⚙️ Cog
- **Exportar**: 📤 Download
- **Filtrar**: 🔍 Filter
- **Actualizar**: 🔄 Refresh
- **Eliminar**: 🗑️ Trash

---

## 🧩 **Componentes Base**

### **Botones**

#### **Variantes**
```css
/* Primary Button */
.btn-primary {
  background-color: var(--color-primary-500);
  color: white;
  border: 1px solid var(--color-primary-500);
  padding: var(--space-2) var(--space-4);
  border-radius: 0.375rem;
  font-weight: var(--font-medium);
  transition: all 0.2s ease;
}

.btn-primary:hover {
  background-color: var(--color-primary-600);
  border-color: var(--color-primary-600);
}

/* Secondary Button */
.btn-secondary {
  background-color: transparent;
  color: var(--color-primary-500);
  border: 1px solid var(--color-primary-500);
  padding: var(--space-2) var(--space-4);
  border-radius: 0.375rem;
  font-weight: var(--font-medium);
  transition: all 0.2s ease;
}

.btn-secondary:hover {
  background-color: var(--color-primary-50);
}

/* Ghost Button */
.btn-ghost {
  background-color: transparent;
  color: var(--color-neutral-600);
  border: none;
  padding: var(--space-2) var(--space-4);
  border-radius: 0.375rem;
  font-weight: var(--font-medium);
  transition: all 0.2s ease;
}

.btn-ghost:hover {
  background-color: var(--color-neutral-100);
  color: var(--color-neutral-900);
}
```

#### **Tamaños**
```css
.btn-sm {
  padding: var(--space-1) var(--space-3);
  font-size: var(--text-sm);
}

.btn-md {
  padding: var(--space-2) var(--space-4);
  font-size: var(--text-base);
}

.btn-lg {
  padding: var(--space-3) var(--space-6);
  font-size: var(--text-lg);
}
```

### **Cards**

#### **Card Base**
```css
.card {
  background-color: white;
  border-radius: 0.5rem;
  box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06);
  border: 1px solid var(--color-neutral-200);
  overflow: hidden;
}

.card-header {
  padding: var(--space-6);
  border-bottom: 1px solid var(--color-neutral-200);
}

.card-body {
  padding: var(--space-6);
}

.card-footer {
  padding: var(--space-6);
  border-top: 1px solid var(--color-neutral-200);
  background-color: var(--color-neutral-50);
}
```

#### **Card de Métricas**
```css
.metric-card {
  background: linear-gradient(135deg, var(--color-primary-500), var(--color-primary-600));
  color: white;
  border-radius: 0.75rem;
  padding: var(--space-6);
  position: relative;
  overflow: hidden;
}

.metric-card::before {
  content: '';
  position: absolute;
  top: 0;
  right: 0;
  width: 100px;
  height: 100px;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 50%;
  transform: translate(30px, -30px);
}
```

### **Formularios**

#### **Inputs**
```css
.input {
  width: 100%;
  padding: var(--space-3) var(--space-4);
  border: 1px solid var(--color-neutral-300);
  border-radius: 0.375rem;
  font-size: var(--text-base);
  transition: all 0.2s ease;
  background-color: white;
}

.input:focus {
  outline: none;
  border-color: var(--color-primary-500);
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

.input:disabled {
  background-color: var(--color-neutral-100);
  color: var(--color-neutral-500);
  cursor: not-allowed;
}
```

#### **Labels**
```css
.label {
  display: block;
  font-size: var(--text-sm);
  font-weight: var(--font-medium);
  color: var(--color-neutral-700);
  margin-bottom: var(--space-2);
}

.label-required::after {
  content: '*';
  color: var(--color-error-500);
  margin-left: var(--space-1);
}
```

---

## 📊 **Visualización de Datos**

### **Estilos de Gráficos**

#### **Configuración Base Chart.js**
```javascript
const chartDefaults = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      position: 'bottom',
      labels: {
        usePointStyle: true,
        padding: 20,
        font: {
          family: 'Inter',
          size: 12,
          weight: '500'
        }
      }
    },
    tooltip: {
      backgroundColor: 'rgba(17, 24, 39, 0.95)',
      titleColor: '#f9fafb',
      bodyColor: '#f9fafb',
      borderColor: '#374151',
      borderWidth: 1,
      cornerRadius: 8,
      padding: 12,
      titleFont: {
        family: 'Inter',
        size: 14,
        weight: '600'
      },
      bodyFont: {
        family: 'Inter',
        size: 13,
        weight: '400'
      }
    }
  },
  scales: {
    x: {
      grid: {
        color: '#f3f4f6',
        borderColor: '#e5e7eb'
      },
      ticks: {
        font: {
          family: 'Inter',
          size: 11
        },
        color: '#6b7280'
      }
    },
    y: {
      grid: {
        color: '#f3f4f6',
        borderColor: '#e5e7eb'
      },
      ticks: {
        font: {
          family: 'Inter',
          size: 11
        },
        color: '#6b7280'
      }
    }
  }
};
```

#### **Estilos de Líneas**
```css
.chart-line-loss {
  border-color: var(--chart-loss);
  background-color: rgba(239, 68, 68, 0.1);
  border-width: 2px;
}

.chart-line-accuracy {
  border-color: var(--chart-accuracy);
  background-color: rgba(34, 197, 94, 0.1);
  border-width: 2px;
}

.chart-line-validation {
  border-color: var(--chart-validation);
  background-color: rgba(59, 130, 246, 0.1);
  border-width: 2px;
  border-dash: [5, 5];
}
```

### **Estados de Datos**

#### **Loading State**
```css
.chart-loading {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 300px;
  background-color: var(--color-neutral-50);
  border-radius: 0.5rem;
  border: 2px dashed var(--color-neutral-300);
}

.loading-spinner {
  width: 2rem;
  height: 2rem;
  border: 2px solid var(--color-neutral-300);
  border-top: 2px solid var(--color-primary-500);
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}
```

#### **Empty State**
```css
.chart-empty {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 300px;
  color: var(--color-neutral-500);
  text-align: center;
}

.empty-icon {
  width: 3rem;
  height: 3rem;
  margin-bottom: var(--space-4);
  opacity: 0.5;
}
```

#### **Error State**
```css
.chart-error {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 300px;
  background-color: var(--color-error-50);
  border: 1px solid var(--color-error-200);
  border-radius: 0.5rem;
  color: var(--color-error-700);
  text-align: center;
}
```

---

## 🌙 **Sistema de Temas**

### **Tema Dark (Default)**

#### **Colores de Fondo**
```css
:root {
  --bg-primary: #ffffff;
  --bg-secondary: #f9fafb;
  --bg-tertiary: #f3f4f6;
  --bg-accent: #eff6ff;
}
```

#### **Colores de Texto**
```css
:root {
  --text-primary: #111827;
  --text-secondary: #374151;
  --text-tertiary: #6b7280;
  --text-accent: #3b82f6;
}
```

### **Tema Oscuro**

#### **Colores de Fondo**
```css
[data-theme="dark"] {
  --bg-primary: #111827;
  --bg-secondary: #1f2937;
  --bg-tertiary: #374151;
  --bg-accent: #1e3a8a;
}
```

#### **Colores de Texto**
```css
[data-theme="dark"] {
  --text-primary: #f9fafb;
  --text-secondary: #e5e7eb;
  --text-tertiary: #9ca3af;
  --text-accent: #60a5fa;
}
```

#### **Adaptaciones de Componentes**
```css
[data-theme="dark"] .card {
  background-color: var(--bg-secondary);
  border-color: var(--color-neutral-700);
}

[data-theme="dark"] .input {
  background-color: var(--bg-tertiary);
  border-color: var(--color-neutral-600);
  color: var(--text-primary);
}

[data-theme="dark"] .input:focus {
  border-color: var(--color-primary-400);
  box-shadow: 0 0 0 3px rgba(96, 165, 250, 0.1);
}
```

### **Tema Alto Contraste**

```css
[data-theme="high-contrast"] {
  --bg-primary: #ffffff;
  --bg-secondary: #000000;
  --text-primary: #000000;
  --text-secondary: #000000;
  --color-primary-500: #0000ff;
  --color-success-500: #008000;
  --color-error-500: #ff0000;
  --color-warning-500: #ff8c00;
}

[data-theme="high-contrast"] .card {
  border: 2px solid #000000;
}

[data-theme="high-contrast"] .btn-primary {
  border: 2px solid #000000;
}
```

---

## ⚡ **Estados y Feedback**

### **Estados de Interacción**

#### **Hover States**
```css
.interactive:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  transition: all 0.2s ease;
}
```

#### **Focus States**
```css
.focusable:focus {
  outline: none;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
  border-color: var(--color-primary-500);
}
```

#### **Active States**
```css
.clickable:active {
  transform: translateY(0);
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}
```

### **Estados de Carga**

#### **Skeleton Loading**
```css
.skeleton {
  background: linear-gradient(90deg, #f0f0f0 25%, #e0e0e0 50%, #f0f0f0 75%);
  background-size: 200% 100%;
  animation: loading 1.5s infinite;
}

@keyframes loading {
  0% { background-position: 200% 0; }
  100% { background-position: -200% 0; }
}
```

#### **Progress Indicators**
```css
.progress-bar {
  width: 100%;
  height: 0.5rem;
  background-color: var(--color-neutral-200);
  border-radius: 0.25rem;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  background: linear-gradient(90deg, var(--color-primary-500), var(--color-primary-400));
  border-radius: 0.25rem;
  transition: width 0.3s ease;
}
```

### **Notificaciones y Alertas**

#### **Toast Notifications**
```css
.toast {
  position: fixed;
  top: var(--space-4);
  right: var(--space-4);
  background-color: white;
  border-radius: 0.5rem;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
  border-left: 4px solid var(--color-primary-500);
  padding: var(--space-4);
  max-width: 400px;
  z-index: 1000;
  animation: slideIn 0.3s ease;
}

@keyframes slideIn {
  from {
    transform: translateX(100%);
    opacity: 0;
  }
  to {
    transform: translateX(0);
    opacity: 1;
  }
}
```

#### **Alert Banners**
```css
.alert {
  padding: var(--space-4);
  border-radius: 0.5rem;
  border: 1px solid;
  margin-bottom: var(--space-4);
}

.alert-success {
  background-color: var(--color-success-50);
  border-color: var(--color-success-200);
  color: var(--color-success-800);
}

.alert-warning {
  background-color: var(--color-warning-50);
  border-color: var(--color-warning-200);
  color: var(--color-warning-800);
}

.alert-error {
  background-color: var(--color-error-50);
  border-color: var(--color-error-200);
  color: var(--color-error-800);
}
```

---

## ♿ **Accesibilidad**

### **Contraste de Colores**

#### **Ratios Mínimos (WCAG AA)**
- **Texto normal**: 4.5:1
- **Texto grande**: 3:1
- **Elementos gráficos**: 3:1
- **Elementos de UI**: 3:1

#### **Verificación de Contraste**
```css
/* Texto sobre fondo claro */
.text-on-light {
  color: var(--color-neutral-900); /* Ratio: 16.75:1 ✅ */
}

/* Texto sobre fondo oscuro */
.text-on-dark {
  color: var(--color-neutral-50); /* Ratio: 16.75:1 ✅ */
}

/* Enlaces */
.link {
  color: var(--color-primary-600); /* Ratio: 5.9:1 ✅ */
}
```

### **Navegación por Teclado**

#### **Focus Management**
```css
.skip-link {
  position: absolute;
  top: -40px;
  left: 6px;
  background: var(--color-primary-600);
  color: white;
  padding: 8px;
  text-decoration: none;
  border-radius: 4px;
  z-index: 1000;
}

.skip-link:focus {
  top: 6px;
}
```

#### **Tab Order**
```css
.tab-trap {
  outline: 2px solid var(--color-primary-500);
  outline-offset: 2px;
}
```

### **Screen Readers**

#### **ARIA Labels**
```html
<!-- Ejemplos de implementación -->
<button aria-label="Iniciar entrenamiento del modelo">
  <PlayIcon />
</button>

<div role="status" aria-live="polite">
  Entrenamiento completado: 95% de precisión
</div>

<table role="table" aria-label="Historial de entrenamientos">
  <caption>Últimos 10 entrenamientos realizados</caption>
</table>
```

### **Reduced Motion**

```css
@media (prefers-reduced-motion: reduce) {
  *,
  *::before,
  *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
}
```

---

## 📱 **Responsive Design**

### **Estrategia Mobile-First**

#### **Breakpoints**
```css
/* Base: Mobile (320px+) */
.dashboard-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: var(--space-4);
}

/* Tablet (768px+) */
@media (min-width: 768px) {
  .dashboard-grid {
    grid-template-columns: repeat(2, 1fr);
    gap: var(--space-6);
  }
}

/* Desktop (1024px+) */
@media (min-width: 1024px) {
  .dashboard-grid {
    grid-template-columns: repeat(3, 1fr);
    gap: var(--space-8);
  }
}

/* Large Desktop (1280px+) */
@media (min-width: 1280px) {
  .dashboard-grid {
    grid-template-columns: repeat(4, 1fr);
  }
}
```

### **Componentes Adaptativos**

#### **Navigation**
```css
/* Mobile: Bottom Navigation */
@media (max-width: 767px) {
  .navigation {
    position: fixed;
    bottom: 0;
    left: 0;
    right: 0;
    display: flex;
    justify-content: space-around;
    background: white;
    border-top: 1px solid var(--color-neutral-200);
    padding: var(--space-2);
  }
}

/* Desktop: Sidebar */
@media (min-width: 768px) {
  .navigation {
    position: fixed;
    left: 0;
    top: 0;
    bottom: 0;
    width: 256px;
    background: white;
    border-right: 1px solid var(--color-neutral-200);
    padding: var(--space-6);
  }
}
```

#### **Charts Responsivos**
```css
.chart-container {
  position: relative;
  height: 200px;
  width: 100%;
}

@media (min-width: 768px) {
  .chart-container {
    height: 300px;
  }
}

@media (min-width: 1024px) {
  .chart-container {
    height: 400px;
  }
}
```

### **Touch Targets**

```css
.touch-target {
  min-height: 44px;
  min-width: 44px;
  padding: var(--space-3);
}

@media (pointer: coarse) {
  .touch-target {
    min-height: 48px;
    min-width: 48px;
  }
}
```

---

## 🔧 **Implementación Técnica**

### **CSS Custom Properties**

#### **Estructura de Variables**
```css
:root {
  /* Colores */
  --color-primary-50: #eff6ff;
  /* ... resto de colores ... */
  
  /* Tipografía */
  --font-family-sans: 'Inter', sans-serif;
  --text-xs: 0.75rem;
  /* ... resto de tipografía ... */
  
  /* Espaciado */
  --space-1: 0.25rem;
  /* ... resto de espaciado ... */
  
  /* Sombras */
  --shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
  --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
  --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
  
  /* Transiciones */
  --transition-fast: 0.15s ease;
  --transition-base: 0.2s ease;
  --transition-slow: 0.3s ease;
  
  /* Z-index */
  --z-dropdown: 1000;
  --z-modal: 1050;
  --z-tooltip: 1100;
}
```

### **Tailwind CSS Configuration**

```javascript
// tailwind.config.js
module.exports = {
  content: ['./src/**/*.{js,ts,jsx,tsx}'],
  theme: {
    extend: {
      colors: {
        primary: {
          50: '#eff6ff',
          500: '#3b82f6',
          900: '#1e3a8a',
        },
        // ... resto de colores
      },
      fontFamily: {
        sans: ['Inter', 'sans-serif'],
        mono: ['JetBrains Mono', 'monospace'],
      },
      spacing: {
        '18': '4.5rem',
        '88': '22rem',
      },
      animation: {
        'fade-in': 'fadeIn 0.3s ease-in-out',
        'slide-up': 'slideUp 0.3s ease-out',
      },
    },
  },
  plugins: [
    require('@tailwindcss/forms'),
    require('@tailwindcss/typography'),
  ],
}
```

### **Componentes con Styled Components**

```typescript
// components/ui/Button.tsx
import styled, { css } from 'styled-components';

interface ButtonProps {
  variant?: 'primary' | 'secondary' | 'ghost';
  size?: 'sm' | 'md' | 'lg';
  disabled?: boolean;
}

const Button = styled.button<ButtonProps>`
  font-family: var(--font-family-sans);
  font-weight: var(--font-medium);
  border-radius: 0.375rem;
  transition: var(--transition-base);
  cursor: pointer;
  
  ${props => props.variant === 'primary' && css`
    background-color: var(--color-primary-500);
    color: white;
    border: 1px solid var(--color-primary-500);
    
    &:hover:not(:disabled) {
      background-color: var(--color-primary-600);
    }
  `}
  
  ${props => props.size === 'sm' && css`
    padding: var(--space-1) var(--space-3);
    font-size: var(--text-sm);
  `}
  
  ${props => props.disabled && css`
    opacity: 0.5;
    cursor: not-allowed;
  `}
`;
```

### **Theme Provider**

```typescript
// contexts/ThemeContext.tsx
import React, { createContext, useContext, useState, useEffect } from 'react';

type Theme = 'light' | 'dark' | 'high-contrast';

interface ThemeContextType {
  theme: Theme;
  setTheme: (theme: Theme) => void;
  toggleTheme: () => void;
}

const ThemeContext = createContext<ThemeContextType | undefined>(undefined);

export const ThemeProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [theme, setTheme] = useState<Theme>('light');

  useEffect(() => {
    const savedTheme = localStorage.getItem('theme') as Theme;
    if (savedTheme) {
      setTheme(savedTheme);
    } else {
      const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
      setTheme(prefersDark ? 'dark' : 'light');
    }
  }, []);

  useEffect(() => {
    document.documentElement.setAttribute('data-theme', theme);
    localStorage.setItem('theme', theme);
  }, [theme]);

  const toggleTheme = () => {
    setTheme(prev => prev === 'light' ? 'dark' : 'light');
  };

  return (
    <ThemeContext.Provider value={{ theme, setTheme, toggleTheme }}>
      {children}
    </ThemeContext.Provider>
  );
};

export const useTheme = () => {
  const context = useContext(ThemeContext);
  if (!context) {
    throw new Error('useTheme must be used within ThemeProvider');
  }
  return context;
};
```

---

## 📋 **Checklist de Implementación**

### **✅ Fundación**
- [ ] Configurar variables CSS custom properties
- [ ] Implementar sistema de colores
- [ ] Configurar tipografía (Inter + JetBrains Mono)
- [ ] Establecer sistema de espaciado
- [ ] Configurar breakpoints responsivos

### **✅ Componentes Base**
- [ ] Botones (primary, secondary, ghost)
- [ ] Cards (base, métricas, estados)
- [ ] Formularios (inputs, labels, validación)
- [ ] Navegación (sidebar, bottom nav)
- [ ] Modales y overlays

### **✅ Visualización**
- [ ] Configurar Chart.js con estilos custom
- [ ] Implementar paleta de colores para gráficos
- [ ] Estados de carga, error y vacío
- [ ] Tooltips y leyendas consistentes
- [ ] Responsive charts

### **✅ Temas**
- [ ] Tema claro (default)
- [ ] Tema oscuro
- [ ] Tema alto contraste
- [ ] Theme provider y context
- [ ] Persistencia de preferencias

### **✅ Accesibilidad**
- [ ] Verificar ratios de contraste
- [ ] Implementar navegación por teclado
- [ ] ARIA labels y roles
- [ ] Support para screen readers
- [ ] Reduced motion support

### **✅ Testing**
- [ ] Visual regression tests
- [ ] Accessibility tests
- [ ] Cross-browser compatibility
- [ ] Performance de componentes
- [ ] Responsive testing

---

## 🎯 **Métricas de Éxito**

### **Performance**
- **First Contentful Paint**: < 1.5s
- **Largest Contentful Paint**: < 2.5s
- **Cumulative Layout Shift**: < 0.1
- **Bundle size CSS**: < 50KB gzipped

### **Accesibilidad**
- **WCAG AA Compliance**: 100%
- **Lighthouse Accessibility Score**: > 95
- **Keyboard Navigation**: 100% funcional
- **Screen Reader Compatibility**: Completa

### **Usabilidad**
- **Consistency Score**: > 90%
- **Component Reusability**: > 80%
- **Design Token Coverage**: > 95%
- **Cross-browser Compatibility**: 100%

---

## 📚 **Recursos y Referencias**

### **Herramientas de Diseño**
- **Figma**: Prototipado y design system
- **Storybook**: Documentación de componentes
- **Chromatic**: Visual testing
- **Accessibility Insights**: Testing de accesibilidad

### **Librerías y Frameworks**
- **Tailwind CSS**: Framework de utilidades
- **Headless UI**: Componentes accesibles
- **Framer Motion**: Animaciones
- **React Hook Form**: Formularios

### **Testing y Validación**
- **axe-core**: Accessibility testing
- **Lighthouse**: Performance audits
- **Playwright**: E2E testing
- **Chromatic**: Visual regression

### **Documentación**
- **WCAG 2.1**: Guías de accesibilidad
- **Material Design**: Principios de diseño
- **Apple HIG**: Human Interface Guidelines
- **Inclusive Design**: Microsoft guidelines

---

*Este design system está diseñado para evolucionar con el proyecto. Se recomienda revisar y actualizar regularmente basándose en feedback de usuarios y métricas de uso.*