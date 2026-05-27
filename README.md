# 🖼️ Image Data Quality (IDQ) Assessment

Este proyecto es una herramienta de evaluación de calidad de datos para conjuntos de imágenes (Image Data Quality Assessment). Permite analizar colecciones de imágenes para identificar problemas comunes de calidad como desenfoque (blur), sobreexposición, subexposición, bajo contraste, dimensiones incorrectas, baja entropía (falta de información) y formatos inesperados de canales de color.

El sistema consta de scripts para la extracción de métricas cuantitativas, un generador de reportes en consola, y un dashboard interactivo web construido con **Streamlit** y **Plotly** que permite afinar umbrales y visualizar la distribución de la calidad de los datos en tiempo real.

---

## 📂 Estructura del Proyecto

*   **`datasets/archive/`**: Directorio donde se deben organizar las imágenes. Se espera que las imágenes estén agrupadas en carpetas que representen sus respectivas clases o categorías (ej. `datasets/archive/clase_a/imagen1.jpg`).
*   **`extract_metrics.py`**: Procesa de forma recursiva todas las imágenes dentro de `datasets/archive/`, extrae sus métricas de calidad y las guarda en un archivo CSV.
*   **`analyze_quality.py`**: Carga las métricas del archivo CSV y genera un reporte resumido por consola aplicando umbrales predefinidos de calidad.
*   **`dashboard.py`**: Interfaz interactiva web en Streamlit que permite ajustar los umbrales dinámicamente, visualizar gráficos de distribución y descargar reportes personalizados.
*   **`requirements.txt`**: Listado de librerías y dependencias necesarias para ejecutar el proyecto.
*   **`image_quality_metrics.csv`**: Archivo generado automáticamente por el script de extracción que contiene las métricas cuantitativas de cada imagen.

---

## 📊 Métricas de Calidad Extraídas

Para cada imagen procesada, el sistema calcula:

1.  **Nitidez (Blur Score)**: Calculada mediante la varianza del Operador Laplaciano de la imagen en escala de grises. Valores bajos indican imágenes borrosas.
2.  **Brillo (Brightness Mean)**: El valor promedio de los píxeles (de 0 a 255). Ayuda a detectar imágenes subexpuestas (oscuras) o sobreexpuestas (brillantes).
3.  **Contraste (Contrast Std)**: La desviación estándar de los valores de píxeles. Valores bajos indican imágenes planas o con poco rango dinámico.
4.  **Entropía de Shannon (Entropy)**: Mide la cantidad de información o textura en la imagen. Un valor muy bajo suele indicar una imagen uniforme o vacía.
5.  **Dimensiones y Relación de Aspecto**: Alto, ancho, número de canales (ej. RGB vs. escala de grises) y relación de aspecto (aspect ratio) para identificar imágenes que no sean cuadradas o tengan proporciones erróneas.
6.  **Medias de Color**: Promedio de intensidad para los canales Rojo (R), Verde (G) y Azul (B).

---

## 🚀 Requisitos e Instalación

### Prerrequisitos

*   Python 3.8 o superior.
*   Se recomienda el uso de un entorno virtual (venv o conda).

### Paso 1: Clonar o descargar el repositorio
Ubícate en la carpeta raíz del proyecto:
```bash
cd a:/projects/unicauca/maestria/POC/experiments_multimodal_issues/IDQ
```

### Paso 2: Crear y activar un entorno virtual

**En Windows (PowerShell):**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**En Linux / macOS:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### Paso 3: Instalar dependencias
Instala todas las librerías necesarias ejecutando:
```bash
pip install -r requirements.txt
```

---

## 💻 Instrucciones de Uso

### 1. Preparar las imágenes
Coloca tus imágenes en la carpeta `datasets/archive/`. Asegúrate de que estén organizadas en subcarpetas según su clase:
```text
datasets/
└── archive/
    ├── clase_perro/
    │   ├── perro1.jpg
    │   └── perro2.png
    └── clase_gato/
        ├── gato1.jpg
        └── gato2.bmp
```

> 💡 *Nota: La carpeta `datasets/` está configurada en el `.gitignore` por defecto para evitar subir volúmenes grandes de imágenes al repositorio.*

### 2. Extracción de Métricas
Ejecuta el script para escanear las imágenes y generar el archivo `image_quality_metrics.csv`:
```bash
python extract_metrics.py
```
Al finalizar, verás un resumen estadístico de las imágenes procesadas en la terminal.

### 3. Reporte de Calidad en Consola
Para obtener un análisis rápido de problemas potenciales basado en umbrales por defecto, corre:
```bash
python analyze_quality.py
```
Este script imprimirá un reporte indicando cuántas imágenes presentan problemas de desenfoque, brillo, bajo contraste, baja entropía, etc.

### 4. Ejecutar el Dashboard Interactivo (Recomendado)
Para lanzar la interfaz gráfica web e interactuar con los datos y ajustar los umbrales de manera visual:
```bash
streamlit run dashboard.py
```
Una vez ejecutado, Streamlit abrirá automáticamente tu navegador web (usualmente en `http://localhost:8501`).

---

## 🎨 Dashboard Web Interactiva

El dashboard de calidad incluye las siguientes funcionalidades:
*   **Ajuste Dinámico de Umbrales**: Deslizadores en la barra lateral para definir límites de desenfoque, brillo (mínimo/máximo), contraste y entropía.
*   **Métricas Resumen**: Tarjetas informativas con el conteo de imágenes que no cumplen con los criterios de calidad establecidos.
*   **Gráficos de Distribución**: Histogramas dinámicos (con Plotly) de cada métrica con una línea roja vertical que marca el umbral seleccionado.
*   **Explorador de Datos**: Una tabla interactiva para filtrar y examinar detalladamente el registro de cada imagen.
*   **Descarga de Reportes**: Botón en la barra lateral para descargar las métricas filtradas en formato CSV.
