import streamlit as st
import pandas as pd
import joblib
import plotly.graph_objects as go
import os
from datetime import datetime
from streamlit_lottie import st_lottie
import json
from dotenv import load_dotenv  
from sqlalchemy import create_engine 
# ==================== CONFIGURACIÓN ====================
# Cargar variables de entorno
load_dotenv()

st.set_page_config(
    page_title="HealthCheck AI - Asistente Nutricional",
    page_icon="⚖️",
    layout="wide"
)
def load_lottie_file(filepath: str):
    with open(filepath, "r") as f:
        return json.load(f)

# Cargar tu archivo (ajusta la ruta según donde lo guardes)
lottie_balanza = load_lottie_file("assest/Live chatbot.json")

# CSS personalizado 
st.markdown("""
    <style>
    /* FONDO GENERAL CON GRADIENTE OCEAN */
    .main {
        padding: 0rem 1rem;
        background: linear-gradient(135deg, #0f2027 0%, #203a43 50%, #2c5364 100%);
    }
    
    /* MENSAJES DEL CHAT - ESTILO PREMIUM */
    .chat-message {
        background: linear-gradient(135deg, #ffffff 0%, #f0f9ff 100%);
        padding: 24px;
        border-radius: 20px;
        margin: 18px 0;
        border-left: 6px solid #0891b2;
        box-shadow: 0 10px 30px rgba(8, 145, 178, 0.3);
        font-size: 20px;
        line-height: 1.7;
        position: relative;
        overflow: hidden;
    }
    .chat-message::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: linear-gradient(90deg, #0891b2, #06b6d4, #22d3ee);
    }
    .assistant-message {
        border-left: 6px solid #0891b2;
        background: linear-gradient(135deg, #cffafe 0%, #e0f2fe 100%);
    }
    .user-message {
        border-left: 6px solid #f59e0b;
        background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
    }
    .chat-message strong {
        font-size: 22px;
        background: linear-gradient(135deg, #0c4a6e 0%, #075985 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
    }
    
    /* HEADERS CON COLORES BRILLANTES Y ALTA VISIBILIDAD */
    h1 {
        color: #ffffff !important;
        text-align: center;
        margin-bottom: 10px;
        font-size: 75px;
        font-weight: 900;
        text-shadow: 
            0 0 40px rgba(6, 182, 212, 0.8),
            0 0 20px rgba(251, 191, 36, 0.6),
            0 4px 10px rgba(0, 0, 0, 0.5);
        letter-spacing: -1px;
    }
    h2 {
        color: #ffffff !important;
        font-size: 42px;
        font-weight: 800;
        text-shadow: 
            0 0 30px rgba(6, 182, 212, 0.7),
            0 4px 10px rgba(0, 0, 0, 0.4);
    }
    h3 {
        color: #ffffff !important;
        font-size: 32px;
        font-weight: 700;
        text-shadow: 
            0 0 20px rgba(6, 182, 212, 0.6),
            0 2px 8px rgba(0, 0, 0, 0.3);
    }
    h4 {
        color: #bae6fd;
        font-weight: 600;
    }
    
    /* INDICADOR DE PASOS - OCEAN STYLE */
    .step-indicator {
        background: linear-gradient(135deg, #0891b2 0%, #06b6d4 50%, #0ea5e9 100%);
        color: white;
        padding: 18px 32px;
        border-radius: 20px;
        text-align: center;
        font-weight: 800;
        font-size: 20px;
        margin-bottom: 28px;
        box-shadow: 0 12px 35px rgba(8, 145, 178, 0.4);
        letter-spacing: 1px;
        border: 2px solid rgba(255, 255, 255, 0.2);
    }
    
    /* BARRA DE PROGRESO */
    .stProgress > div > div > div {
        background: linear-gradient(90deg, #0891b2 0%, #06b6d4 50%, #fbbf24 100%);
        box-shadow: 0 4px 15px rgba(8, 145, 178, 0.5);
    }
    
    /* CONTENEDOR DEL AVATAR - OCEAN PREMIUM */
    .avatar-container {
        background: linear-gradient(135deg, #ffffff 0%, #f0f9ff 100%);
        border-radius: 28px;
        padding: 38px;
        text-align: center;
        box-shadow: 0 20px 50px rgba(8, 145, 178, 0.35);
        border: 3px solid rgba(6, 182, 212, 0.3);
        position: sticky;
        top: 20px;
        position: relative;
        overflow: hidden;
    }
    .avatar-container::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(6, 182, 212, 0.1) 0%, transparent 70%);
        animation: pulse 4s ease-in-out infinite;
    }
    @keyframes pulse {
        0%, 100% { transform: scale(1); opacity: 0.5; }
        50% { transform: scale(1.1); opacity: 0.8; }
    }
    .avatar-image {
        font-size: 200px;
        margin: 20px 0;
        animation: float 3s ease-in-out infinite;
        filter: drop-shadow(0 20px 35px rgba(6, 182, 212, 0.5));
        position: relative;
        z-index: 1;
    }
    @keyframes float {
        0%, 100% { transform: translateY(0px) rotate(0deg); }
        50% { transform: translateY(-20px) rotate(5deg); }
    }
    .avatar-text {
        font-size: 24px;
        background: linear-gradient(135deg, #0891b2 0%, #06b6d4 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-top: 10px;
        font-weight: 800;
        position: relative;
        z-index: 1;
    }
    
    /* CONTENEDORES CON EFECTO GLASS - GLASSMORPHISM */
    [data-testid="stVerticalBlock"] > [data-testid="stVerticalBlock"] {
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.95) 0%, rgba(240, 249, 255, 0.9) 100%);
        border-radius: 30px;
        padding: 35px;
        box-shadow: 
            0 25px 60px rgba(8, 145, 178, 0.25),
            inset 0 1px 0 rgba(255, 255, 255, 0.6);
        border: 2px solid rgba(6, 182, 212, 0.2);
        backdrop-filter: blur(20px);
    }
    
    /* INPUTS Y SELECTBOX - OCEAN STYLE */
    div[data-baseweb="select"] > div {
        font-size: 21px !important;
        font-weight: 600 !important;
        color: #0c4a6e !important;
        border-radius: 16px !important;
        border: 3px solid #7dd3fc !important;
        background: linear-gradient(135deg, #ffffff 0%, #f0f9ff 100%) !important;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1) !important;
        box-shadow: 0 4px 15px rgba(8, 145, 178, 0.1) !important;
    }
    div[data-baseweb="select"] > div:focus-within {
        border-color: #0891b2 !important;
        box-shadow: 0 0 0 5px rgba(8, 145, 178, 0.2), 0 8px 25px rgba(8, 145, 178, 0.3) !important;
        transform: translateY(-3px);
    }
    div[role="listbox"] li {
        font-size: 19px !important;
        padding: 16px !important;
        font-weight: 600 !important;
        color: #0c4a6e !important;
    }
    div[role="listbox"] li:hover {
        background: linear-gradient(135deg, #cffafe 0%, #e0f2fe 100%) !important;
    }
    input[type="number"], input[type="text"] {
        font-size: 21px !important;
        font-weight: 600 !important;
        color: #0c4a6e !important;
        border-radius: 16px !important;
        border: 3px solid #7dd3fc !important;
        background: linear-gradient(135deg, #ffffff 0%, #f0f9ff 100%) !important;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1) !important;
        box-shadow: 0 4px 15px rgba(8, 145, 178, 0.1) !important;
    }
    input[type="number"]:focus, input[type="text"]:focus {
        border-color: #0891b2 !important;
        box-shadow: 0 0 0 5px rgba(8, 145, 178, 0.2), 0 8px 25px rgba(8, 145, 178, 0.3) !important;
        transform: translateY(-3px);
    }
    
    /* BOTONES OCEAN PREMIUM */
    .stButton > button, .stDownloadButton > button {
        font-size: 18px !important;
        font-weight: 800 !important;
        padding: 20px 40px !important;
        border-radius: 18px !important;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1) !important;
        box-shadow: 0 10px 30px rgba(8, 145, 178, 0.35) !important;
        border: none !important;
        background: linear-gradient(135deg, #0891b2 0%, #06b6d4 50%, #0ea5e9 100%) !important;
        color: white !important;
        letter-spacing: 1px !important;
        text-transform: uppercase;
        position: relative;
        overflow: hidden;
    }
    .stButton > button::before, .stDownloadButton > button::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.3), transparent);
        transition: left 0.5s;
    }
    .stButton > button:hover::before, stDownloadButton > button:hover::before {
        left: 100%;
    }
    .stButton > button:hover, .stDownloadButton > button:hover {
        transform: translateY(-5px) scale(1.03) !important;
        box-shadow: 0 18px 45px rgba(8, 145, 178, 0.5) !important;
    }
    .stButton > button:active, .stDownloadButton > button:active {
        transform: translateY(-2px) scale(0.98) !important;
    }
    
    /* BOTÓN PRIMARY (Dorado) */
    .stButton > button[kind="primary"], stDownloadButton > button[kind="primary"] {
        background: linear-gradient(135deg, #f59e0b 0%, #fbbf24 50%, #fcd34d 100%) !important;
        box-shadow: 0 10px 30px rgba(245, 158, 11, 0.35) !important;
    }
    .stButton > button[kind="primary"]:hover, .stDownloadButton > button[kind="primary"]:hover {
        box-shadow: 0 18px 45px rgba(245, 158, 11, 0.5) !important;
    }
    
    /* ADVERTENCIA OCEAN STYLE */
    .warning-box {
        background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
        padding: 22px;
        border-radius: 18px;
        border-left: 6px solid #f59e0b;
        margin-top: 22px;
        box-shadow: 0 8px 25px rgba(245, 158, 11, 0.3);
        color: #78350f;
        font-weight: 700;
        position: relative;
        overflow: hidden;
    }
    .warning-box::before {
        content: '⚠️';
        position: absolute;
        right: 20px;
        top: 50%;
        transform: translateY(-50%);
        font-size: 40px;
        # opacity: 0.2;
    }
    
    /* QUITAR ESPACIO ENTRE LABEL E INPUT */
    div[data-testid="stTextInput"] {
        margin-top: -20px;
    }
    
    /* EFECTOS ADICIONALES */
    /* Subtítulo principal */
    .main > div > div > div > div > p {
        color: #ffffff !important;
        text-shadow: 
            0 0 20px rgba(251, 191, 36, 0.6),
            0 2px 6px rgba(0, 0, 0, 0.4);
        font-weight: 600 !important;
        font-size: 22px !important;
    }
    /* Textos normales en formulario */
    p {
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

# ==================== CARGAR MODELO ====================
@st.cache_resource
def load_assets():
    path = 'models/modelo_obesidad_final_g.pkl'
    if os.path.exists(path):
        return joblib.load(path)
    # Fallback al modelo optimizado
    path_alt = 'models/modelo_obesidad_final_g.pkl'
    if os.path.exists(path_alt):
        return joblib.load(path_alt)
    return None

assets = load_assets()

# ==================== INFORMACIÓN DE CATEGORÍAS ====================
CATEGORIAS_INFO = {
    'Insufficient_Weight': {
        'nombre': 'Peso Insuficiente',
        'color': '#0ea5e9',
        'icono': '⚖️',
        'riesgo': 'MODERADO',
        'recomendaciones': [
            '📞 Contacta con nosotros en el XXX XXX XXX',
            'Consultar con nutricionista para plan de ganancia de peso saludable',
            'Incrementar ingesta calórica con alimentos nutritivos',
            'Incluir proteínas de calidad en cada comida',
            'Realizar ejercicio de fuerza para ganar masa muscular'
        ]
    },
    'Normal_Weight': {
        'nombre': 'Peso Normal',
        'color': '#10b981',
        'icono': '✅',
        'riesgo': 'BAJO',
        'recomendaciones': [
            'Mantener el peso actual con hábitos equilibrados',
            'Incrementar consumo de vegetales a diario',
            'Actividad física moderada 3-4 días por semana',
            'Mantener hidratación adecuada de 2-2.5 litros diarios'
        ]
    },
    'Overweight_Level_I': {
        'nombre': 'Sobrepeso Nivel I',
        'color': '#fbbf24',
        'icono': '⚠️',
        'riesgo': 'MODERADO',
        'recomendaciones': [
            '📞 Contacta con nosotros en el XXX XXX XXX',
            'Reducir consumo de alimentos procesados y azúcares',
            'Aumentar actividad física a 4-5 días por semana',
            'Control de porciones y horarios regulares de comida',
            'Incluir más vegetales y frutas en la dieta'
        ]
    },
    'Overweight_Level_II': {
        'nombre': 'Sobrepeso Nivel II',
        'color': '#fb923c',
        'icono': '⚠️',
        'riesgo': 'ALTO',
        'recomendaciones': [
            '📞 Contacta con nosotros en el XXX XXX XXX',
            'Plan nutricional estructurado con profesional',
            'Ejercicio cardiovascular 5 días por semana',
            'Reducir significativamente alimentos ultraprocesados',
            'Monitoreo de presión arterial y glucosa'
        ]
    },
    'Obesity_Type_I': {
        'nombre': 'Obesidad Tipo I',
        'color': '#f97316',
        'icono': '🚨',
        'riesgo': 'ALTO',
        'recomendaciones': [
            '📞 Contacta con nosotros en el XXX XXX XXX',
            'Intervención nutricional intensiva inmediata',
            'Plan de ejercicio supervisado por profesional',
            'Evaluación médica completa de comorbilidades',
            'Establecer objetivos realistas de pérdida de peso'
        ]
    },
    'Obesity_Type_II': {
        'nombre': 'Obesidad Tipo II',
        'color': '#ef4444',
        'icono': '🚨',
        'riesgo': 'CRÍTICO',
        'recomendaciones': [
            '📞 Contacta con nosotros en el XXX XXX XXX',
            'Atención médica especializada urgente',
            'Evaluación de riesgos cardiovasculares y metabólicos',
            'Plan nutricional médicamente supervisado',
            'Valorar tratamiento farmacológico si es necesario'
        ]
    },
    'Obesity_Type_III': {
        'nombre': 'Obesidad Tipo III',
        'color': '#dc2626',
        'icono': '🚨',
        'riesgo': 'CRÍTICO',
        'recomendaciones': [
            '📞 Contacta con nosotros en el XXX XXX XXX',
            'Atención médica especializada inmediata',
            'Evaluación para cirugía bariátrica si cumple criterios',
            'Tratamiento integral por equipo multidisciplinario',
            'Monitoreo continuo de complicaciones'
        ]
    }
}

# ==================== ESTADO DE SESIÓN ====================
if 'step' not in st.session_state:
    st.session_state.step = 0
if 'data' not in st.session_state:
    st.session_state.data = {}
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
    # Saludo inicial automático
    st.session_state.chat_history.append({
        'role': 'assistant',
        'content': '¡Hola! 👋 Bienvenido a HealthCheck AI. Soy tu asistente nutricional inteligente y voy a ayudarte a evaluar tu estado de salud de forma personalizada.<br><br>📋 <strong>Para comenzar, rellena el formulario del centro</strong> con tus datos personales. Iré conversando contigo mientras completas cada paso. ¡Estoy aquí para ayudarte en todo momento! 😊'
    })
if 'show_modal' not in st.session_state:
    st.session_state.show_modal = False

def next_step():
    st.session_state.step += 1
    # Compatible con versiones antiguas y nuevas de Streamlit
    if hasattr(st, 'rerun'):
        st.rerun()
    else:
        st.experimental_rerun()

def reset_app():
    st.session_state.step = 0
    st.session_state.data = {}
    st.session_state.chat_history = [{
        'role': 'assistant',
        'content': '¡Hola! 👋 Bienvenido a HealthCheck AI. Soy tu asistente nutricional inteligente y voy a ayudarte a evaluar tu estado de salud de forma personalizada.<br><br>📋 <strong>Para comenzar, rellena el formulario del centro</strong> con tus datos personales. Iré conversando contigo mientras completas cada paso. ¡Estoy aquí para ayudarte en todo momento! 😊'
    }]
    st.session_state.show_modal = False
    # Compatible con versiones antiguas y nuevas de Streamlit
    if hasattr(st, 'rerun'):
        st.rerun()
    else:
        st.experimental_rerun()

## ==================== HEADER CON LOTTIE ====================
import streamlit.components.v1 as components

# Cargar el JSON del Lottie
lottie_balanza = load_lottie_file("assest/Live chatbot.json")

# Convertir el JSON a string para insertarlo en el HTML
import json
lottie_json_str = json.dumps(lottie_balanza)

# Crear el header completo en HTML
header_html = f"""
<!DOCTYPE html>
<html>
<head>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/bodymovin/5.12.2/lottie.min.js"></script>
    <style>
        body {{
            margin: 0;
            padding: 0;
            background: linear-gradient(135deg, #0f2027 0%, #203a43 50%, #2c5364 100%);
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
        }}
        .header-container {{
            display: flex;
            align-items: center;
            padding: 10px;
            background: transparent;
        }}
        .lottie-wrapper {{
            width: 180px;
            height: 180px;
            margin-right: 20px;
            background: transparent;
        }}
        .title-wrapper {{
            flex: 1;
        }}
        h1 {{
            color: #ffffff;
            font-size: 50px;
            font-weight: 900;
            margin: 0 0 10px 0;
            text-shadow: 
                0 0 40px rgba(6, 182, 212, 0.8),
                0 0 20px rgba(251, 191, 36, 0.6),
                0 4px 10px rgba(0, 0, 0, 0.5);
            letter-spacing: -1px;
        }}
        h2 {{
            color: #ffffff;
            font-size: 22px;
            font-weight: 600;
            margin: 0;
            text-shadow: 
                0 0 20px rgba(251, 191, 36, 0.6),
                0 2px 6px rgba(0, 0, 0, 0.4);
        }}
    </style>
</head>
<body>
    <div class="header-container">
        <div class="lottie-wrapper" id="lottie-animation"></div>
        <div class="title-wrapper">
            <h1> HealthCheck AI - Asistente Nutricional Inteligente</h1>
            <h2>Tu compañero personal de salud y bienestar</h2>
        </div>
    </div>
    <script>
        var animationData = {lottie_json_str};
        lottie.loadAnimation({{
            container: document.getElementById('lottie-animation'),
            renderer: 'svg',
            loop: true,
            autoplay: true,
            animationData: animationData
        }});
    </script>
</body>
</html>
"""

components.html(header_html, height=220)

# Indicador de paso
steps_labels = [
    " Presentación",
    " Medidas Corporales", 
    " Hábitos Alimenticios",
    " Estilo de Vida",
    " Diagnóstico"
]
if st.session_state.step < len(steps_labels):
    progress = (st.session_state.step + 1) / len(steps_labels)
    st.progress(progress)
    st.markdown(f'<div class="step-indicator">Paso {st.session_state.step + 1}/{len(steps_labels)}: {steps_labels[st.session_state.step]}</div>', unsafe_allow_html=True)

# ==================== LAYOUT PRINCIPAL (3 COLUMNAS) ====================
col_chat, col_form, col_avatar = st.columns([2, 3, 2])

# ==================== COLUMNA IZQUIERDA - CHAT ====================
with col_chat:
    st.markdown("## 💬 Conversación")
    
    # Mostrar solo los últimos 3 mensajes del chat
    chat_container = st.container()
    with chat_container:
        mensajes_recientes = st.session_state.chat_history[-3:] if len(st.session_state.chat_history) > 3 else st.session_state.chat_history
        
        for message in mensajes_recientes:
            if message['role'] == 'assistant':
                st.markdown(f"""
                    <div class="chat-message assistant-message">
                        <strong>🤖 Asistente:</strong><br>{message['content']}
                    </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                    <div class="chat-message user-message">
                        <strong>Tú:</strong><br>{message['content']}
                    </div>
                """, unsafe_allow_html=True)

# ==================== COLUMNA CENTRAL - FORMULARIO ====================
with col_form:
    st.markdown("## 📝 Formulario")
    
    # Si estamos en paso 4, mostrar resultados aquí en lugar del formulario
    if st.session_state.step == 4:
        # MOSTRAR RESULTADOS EN EL CENTRO
        # Construir input para el modelo
        input_dict = {
            'gender': st.session_state.data['gender'],
            'age': st.session_state.data['age'],
            'height': st.session_state.data['height'],
            'weight': st.session_state.data['weight'],
            'family_history': st.session_state.data['family_history'],
            'favc': st.session_state.data['favc'],
            'fcvc': st.session_state.data['fcvc'],
            'ncp': st.session_state.data['ncp'],
            'caec': st.session_state.data['caec'],
            'smoke': st.session_state.data['smoke'],
            'ch2o': st.session_state.data['ch2o'],
            'scc': "no",
            'faf': st.session_state.data['faf'],
            'tue': 1.0,
            'calc': st.session_state.data['calc'],
            'mtrans': "Public_Transportation",
            'imc': st.session_state.data['imc']
        }
        
        try:
            df_input = pd.DataFrame([input_dict])
            
            # Predicción
            if assets and 'pipeline' in assets:
                pred = assets['pipeline'].predict(df_input)
                label = assets['label_encoder'].inverse_transform(pred)[0]
                probs = assets['pipeline'].predict_proba(df_input)[0]
                clases = assets['label_encoder'].inverse_transform(assets['pipeline'].classes_)
            elif assets:
                pred = assets.predict(df_input)
                label = pred[0]
                probs = assets.predict_proba(df_input)[0]
                clases = assets.classes_
            else:
                st.error("⚠️ No se pudo cargar el modelo")
                st.stop()
            
            # Información de la categoría
            info_categoria = CATEGORIAS_INFO.get(label, CATEGORIAS_INFO['Normal_Weight'])
            confianza = max(probs) * 100
            
            # Actualizar mensaje del chat si no existe
            if not any('completado el análisis' in msg.get('content', '') for msg in st.session_state.chat_history):
                st.session_state.chat_history.append({
                    'role': 'assistant',
                    'content': f'📊 ¡Listo! Tu categoría es: **{info_categoria["nombre"]}** con {confianza:.1f}% de confianza. Riesgo: **{info_categoria["riesgo"]}**'
                })
            
            # RESULTADOS
            st.markdown(f"###  🎯 Resultados de {st.session_state.data.get('nombre', 'Usuario')}")
            
            # Métricas principales
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown(f"""
                    <div style='
                        background: linear-gradient(135deg, {info_categoria["color"]}40 0%, {info_categoria["color"]}60 100%); 
                        padding: 24px; 
                        border-radius: 18px; 
                        text-align: center; 
                        border: 3px solid {info_categoria["color"]};
                        box-shadow: 0 8px 25px {info_categoria["color"]}50;
                    '>
                        <p style='margin: 0; font-size: 16px; color: #ffffff; font-weight: 700; text-shadow: 0 2px 4px rgba(0,0,0,0.3);'>Categoría</p>
                        <p style='margin: 12px 0 0 0; font-size: 26px; font-weight: 900; color: #ffffff; text-shadow: 0 3px 6px rgba(0,0,0,0.4);'>
                            {info_categoria['icono']} {info_categoria['nombre']}
                        </p>
                    </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"""
                    <div style='
                        background: linear-gradient(135deg, #06b6d4 0%, #0891b2 100%); 
                        padding: 24px; 
                        border-radius: 18px; 
                        text-align: center; 
                        border: 3px solid #0ea5e9;
                        box-shadow: 0 8px 25px rgba(6, 182, 212, 0.5);
                    '>
                        <p style='margin: 0; font-size: 16px; color: #ffffff; font-weight: 700; text-shadow: 0 2px 4px rgba(0,0,0,0.3);'>Confianza</p>
                        <p style='margin: 12px 0 0 0; font-size: 26px; font-weight: 900; color: #ffffff; text-shadow: 0 3px 6px rgba(0,0,0,0.4);'>
                            {confianza:.1f}%
                        </p>
                    </div>
                """, unsafe_allow_html=True)
            
            with col3:
                color_riesgo = {
                    'BAJO': '#10b981',
                    'MODERADO': '#fbbf24',
                    'ALTO': '#fb923c',
                    'CRÍTICO': '#ef4444'
                }
                st.markdown(f"""
                    <div style='
                        background: linear-gradient(135deg, {color_riesgo[info_categoria["riesgo"]]}80 0%, {color_riesgo[info_categoria["riesgo"]]} 100%); 
                        padding: 24px; 
                        border-radius: 18px; 
                        text-align: center; 
                        border: 3px solid {color_riesgo[info_categoria["riesgo"]]};
                        box-shadow: 0 8px 25px {color_riesgo[info_categoria["riesgo"]]}50;
                    '>
                        <p style='margin: 0; font-size: 16px; color: #ffffff; font-weight: 700; text-shadow: 0 2px 4px rgba(0,0,0,0.3);'>Riesgo</p>
                        <p style='margin: 12px 0 0 0; font-size: 26px; font-weight: 900; color: #ffffff; text-shadow: 0 3px 6px rgba(0,0,0,0.4);'>
                            {info_categoria['riesgo']}
                        </p>
                    </div>
                """, unsafe_allow_html=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            # Gráfico de probabilidades
            st.markdown("####   Distribución de Probabilidades")
            
            # Preparar datos
            prob_dict = dict(zip(clases, probs * 100))
            categorias_ordenadas = ['Insufficient_Weight','Normal_Weight', 'Overweight_Level_I', 
                                   'Overweight_Level_II', 'Obesity_Type_I', 'Obesity_Type_II', 'Obesity_Type_III']
            
            nombres = []
            colores = []
            valores = []
            opacidades = []
            anchos_borde = []
            
            for cat in categorias_ordenadas:
                if cat in CATEGORIAS_INFO:
                    nombres.append(CATEGORIAS_INFO[cat]['nombre'])
                    
                    # Si es la categoría predicha, hacer más brillante y con borde
                    if cat == label:
                        colores.append(CATEGORIAS_INFO[cat]['color'])
                        opacidades.append(1.0)  # Opacidad completa
                        anchos_borde.append(5)  # Borde más grueso
                    else:
                        colores.append(CATEGORIAS_INFO[cat]['color'])
                        opacidades.append(0.35)  # Más transparente
                        anchos_borde.append(1)  # Borde fino
                    
                    valores.append(prob_dict.get(cat, 0))
            
            # Crear trazas individuales para cada barra con diferentes opacidades
            fig = go.Figure()
            
            for i, (nombre, valor, color, opacidad, ancho) in enumerate(zip(nombres, valores, colores, opacidades, anchos_borde)):
                # Convertir hex a rgba para manejar opacidad
                import matplotlib.colors as mcolors
                rgb = mcolors.hex2color(color)
                rgba = f'rgba({int(rgb[0]*255)}, {int(rgb[1]*255)}, {int(rgb[2]*255)}, {opacidad})'
                
                fig.add_trace(go.Bar(
                    y=[nombre],
                    x=[valor],
                    orientation='h',
                    marker=dict(
                        color=rgba,
                        line=dict(
                            color=color if opacidad == 1.0 else '#d1d5db',
                            width=ancho
                        )
                    ),
                    text=f"{valor:.1f}%",
                    textposition='auto',
                    textfont=dict(
                        size=20 if opacidad == 1.0 else 14,
                        color='white' if opacidad == 1.0 else '#6b7280',
                        family='Arial Black' if opacidad == 1.0 else 'Arial'
                    ),
                    hovertemplate=f'<b>{nombre}</b><br>Probabilidad: {valor:.2f}%<extra></extra>',
                    showlegend=False
                ))
            
            fig.update_layout(
                height=440,
                margin=dict(l=20, r=20, t=20, b=20),
                xaxis=dict(
                    title="Probabilidad (%)", 
                    title_font=dict(size=19, color='#0c4a6e', family='Arial Black'),
                    range=[0, 108], 
                    gridcolor='#e0f2fe',
                    tickfont=dict(size=16, color='#0c4a6e', family='Arial Black')
                ),
                yaxis=dict(
                    title="", 
                    autorange="reversed",
                    tickfont=dict(size=17, color='#0c4a6e', family='Arial Black')
                ),
                plot_bgcolor='#f0f9ff',
                paper_bgcolor='white',
                font=dict(size=15, color='#0c4a6e'),
                bargap=0.18
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Recomendaciones con colores dinámicos según categoría
            st.markdown("####   Recomendaciones Personalizadas")
            
            # Definir colores de fondo según el riesgo
            color_fondo_map = {
                'BAJO': 'linear-gradient(135deg, #d1fae5 0%, #a7f3d0 100%)',
                'MODERADO': 'linear-gradient(135deg, #fef3c7 0%, #fde68a 100%)',
                'ALTO': 'linear-gradient(135deg, #fed7aa 0%, #fdba74 100%)',
                'CRÍTICO': 'linear-gradient(135deg, #fecaca 0%, #fca5a5 100%)'
            }
            
            color_borde_map = {
                'BAJO': '#10b981',
                'MODERADO': '#f59e0b',
                'ALTO': '#f97316',
                'CRÍTICO': '#ef4444'
            }
            
            color_texto_map = {
                'BAJO': '#064e3b',
                'MODERADO': '#78350f',
                'ALTO': '#7c2d12',
                'CRÍTICO': '#7f1d1d'
            }
            
            nivel_riesgo = info_categoria['riesgo']
            fondo = color_fondo_map.get(nivel_riesgo, color_fondo_map['BAJO'])
            borde = color_borde_map.get(nivel_riesgo, color_borde_map['BAJO'])
            texto = color_texto_map.get(nivel_riesgo, color_texto_map['BAJO'])
            
            for i, rec in enumerate(info_categoria['recomendaciones'], 1):
                st.markdown(f"""
                    <div style='
                        background: {fondo};
                        padding: 20px;
                        border-radius: 16px;
                        margin: 16px 0;
                        border-left: 6px solid {borde};
                        box-shadow: 0 6px 20px rgba(8, 145, 178, 0.15);
                        font-size: 18px;
                        color: {texto};
                        font-weight: 600;
                        line-height: 1.6;
                    '>
                        <strong style="font-size: 20px; color: {texto};">🔹 {i}.</strong> {rec}
                    </div>
                """, unsafe_allow_html=True)
            
            # Botones de acción con mejor diseño
            st.markdown("<br>", unsafe_allow_html=True)
            col_btn1, col_btn2, col_btn3, col_btn4 = st.columns(4)
           
            with col_btn1:
                if st.button(" Guardar Resultado", use_container_width=True, key="save_result", type="primary"):
                    
                    # 1. Preparamos los datos a guardar
                    df_input['nombre'] = st.session_state.data['nombre']
                    df_input['prediccion'] = label
                    df_input['fecha'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    
                    guardado_exitoso_db = False
                    
                    # 2. INTENTO 1: Guardar en Base de Datos PostgreSQL
                    DATABASE_URL = os.environ.get("DATABASE_URL")
                    
                    if DATABASE_URL:
                        try:
                            if DATABASE_URL.startswith("postgres://"):
                                DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)
                                
                            engine = create_engine(DATABASE_URL)
                            df_input.to_sql('historico', con=engine, if_exists='append', index=False)
                            st.success(" Guardado exitosamente en la base de datos en la nube")
                            guardado_exitoso_db = True
                        except Exception as e:
                            # Si falla, mostramos una advertencia pero el programa sigue ejecutándose
                            st.warning(f"⚠️ La base de datos no está disponible. Usando archivo de respaldo...")
                            print(f"Error de DB: {e}") # Queda registrado en los logs
                    
                    # 3. INTENTO 2 (Fallback): Guardar en CSV si la BD falló o no existe
                    if not guardado_exitoso_db:
                        try:
                            if not os.path.exists('data'):
                                os.makedirs('data')
                                
                            df_input.to_csv('data/historico.csv', mode='a', index=False, sep=";",
                                          header=not os.path.exists('data/historico.csv'))
                            st.success(" Guardado exitosamente en el archivo local (CSV)")
                        except Exception as e:
                            st.error(f"❌ Error crítico: No se pudo guardar ni en DB ni en CSV.")
            with col_btn2:
                if st.button("Modificar Datos", use_container_width=True, key="back_step"):
                    st.session_state.step = 1
                    if hasattr(st, 'rerun'):
                        st.rerun()
                    else:
                        st.experimental_rerun()
            
            with col_btn3:
                if st.button("Nueva Consulta", use_container_width=True, key="new_consult"):
                    reset_app()
                    
            with col_btn4:
                datos_disponibles = False
                
                # 1. Intentamos leer de la base de datos
                try:
                    DATABASE_URL = os.environ.get("DATABASE_URL", "sqlite:///local_history.db")
                    if DATABASE_URL.startswith("postgres://"):
                        DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)
                    
                    engine = create_engine(DATABASE_URL)
                    df_descarga = pd.read_sql('historico', con=engine)
                    csv_descarga = df_descarga.to_csv(index=False).encode('utf-8')
                    datos_disponibles = True
                    
                except Exception:
                    # 2. Si falla, intentamos leer del CSV local como respaldo
                    try:
                        if os.path.exists('data/historico.csv'):
                            df_descarga = pd.read_csv('data/historico.csv', sep=";")
                            # Lo convertimos a formato texto para que el botón lo pueda descargar
                            csv_descarga = df_descarga.to_csv(index=False, sep=";").encode('utf-8')
                            datos_disponibles = True
                    except Exception:
                        pass
                
                # 3. Mostrar el botón adecuado
                if datos_disponibles:
                    st.download_button(
                        label="Descargar datos",
                        data=csv_descarga,
                        file_name="historico_obesidad.csv",
                        mime="text/csv",
                        use_container_width=True
                    )
                else:
                    # Si no hay datos en ningún sitio, mostramos un botón desactivado
                    st.button("📥 Sin datos", disabled=True, use_container_width=True)
            
            # Advertencia médica compacta
            st.markdown("""
                <div class='warning-box' style='font-size: 16px; padding: 18px;'>
                    <strong> Importante:</strong> Diagnóstico orientativo. Consulta con un profesional de la salud.
                </div>
            """, unsafe_allow_html=True)
            
        except Exception as e:
            st.error(f"❌ Error: {e}")
    
    else:
        # MOSTRAR FORMULARIO (pasos 0-3)
        with st.container():
            # PASO 0: Presentación
            if st.session_state.step == 0:
                st.markdown("###   ¡Empecemos!")
                st.markdown("""
                <p style='
                    font-size:26px;
                    font-weight:700;
                    margin-bottom:-50px;
                    margin-top:20px;
                    color:  white;
                '>
                Tu nombre
                </p>
                """, unsafe_allow_html=True)
                nombre = st.text_input("", value=st.session_state.data.get('nombre', ''), key="nombre_input", placeholder="Escribe tu nombre aquí...")
                
                st.markdown("""
                <p style='
                    font-size:26px;
                    font-weight:700;
                    margin-bottom:-50px;
                    margin-top:20px;
                    color: white;
                '>
                Género
                </p>
                """, unsafe_allow_html=True)
                genero = st.selectbox("", ["Femenino", "Masculino"], key="genero_input")
                if st.button(" Comenzar Evaluación", use_container_width=True, type="primary"):
                    if nombre:
                        st.session_state.data['nombre'] = nombre
                        st.session_state.data['gender'] = "Female" if genero == "Femenino" else "Male"
                        st.session_state.chat_history.append({
                            'role': 'user',
                            'content': f'Mi nombre es {nombre}, soy {genero}'
                        })
                        st.session_state.chat_history.append({
                            'role': 'assistant',
                            'content': f'¡Encantado de conocerte, {nombre}! 😊 Ahora necesito conocer tus medidas corporales para hacer una evaluación precisa. Por favor completa los campos del formulario.'
                        })
                        next_step()
                    else:
                        st.warning("⚠️ Por favor, ingresa tu nombre para continuar")
            
            # PASO 1: Medidas Corporales
            elif st.session_state.step == 1:
                st.markdown(f"###  📏 Medidas de {st.session_state.data.get('nombre', 'Usuario')}")
                st.markdown("""
                <p style='
                    font-size:26px;
                    font-weight:700;
                    margin-bottom:-50px;
                    margin-top:20px;
                    color:  white;
                '>
                Edad
                </p>
                """, unsafe_allow_html=True)
                edad = st.number_input("", min_value=10, max_value=100, value=st.session_state.data.get('age', 25), key="edad_input")
                st.markdown("""
                <p style='
                    font-size:26px;
                    font-weight:700;
                    margin-bottom:-50px;
                    margin-top:20px;
                    color:  white;
                '>
                Altura (m)
                </p>
                """, unsafe_allow_html=True)
                altura = st.number_input("", min_value=1.20, max_value=2.30, value=st.session_state.data.get('height', 1.70), step=0.01, key="altura_input")
                st.markdown("""
                <p style='
                    font-size:26px;
                    font-weight:700;
                    margin-bottom:-50px;
                    margin-top:20px;
                    color:  white;
                '>
                Peso (kg)
                </p>
                """, unsafe_allow_html=True)
                peso = st.number_input("", min_value=30.0, max_value=200.0, value=st.session_state.data.get('weight', 70.0), step=0.1, key="peso_input")
                
                # Calcular y mostrar IMC
                if altura > 0:
                    imc = peso / (altura ** 2)
                    st.markdown(f"""
                        <div style='background: linear-gradient(135deg, #cffafe 0%, #e0f2fe 100%); padding: 18px; border-radius: 14px; margin: 15px 0; border: 2px solid #06b6d4;'>
                            <p style='margin: 0; color: #0c4a6e; font-size: 16px; font-weight: 600;'> Tu IMC</p>
                            <p style='margin: 8px 0 0 0; color: #0891b2; font-size: 32px; font-weight: 800;'>{imc:.2f}</p>
                        </div>
                    """, unsafe_allow_html=True)
                
                if st.button(" Siguiente Paso", use_container_width=True):
                    st.session_state.data['age'] = edad
                    st.session_state.data['height'] = altura
                    st.session_state.data['weight'] = peso
                    st.session_state.data['imc'] = imc
                    
                    st.session_state.chat_history.append({
                        'role': 'user',
                        'content': f'Tengo {edad} años, mido {altura}m y peso {peso}kg (IMC: {imc:.2f})'
                    })
                    st.session_state.chat_history.append({
                        'role': 'assistant',
                        'content': 'Perfecto! 📝 Ahora cuéntame sobre tus hábitos alimenticios. Esta información es muy importante para entender tu situación nutricional.'
                    })
                    next_step()
            
            # PASO 2: Hábitos Alimenticios
            elif st.session_state.step == 2:
                st.markdown("### 🍽️  Tus Hábitos Alimenticios")
                
                fcvc_opciones = {
                    "Nunca": 1.0,
                    "Raramente": 1.5,
                    "A veces": 2.0,
                    "Frecuentemente": 2.5,
                    "Siempre": 3.0
                }
                st.markdown("""
                <p style='
                    font-size:26px;
                    font-weight:700;
                    margin-bottom:-50px;
                    margin-top:20px;
                    color: white;
                '>
                ¿Con qué frecuencia consumes vegetales?
                </p>
                """, unsafe_allow_html=True)
                fcvc_texto = st.selectbox(
                    "",
                    options=list(fcvc_opciones.keys()),
                    index=2,
                    key="fcvc_input"
                )
                fcvc = fcvc_opciones[fcvc_texto]
                st.markdown("""
                <p style='
                    font-size:26px;
                    font-weight:700;
                    margin-bottom:-50px;
                    margin-top:20px;
                    color:  white;
                '>
                ¿Cuántas comidas principales haces al día?
                </p>
                """, unsafe_allow_html=True)
                ncp = st.selectbox(
                    "",
                    options=["1 comida", "2 comidas", "3 comidas", "4 comidas o más"],
                    index=2,
                    key="ncp_input"
                )
                ncp_valor = {"1 comida": 1.0, "2 comidas": 2.0, "3 comidas": 3.0, "4 comidas o más": 4.0}[ncp]
                st.markdown("""
                <p style='
                    font-size:26px;
                    font-weight:700;
                    margin-bottom:-50px;
                    margin-top:20px;
                    color:  white;
                '>
                ¿Consumes alimentos altos en calorías frecuentemente?
                </p>
                """, unsafe_allow_html=True)
                favc = st.selectbox("", 
                                  ["No", "Sí"], key="favc_input")
                
                ch2o_opciones = {
                    "Menos de 1 litro": 0.5,
                    "1 - 1.5 litros": 1.0,
                    "1.5 - 2 litros": 1.5,
                    "2 - 2.5 litros": 2.0,
                    "2.5 - 3 litros": 2.5,
                    "Más de 3 litros": 3.0
                }
                st.markdown("""
                <p style='
                    font-size:26px;
                    font-weight:700;
                    margin-bottom:-50px;
                    margin-top:20px;
                    color:  white;
                '>
                ¿Cuántos litros de agua bebes al día?
                </p>
                """, unsafe_allow_html=True)
                ch2o_texto = st.selectbox(
                    "",
                    options=list(ch2o_opciones.keys()),
                    index=3,
                    key="ch2o_input"
                )
                ch2o = ch2o_opciones[ch2o_texto]
                
                caec_opciones = {
                    "Nunca": "no",
                    "A veces": "Sometimes",
                    "Frecuentemente": "Frequently",
                    "Siempre": "Always"
                }
                st.markdown("""
                <p style='font-size:26px; font-weight:700; margin-bottom:-50px; margin-top:20px; color: white;'>
                ¿Sueles comer entre comidas (snacks)?
                </p>
                """, unsafe_allow_html=True)
                caec_texto = st.selectbox("", options=list(caec_opciones.keys()), key="caec_input")
                caec_valor = caec_opciones[caec_texto]
                
                
                if st.button(" Siguiente Paso", use_container_width=True):
                    st.session_state.data['caec'] = caec_valor
                    st.session_state.data['fcvc'] = fcvc
                    st.session_state.data['ncp'] = ncp_valor
                    st.session_state.data['favc'] = "yes" if favc == "Sí" else "no"
                    st.session_state.data['ch2o'] = ch2o
                    
                    st.session_state.chat_history.append({
                        'role': 'user',
                        'content': f'Consumo vegetales {fcvc_texto.lower()}, hago {ncp}, {"sí" if favc == "Sí" else "no"} consumo alimentos calóricos frecuentemente, y bebo {ch2o_texto.lower()}'
                    })
                    st.session_state.chat_history.append({
                        'role': 'assistant',
                        'content': '¡Muy bien! 💪 Casi terminamos. Ahora cuéntame sobre tu estilo de vida y actividad física. Este es el último paso antes del diagnóstico.'
                    })
                    next_step()
            
            # PASO 3: Estilo de Vida
            elif st.session_state.step == 3:
                st.markdown("###  💪 Tu Estilo de Vida")
                
                faf_opciones = {
                    "Nunca (0 días)": 0.0,
                    "1 día a la semana": 1.0,
                    "2 días a la semana": 2.0,
                    "3 días a la semana": 3.0,
                    "4 días a la semana": 4.0,
                    "5 días a la semana": 5.0,
                    "6 días a la semana": 6.0,
                    "Todos los días": 7.0
                }
                st.markdown("""
                <p style='
                    font-size:26px;
                    font-weight:700;
                    margin-bottom:-50px;
                    margin-top:20px;
                    color:  white;
                '>
                ¿Cuántos días a la semana haces actividad física?
                </p>
                """, unsafe_allow_html=True)
                faf_texto = st.selectbox(
                    "",
                    options=list(faf_opciones.keys()),
                    index=2,
                    key="faf_input"
                )
                faf = faf_opciones[faf_texto]
                st.markdown("""
                <p style='
                    font-size:26px;
                    font-weight:700;
                    margin-bottom:-50px;
                    margin-top:20px;
                    color:  white;
                '>
                ¿Tienes antecedentes familiares de obesidad?
                </p>
                """, unsafe_allow_html=True)
                family = st.selectbox("", 
                                    ["No", "Sí"], key="family_input")
                st.markdown("""
                <p style='
                    font-size:26px;
                    font-weight:700;
                    margin-bottom:-50px;
                    margin-top:20px;
                    color:  white;
                '>
                ¿Fumas?
                </p>
                """, unsafe_allow_html=True)
                smoke = st.selectbox("", ["No", "Sí"], key="smoke_input")
                
                calc_opciones = {
                    "Nunca": "no",
                    "A veces": "Sometimes",
                    "Frecuentemente": "Frequently",
                    "Siempre": "Always"
                }
                st.markdown("""
                <p style='font-size:26px; font-weight:700; margin-bottom:-50px; margin-top:20px; color: white;'>
                ¿Con qué frecuencia consumes alcohol?
                </p>
                """, unsafe_allow_html=True)
                calc_texto = st.selectbox("", options=list(calc_opciones.keys()), key="calc_input")
                calc_valor = calc_opciones[calc_texto]
                
                if st.button(" Ver Mi Diagnóstico", use_container_width=True, type="primary"):
                    st.session_state.data['calc'] = calc_valor
                    st.session_state.data['faf'] = faf
                    st.session_state.data['family_history'] = "yes" if family == "Sí" else "no"
                    st.session_state.data['smoke'] = "yes" if smoke == "Sí" else "no"
                    
                    st.session_state.chat_history.append({
                        'role': 'user',
                        'content': f'Hago ejercicio {faf_texto.lower()}, {"sí" if family == "Sí" else "no"} tengo antecedentes familiares, y {"sí" if smoke == "Sí" else "no"} fumo'
                    })
                    st.session_state.chat_history.append({
                        'role': 'assistant',
                        'content': f'¡Excelente, {st.session_state.data.get("nombre")}! 🎉 Ya tengo toda la información que necesito. Déjame analizar tus datos con mi sistema de inteligencia artificial...'
                    })
                    st.session_state.show_modal = True
                    next_step()

# ==================== COLUMNA DERECHA - AVATAR ====================
with col_avatar:
    st.markdown("## 🤖 Asistente")
    
    # Avatar animado que cambia según el paso
    avatar_emojis = {
        0: "👋",  # Saludo
        1: "📏",  # Medidas
        2: "🍽️",  # Alimentación
        3: "💪",  # Ejercicio
        4: "🎯"   # Resultado
    }
    
    avatar_messages = {
        0: "¡Hola! Soy tu asistente",
        1: "Midiendo tu salud",
        2: "Analizando nutrición",
        3: "Evaluando actividad",
        4: "¡Listo para mostrar!"
    }
    
    current_emoji = avatar_emojis.get(st.session_state.step, "🤖")
    current_message = avatar_messages.get(st.session_state.step, "Procesando...")
    
    st.markdown(f"""
        <div class="avatar-container">
            <div class="avatar-image">{current_emoji}</div>
            <p class="avatar-text"><strong>{current_message}</strong></p>
            <p class="avatar-text" style="font-size: 14px;">Paso {st.session_state.step + 1} de 5</p>
        </div>
    """, unsafe_allow_html=True)