import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import joblib
import os

# ==========================================
# 1. CONFIGURACIÓN DE LA PÁGINA Y ESTILOS CSS
# ==========================================
st.set_page_config(page_title="Predicctor de Obesidad", page_icon="🩺", layout="wide")

# --- CSS PERSONALIZADO ---
st.markdown("""
    <style>
    /* Fondo crema/grisáceo muy elegante */
    .stApp {
        background-color: #F7F5F0;
    }
    
    /* Estilo llamativo para los selectores e inputs (Efecto botón 3D) */
    div[data-baseweb="select"] > div, div[data-baseweb="input"] > div {
        border-radius: 12px !important;
        border: 2px solid #bdc3c7 !important;
        background-color: #f8f8f8 !important;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1) !important;
        transition: all 0.3s ease;
    }
    
    /* Efecto al pasar el ratón por encima de los inputs */
    div[data-baseweb="select"] > div:hover, div[data-baseweb="input"] > div:hover {
        border-color: #3498db !important;
        box-shadow: 0 6px 12px rgba(0,0,0,0.15) !important;
    }
    
    /* Darle color a los títulos */
    h1, h2, h3 {
        color: #2c3e50;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🩺 Sistema de Predicción de Riesgo de Obesidad")
st.markdown("""
Esta herramienta utiliza un modelo de **Machine Learning (XGBoost)** entrenado para evaluar el riesgo de obesidad de un paciente en base a su biometría, genética y estilo de vida.
""")

# ==========================================
# 2. CARGA DEL MODELO Y ENCODER (Con Caché)
# ==========================================
@st.cache_resource
def load_models():
    try:
        pipeline = joblib.load('models/pipeline_obesity_XGBoost_Optimizado_m.pkl')
        le = joblib.load('models/label_encoder_m.pkl')
        return pipeline, le
    except FileNotFoundError:
        st.error("⚠️ Archivos del modelo no encontrados. Asegúrate de haber ejecutado el notebook de modelado.")
        return None, None

pipeline, le = load_models()

# ==========
# 3. MAPEOS
# ==========
# El modelo espera textos en inglés ('yes', 'no', 'Female', etc.). 
# Mapeamos los inputs en español a los valores exactos que el modelo aprendió.
yes_no = {"No": "no", 'Ocasionalmente': 'Sometimes',"Si": "yes"}
consumo_map = {'Nunca': 'no', 'Ocasionalmente': 'Sometimes', 'Frecuentemente': 'Frequently', 'Siempre': 'Always'}
gender_map = {"Femenino": "Female", "Masculino": "Male"}
smoke_map = {"No": "no", "Ocasionalmente": "Sometimes", "Si": "yes"} # El modelo original solo tenía yes/no, pero el pipeline lo manejará.
caec_map = {'Nunca': 'no', 'Ocasionalmente': 'Sometimes', 'Frecuentemente': 'Frequently', 'Siempre': 'Always'}
fcvc_map = {'Baja': 1.0, 'Media': 2.0, 'Alta': 3.0}
ncp_map = {'1': 1.0, '2': 2.0, '3': 3.0, '4': 4.0, '5': 5.0, '+': 6.0}
ch2o_map = {'1': 1.0, '1.5': 1.5, '2': 2.0, '2.5': 2.5, '+': 3.0}
faf_map = {'0': 0.0, '1': 1.0, '2': 2.0, '3': 3.0, '4': 4.0, '5': 5.0, '+': 6.0}
tue_map = {'0-2': 1.0, '3-4': 2.0, '5+': 3.0}
mtrans_map = {'Coche': 'Automobile', 'Moto': 'Motorbike', 'Bicicleta': 'Bike', 'Transporte Público': 'Public_Transportation', 'Caminando': 'Walking'}

# ==========================================
# 4. ENTRADA DE DATOS (INPUTS)
# ==========================================
st.write("### 📝 Datos del Paciente")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("##### 🧬 Biometría y Genética")
    gender = gender_map[st.selectbox("Sexo", ["Femenino", "Masculino"])]
    age = st.number_input("Edad", min_value=14, max_value=80, value=25, step=1)
    height = st.number_input("Altura (metros)", 1.20, 2.20, 1.70)
    weight = st.number_input("Peso (kg)", 30.0, 200.0, 70.0)
    family_history = yes_no[st.selectbox("Historial Familiar de Sobrepeso", ["No", "Si"])]

with col2:
    st.markdown("##### 🍔 Hábitos Alimenticios")
    favc = yes_no[st.selectbox("Consumo de comida calórica (FAVC)", ["No", 'Ocasionalmente',"Si"])] # FAVC es yes/no
    caec = caec_map[st.selectbox("Picoteo entre horas",['Nunca','Ocasionalmente','Frecuentemente','Siempre'])]
    fcvc = fcvc_map[st.selectbox("Consumo de vegetales (FCVC)", ['Baja','Media','Alta'])]
    ncp = ncp_map[st.selectbox("Comidas al día (NCP)",['1','2','3','4','5','+'])]
    ch2o = ch2o_map[st.selectbox("Agua diaria (CH2O) en litros", ['1', '1.5', '2', '2.5', '+'])]
    calc = consumo_map[st.selectbox("Alcohol (CALC)",['Nunca','Ocasionalmente','Frecuentemente','Siempre'])]

with col3:
    st.markdown("##### 🏃 Estilo de Vida")
    smoke = smoke_map[st.selectbox("Fumador", ["No", "Ocasionalmente", "Si"])]
    scc = yes_no[st.selectbox("Control de calorías diarias (SCC)",["No", "Si"])]
    faf = faf_map[st.selectbox("Actividad física (FAF)",['0','1','2','3','4','5','+'])]
    tue = tue_map[st.selectbox("Exposición a pantallas horas/día", ['0-2', '3-4', '5+'])]
    mtrans = mtrans_map[st.selectbox("Transporte habitual",['Coche','Moto','Bicicleta','Transporte Público','Caminando'])]

# ==========================================
# 5. PREDICCIÓN Y CÁLCULOS
# ==========================================
if pipeline is not None and le is not None:
    input_data = pd.DataFrame([[
        gender, age, height, weight, family_history, favc, 
        fcvc, ncp, caec, smoke, ch2o, scc, faf, tue, calc, mtrans
    ]], columns=[
        'gender', 'age', 'height', 'weight', 'family_history_with_overweight', 'favc', 
        'fcvc', 'ncp', 'caec', 'smoke', 'ch2o', 'scc', 'faf', 'tue', 'calc', 'mtrans'
    ])

    # Predicción a través del pipeline
    pred_encoded = pipeline.predict(input_data)[0]
    pred_text = le.inverse_transform([pred_encoded])[0]
    
    # Probabilidades
    probabilidades = pipeline.predict_proba(input_data)[0]
    confianza_max = np.max(probabilidades) * 100

    # Cálculo del IMC
    imc = weight / (height ** 2)

    # ==========================================
    # 6. MOSTRAR RESULTADOS (MÉTRICAS)
    # ==========================================
    st.markdown("---")
    st.write("### 📊 Resultados del Diagnóstico Predictivo")
    
    res_col1, res_col2, res_col3 = st.columns(3)
    
    # Añadimos el icono de la balanza aquí ⚖️
    res_col1.metric(label="⚖️ IMC Calculado (Masa Corporal)", value=f"{imc:.1f}")
    res_col2.metric(label="🎯 Predicción del Modelo", value=pred_text)
    res_col3.metric(label="🧠 Confianza Algorítmica", value=f"{confianza_max:.1f}%")

    # ==========================================
    # 7. VISUALIZACIÓN: BARRAS Y PASTEL (PIE CHART)
    # ==========================================
    st.markdown("---")
    st.write("### 📈 Probabilidades por Nivel de Obesidad")
    
    df_probs = pd.DataFrame({
        'Nivel de Obesidad': le.classes_,
        'Probabilidad (%)': probabilidades * 100
    })
    
    orden_clinico =['Insufficient_Weight', 'Normal_Weight', 'Overweight_Level_I', 
                     'Overweight_Level_II', 'Obesity_Type_I', 'Obesity_Type_II', 'Obesity_Type_III']
    
    df_probs['Nivel de Obesidad'] = pd.Categorical(df_probs['Nivel de Obesidad'], categories=orden_clinico, ordered=True)
    df_probs = df_probs.sort_values('Nivel de Obesidad')
    
    # Colores: Rojo para el ganador, Azul pálido para el resto
    colores_bar =["#ff7363" if clase == pred_text else "#5DDB15" for clase in df_probs['Nivel de Obesidad']]

    # Creamos 2 columnas para poner el gráfico de barras y el de pastel lado a lado
    chart_col1, chart_col2 = st.columns(2)

    with chart_col1:
        # --- GRÁFICO DE BARRAS ---
        fig_bar, ax_bar = plt.subplots(figsize=(8, 5))
        fig_bar.patch.set_facecolor("#E3F8F8") # Fondo igual al CSS
        ax_bar.set_facecolor("#D3F7E5")
        
        ax_bar.barh(df_probs['Nivel de Obesidad'], df_probs['Probabilidad (%)'], color=colores_bar, edgecolor='white')
        ax_bar.set_xlabel('Probabilidad (%)', fontweight='bold')
        ax_bar.set_xlim(0, 100)
        
        for container in ax_bar.containers:
            ax_bar.bar_label(container, fmt='%.1f%%', padding=5, fontweight='bold')
            
        ax_bar.spines['top'].set_visible(False)
        ax_bar.spines['right'].set_visible(False)
        ax_bar.spines['bottom'].set_visible(False)
        ax_bar.spines['left'].set_visible(False)
        
        st.pyplot(fig_bar)

    with chart_col2:
        # --- GRÁFICO DE PASTEL (PIE CHART) ---
        fig_pie, ax_pie = plt.subplots(figsize=(6, 5))
        fig_pie.patch.set_facecolor("#D3F7E5")
        
        # Filtramos probabilidades mayores al 2% para que el pastel no se vea saturado de ceros
        mask = df_probs['Probabilidad (%)'] > 2.0
        df_pie = df_probs[mask]
        colores_pie =["#ff7363" if clase == pred_text else "#5DDB15" for clase in df_pie['Nivel de Obesidad']]
        
        # Generar el Pie
        wedges, texts, autotexts = ax_pie.pie(
            df_pie['Probabilidad (%)'], 
            labels=df_pie['Nivel de Obesidad'], 
            autopct='%1.1f%%', 
            colors=colores_pie, 
            startangle=140,
            wedgeprops={'edgecolor': 'white', 'linewidth': 2}
        )
        
        # Estilizar textos del pastel
        for text in texts:
            text.set_fontsize(9)
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontweight('bold')
            
        ax_pie.axis('equal') # Asegura que sea un círculo perfecto
        st.pyplot(fig_pie)