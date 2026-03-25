# 📝 Obesity Risk Classification MVP

![Python](https://img.shields.io/badge/python-3.11%20%7C%203.12-blue.svg)
![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?logo=docker&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?logo=Streamlit&logoColor=white)
![XGBoost](https://img.shields.io/badge/XGBoost-black?logo=xgboost&logoColor=white)

Este repositorio contiene un **Producto Mínimo Viable (MVP)** para la clasificación multiclase de niveles de obesidad. El proyecto utiliza un modelo de Machine Learning basado en **XGBoost** para predecir el estado nutricional de una persona en función de sus hábitos físicos y antecedentes personales.

---

## 🚀 Descripción del Proyecto

El objetivo es proporcionar una herramienta interactiva que permita a los profesionales de la salud o usuarios finales estimar el nivel de obesidad (desde peso insuficiente hasta obesidad tipo III). Tras experimentar con diversos algoritmos, el modelo XGBoost fue seleccionado como el definitivo debido a su alta precisión y capacidad de generalización.

### ✨ Características principales:
* **Análisis Exploratorio de Datos (EDA):** Visualizaciones interactivas de las tendencias de salud.
* **Modelo de Predicción:** Implementación optimizada de XGBoost.
* **Interfaz de Usuario:** Aplicación web moderna construida con Streamlit.
* **Contenerización:** Despliegue sencillo y consistente mediante Docker.

---

## 🛠️ Stack Tecnológico

| Categoría | Herramientas |
| :--- | :--- |
| **Lenguaje** | Python 3.11+ |
| **Análisis de Datos** | Pandas, NumPy |
| **Visualización** | Plotly, Matplotlib, Seaborn, Altair |
| **Machine Learning** | Scikit-learn, XGBoost, Joblib |
| **Interfaz** | Streamlit & Streamlit-lottie |
| **Gestión/Entorno** | Docker, Jupyter Notebooks, UV |

---

## 📦 Instalación y Uso

Puedes ejecutar este proyecto de dos formas: mediante Docker (recomendado) o en un entorno virtual local.

### Opción 1: Usando Docker 🐳

1. **Clonar el repositorio:**
   ```bash
   git clone [https://github.com/Bootcamp-IA-P6/p7_g1_multiclase.git](https://github.com/Bootcamp-IA-P6/p7_g1_multiclase.git)
   cd p7_g1_multiclase


2.  **Construir la imagen:**

    ```bash
    docker build -t obesidad-app .
    ```

3.  **Ejecutar el contenedor:**

    ```bash
    docker run -p 8501:8501 obesidad-app
    ```

    *Accede a la app en: [http://localhost:8501](https://www.google.com/search?q=http://localhost:8501)*

-----

### Opción 2: Instalación Local 💻

1.  **Crear y activar un entorno virtual:**

    ```bash
    python -m venv venv
    # En Windows:
    venv\Scripts\activate
    # En macOS/Linux:
    source venv/bin/activate
    ```

2.  **Instalar dependencias:**
    *(Recomendado usar `uv` para mayor velocidad)*

    ```bash
    uv sync
    ```

3.  **Ejecutar la aplicación:**

    ```bash
    # En Windows:
    uv run streamlit run app.py
    # En macOS/Linux:
    streamlit run app.py
    ```

-----

## 📊 Estructura del Proyecto

```text
├── data/               # Conjuntos de datos (raw y procesados)
├── models/             # Modelos entrenados (.joblib / .json)
├── notebooks/          # Jupyter Notebooks con el EDA y entrenamiento
├── report/             # Reportes Ejecutivos en pdf
├── app.py              # Aplicación principal de Streamlit
├── Dockerfile          # Configuración de Docker
├── requirements.txt    # Dependencias del proyecto
└── README.md           # Documentación
```

-----

## 🤖 Modelado y Resultados

Durante la fase de desarrollo, se evaluaron múltiples arquitecturas para garantizar el mejor desempeño:

  * **Regresión Logística:** Utilizada como *baseline* para comparación inicial.
  * **Random Forest:** Buen desempeño, pero con tendencia al sobreajuste.
  * **XGBoost (Elegido):** Demostró ser el más robusto para manejar la naturaleza multiclase de este problema, logrando métricas superiores en **F1-Score** y **Accuracy**.

> [\!TIP]
> El modelo final está serializado en la carpeta `models/` para su consumo inmediato por la interfaz de Streamlit.

-----

## 👥 Contribuyentes

Este proyecto fue desarrollado por el **Grupo 1 - Bootcamp IA P6**:

| Nombre | Rol |
| :--- | :--- |
| **Gema Yébenes Caballero** | Scrum Master |
| **José Julio Ramírez y Sánchez-Escobar** | Data Steward |
| **Andrés Torrez** | IA Developer |
| **Juan Manuel Iriondo Ortega** | Data Analyst |
| **Mar Izquierdo Vaquer** | Product Owner |

-----

> [\!IMPORTANT]
> Este proyecto fue realizado como parte del entregable **P7** del Bootcamp de Inteligencia Artificial.
