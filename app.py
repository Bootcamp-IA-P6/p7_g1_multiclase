import streamlit as st
import pandas as pd
import joblib
import plotly.graph_objects as go
import os
from datetime import datetime

# ==================== CONFIGURACIÓN ====================
st.set_page_config(
    page_title="HealthCheck AI - Asistente Nutricional",
    page_icon="⚖️",
    layout="wide"
)

# CSS personalizado - Diseño profesional y elegante
st.markdown("""
    <style>
    .main {
    padding: 0rem 1rem;
    }
    .chat-message {
        background: white;
        padding: 20px;
        border-radius: 15px;
        margin: 15px 0;
        border-left: 4px solid #059669;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        font-size: 20px;
        line-height: 1.6;
    }
    .assistant-message {
        border-left: 4px solid #1E88E5;
       
    }
    .user-message {
        border-left: 4px solid #059669;
        background: #f0fdf4;
    }
    .chat-message strong {
        font-size: 20px;
    }
    .stMetric {
        background-color: #f0f2f6;
        padding: 15px;
        border-radius: 10px;
    }
    h1 {
        color: #1E88E5;
        text-align: center;
        margin-bottom: 10px;
        font-size: 70px;
    }
    h2 {
        color: #059669;
        font-size: 40px;
    }
    h3 {
        color: #1E88E5;
        font-size: 30px;
    }
    .recommendation {
        background-color: #EAF3DE;
        padding: 15px;
        border-radius: 8px;
        margin: 10px 0;
        border-left: 4px solid #3B6D11;
    }
    .warning-box {
        background-color: #FCEBEB;
        padding: 15px;
        border-radius: 8px;
        border-left: 4px solid #E24B4A;
        margin-top: 20px;
    }
    .info-badge {
        background-color: #E6F1FB;
        color: #0C447C;
        padding: 5px 10px;
        border-radius: 5px;
        font-size: 12px;
        display: inline-block;
        margin: 5px 0;
    }
    .step-indicator {
        background: linear-gradient(90deg, #1E88E5, #059669);
        color: white;
        padding: 10px 20px;
        border-radius: 10px;
        text-align: center;
        font-weight: bold;
        margin-bottom: 20px;
    }
    .avatar-container {
        background: white;
        border-radius: 15px;
        padding: 20px;
        text-align: center;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        position: sticky;
        top: 20px;
    }
    .avatar-image {
        font-size: 200px;
        margin: 20px 0;
        animation: float 3s ease-in-out infinite;
    }
    @keyframes float {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
    }
    .avatar-text {
        font-size: 20px;
        color: #666;
        margin-top: 10px;
    }
    .resultado-container {
        background: white;
        border-radius: 20px;
        padding: 30px;
        box-shadow: 0 10px 40px rgba(0,0,0,0.2);
        margin-top: 20px;
    }
    /* QUITAR ESPACIO ENTRE LABEL E INPUT */
    div[data-testid="stTextInput"] {
        margin-top: -20px;
    }
    /* AUMENTAR TAMAÑO DE TEXTO EN SELECTBOX */
    div[data-baseweb="select"] > div {
        font-size: 20px !important;
        font-weight: 500 !important;
        color: #333 !important;
    }
    /* AUMENTAR TAMAÑO EN OPCIONES DEL DROPDOWN */
    div[role="listbox"] li {
        font-size: 18px !important;
        padding: 12px !important;
    }
    /* AUMENTAR TAMAÑO EN NUMBER INPUT */
    input[type="number"] {
        font-size: 20px !important;
        font-weight: 500 !important;
        color: #333 !important;
    }
    /* AUMENTAR TAMAÑO EN TEXT INPUT */
    input[type="text"] {
        font-size: 20px !important;
        font-weight: 500 !important;
        color: #333 !important;
    }
    /* AUMENTAR TAMAÑO DE TEXTO EN BOTONES */
    .stButton > button {
        font-size: 18px !important;
        font-weight: 600 !important;
        padding: 12px 24px !important;
        border-radius: 10px !important;
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
    path_alt = 'models/modelo_obesidad-g.pkl'
    if os.path.exists(path_alt):
        return joblib.load(path_alt)
    return None

assets = load_assets()

# ==================== INFORMACIÓN DE CATEGORÍAS ====================
CATEGORIAS_INFO = {
    'Insufficient_Weight': {
        'nombre': 'Peso Insuficiente',
        'color': '#378ADD',
        'icono': '⚖️',
        'riesgo': 'MODERADO',
        'recomendaciones': [
            'Consultar con nutricionista para plan de ganancia de peso saludable',
            'Incrementar ingesta calórica con alimentos nutritivos',
            'Incluir proteínas de calidad en cada comida',
            'Realizar ejercicio de fuerza para ganar masa muscular'
        ]
    },
    'Normal_Weight': {
        'nombre': 'Peso Normal',
        'color': '#3B6D11',
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
        'color': '#BA7517',
        'icono': '⚠️',
        'riesgo': 'MODERADO',
        'recomendaciones': [
            'Reducir consumo de alimentos procesados y azúcares',
            'Aumentar actividad física a 4-5 días por semana',
            'Control de porciones y horarios regulares de comida',
            'Incluir más vegetales y frutas en la dieta'
        ]
    },
    'Overweight_Level_II': {
        'nombre': 'Sobrepeso Nivel II',
        'color': '#EF9F27',
        'icono': '⚠️',
        'riesgo': 'ALTO',
        'recomendaciones': [
            'Plan nutricional estructurado con profesional',
            'Ejercicio cardiovascular 5 días por semana',
            'Reducir significativamente alimentos ultraprocesados',
            'Monitoreo de presión arterial y glucosa'
        ]
    },
    'Obesity_Type_I': {
        'nombre': 'Obesidad Tipo I',
        'color': '#D85A30',
        'icono': '🚨',
        'riesgo': 'ALTO',
        'recomendaciones': [
            'Intervención nutricional intensiva inmediata',
            'Plan de ejercicio supervisado por profesional',
            'Evaluación médica completa de comorbilidades',
            'Establecer objetivos realistas de pérdida de peso'
        ]
    },
    'Obesity_Type_II': {
        'nombre': 'Obesidad Tipo II',
        'color': '#E24B4A',
        'icono': '🚨',
        'riesgo': 'CRÍTICO',
        'recomendaciones': [
            'Atención médica especializada urgente',
            'Evaluación de riesgos cardiovasculares y metabólicos',
            'Plan nutricional médicamente supervisado',
            'Valorar tratamiento farmacológico si es necesario'
        ]
    },
    'Obesity_Type_III': {
        'nombre': 'Obesidad Tipo III',
        'color': '#A32D2D',
        'icono': '🚨',
        'riesgo': 'CRÍTICO',
        'recomendaciones': [
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

# ==================== HEADER ====================
st.markdown("# ⚖️ HealthCheck AI - Asistente Nutricional Inteligente")
st.markdown("### Tu compañero personal de salud y bienestar")

# Indicador de paso
steps_labels = [
    "👤 Presentación",
    "📏 Medidas Corporales", 
    "🍽️ Hábitos Alimenticios",
    "💪 Estilo de Vida",
    "📊 Diagnóstico"
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
                        <strong>👤 Tú:</strong><br>{message['content']}
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
            'caec': "Sometimes",
            'smoke': st.session_state.data['smoke'],
            'ch2o': st.session_state.data['ch2o'],
            'scc': "no",
            'faf': st.session_state.data['faf'],
            'tue': 1.0,
            'calc': "Sometimes",
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
            st.markdown(f"### 🎯 Resultados de {st.session_state.data.get('nombre', 'Usuario')}")
            
            # Métricas principales
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown(f"""
                    <div style='background-color: {info_categoria["color"]}22; padding: 20px; border-radius: 10px; text-align: center;'>
                        <p style='margin: 0; font-size: 14px; color: #666;'>Categoría</p>
                        <p style='margin: 8px 0 0 0; font-size: 22px; font-weight: bold; color: {info_categoria["color"]};'>
                            {info_categoria['icono']} {info_categoria['nombre']}
                        </p>
                    </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"""
                    <div style='background-color: #E6F1FB; padding: 20px; border-radius: 10px; text-align: center;'>
                        <p style='margin: 0; font-size: 14px; color: #666;'>Confianza</p>
                        <p style='margin: 8px 0 0 0; font-size: 22px; font-weight: bold; color: #185FA5;'>
                            {confianza:.1f}%
                        </p>
                    </div>
                """, unsafe_allow_html=True)
            
            with col3:
                color_riesgo = {
                    'BAJO': '#3B6D11',
                    'MODERADO': '#BA7517',
                    'ALTO': '#EF9F27',
                    'CRÍTICO': '#E24B4A'
                }
                st.markdown(f"""
                    <div style='background-color: {color_riesgo[info_categoria["riesgo"]]}22; padding: 20px; border-radius: 10px; text-align: center;'>
                        <p style='margin: 0; font-size: 14px; color: #666;'>Riesgo</p>
                        <p style='margin: 8px 0 0 0; font-size: 22px; font-weight: bold; color: {color_riesgo[info_categoria["riesgo"]]};'>
                            {info_categoria['riesgo']}
                        </p>
                    </div>
                """, unsafe_allow_html=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            # Gráfico de probabilidades
            st.markdown("#### 📊 Distribución de Probabilidades")
            
            # Preparar datos
            prob_dict = dict(zip(clases, probs * 100))
            categorias_ordenadas = ['Normal_Weight', 'Overweight_Level_I', 'Insufficient_Weight',
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
                        anchos_borde.append(4)  # Borde más grueso
                    else:
                        colores.append(CATEGORIAS_INFO[cat]['color'])
                        opacidades.append(0.4)  # Más transparente
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
                            color=color if opacidad == 1.0 else 'lightgray',
                            width=ancho
                        )
                    ),
                    text=f"{valor:.1f}%",
                    textposition='auto',
                    textfont=dict(
                        size=18 if opacidad == 1.0 else 14,
                        color='white' if opacidad == 1.0 else '#666',
                        family='Arial Black' if opacidad == 1.0 else 'Arial'
                    ),
                    hovertemplate=f'<b>{nombre}</b><br>Probabilidad: {valor:.2f}%<extra></extra>',
                    showlegend=False
                ))
            
            fig.update_layout(
                height=420,
                margin=dict(l=20, r=20, t=20, b=20),
                xaxis=dict(
                    title="Probabilidad (%)", 
                    title_font=dict(size=18, color='#333', family='Arial Black'),
                    range=[0, 105], 
                    gridcolor='#E0E0E0',
                    tickfont=dict(size=15, color='#333')
                ),
                yaxis=dict(
                    title="", 
                    autorange="reversed",
                    tickfont=dict(size=16, color='#333', family='Arial')
                ),
                plot_bgcolor='#F8F9FA',
                paper_bgcolor='white',
                font=dict(size=14, color='#333'),
                bargap=0.15
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Recomendaciones con colores dinámicos según categoría
            st.markdown("#### 💡 Recomendaciones Personalizadas")
            
            # Definir colores de fondo según el riesgo
            color_fondo_map = {
                'BAJO': 'linear-gradient(135deg, #D4EDDA 0%, #C3E6CB 100%)',
                'MODERADO': 'linear-gradient(135deg, #FFF3CD 0%, #FFE5A0 100%)',
                'ALTO': 'linear-gradient(135deg, #FFE5CC 0%, #FFD699 100%)',
                'CRÍTICO': 'linear-gradient(135deg, #F8D7DA 0%, #F5C6CB 100%)'
            }
            
            color_borde_map = {
                'BAJO': '#28A745',
                'MODERADO': '#FFC107',
                'ALTO': '#FF9800',
                'CRÍTICO': '#DC3545'
            }
            
            color_texto_map = {
                'BAJO': '#155724',
                'MODERADO': '#856404',
                'ALTO': '#8B4000',
                'CRÍTICO': '#721C24'
            }
            
            nivel_riesgo = info_categoria['riesgo']
            fondo = color_fondo_map.get(nivel_riesgo, color_fondo_map['BAJO'])
            borde = color_borde_map.get(nivel_riesgo, color_borde_map['BAJO'])
            texto = color_texto_map.get(nivel_riesgo, color_texto_map['BAJO'])
            
            for i, rec in enumerate(info_categoria['recomendaciones'], 1):
                st.markdown(f"""
                    <div style='
                        background: {fondo};
                        padding: 18px;
                        border-radius: 12px;
                        margin: 14px 0;
                        border-left: 6px solid {borde};
                        box-shadow: 0 3px 6px rgba(0,0,0,0.08);
                        font-size: 17px;
                        color: {texto};
                        font-weight: 500;
                        line-height: 1.5;
                    '>
                        <strong style="font-size: 19px; color: {texto};">🔹 {i}.</strong> {rec}
                    </div>
                """, unsafe_allow_html=True)
            
            # Botones de acción
            st.markdown("<br>", unsafe_allow_html=True)
            col_btn1, col_btn2, col_btn3 = st.columns(3)
            
            with col_btn1:
                if st.button("📥 Guardar", use_container_width=True, key="save_result"):
                    if not os.path.exists('data'):
                        os.makedirs('data')
                    df_input['nombre'] = st.session_state.data['nombre']
                    df_input['prediccion'] = label
                    df_input['fecha'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    df_input.to_csv('data/historico.csv', mode='a', index=False, 
                                  header=not os.path.exists('data/historico.csv'))
                    st.success("✅ Guardado")
            
            with col_btn2:
                if st.button("⬅️ Modificar", use_container_width=True, key="back_step"):
                    st.session_state.step = 3
                    if hasattr(st, 'rerun'):
                        st.rerun()
                    else:
                        st.experimental_rerun()
            
            with col_btn3:
                if st.button("🔄 Nuevo", use_container_width=True, key="new_consult"):
                    reset_app()
            
            # Advertencia médica compacta
            st.markdown("""
                <div class='warning-box' style='font-size: 12px; padding: 12px;'>
                    <strong>⚕️ Importante:</strong> Diagnóstico orientativo. Consulta con un profesional de la salud.
                </div>
            """, unsafe_allow_html=True)
            
        except Exception as e:
            st.error(f"❌ Error: {e}")
    
    else:
        # MOSTRAR FORMULARIO (pasos 0-3)
        with st.container():
            # PASO 0: Presentación
            if st.session_state.step == 0:
                st.markdown("### 👤 ¡Empecemos!")
                st.markdown("""
                <p style='
                    font-size:25px;
                    font-weight:600;
                    margin-bottom:-50px;
                    margin-top:20px;
                '>
                Tu nombre
                </p>
                """, unsafe_allow_html=True)
                nombre = st.text_input("", value=st.session_state.data.get('nombre', ''), key="nombre_input", placeholder="Escribe tu nombre aquí...")
                
                st.markdown("""
                <p style='
                    font-size:25px;
                    font-weight:600;
                    margin-bottom:-50px;
                    margin-top:20px;
                '>
                Género
                </p>
                """, unsafe_allow_html=True)
                genero = st.selectbox("", ["Femenino", "Masculino"], key="genero_input")
                if st.button("Comenzar Evaluación 🚀", use_container_width=True):
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
                st.markdown(f"### 📏 Medidas de {st.session_state.data.get('nombre', 'Usuario')}")
                st.markdown("""
                <p style='
                    font-size:25px;
                    font-weight:600;
                    margin-bottom:-50px;
                    margin-top:20px;
                '>
                Edad
                </p>
                """, unsafe_allow_html=True)
                edad = st.number_input("", min_value=10, max_value=100, value=st.session_state.data.get('age', 25), key="edad_input")
                st.markdown("""
                <p style='
                    font-size:25px;
                    font-weight:600;
                    margin-bottom:-50px;
                    margin-top:20px;
                '>
                Altura (m)
                </p>
                """, unsafe_allow_html=True)
                altura = st.number_input("", min_value=1.20, max_value=2.30, value=st.session_state.data.get('height', 1.70), step=0.01, key="altura_input")
                st.markdown("""
                <p style='
                    font-size:25px;
                    font-weight:600;
                    margin-bottom:-50px;
                    margin-top:20px;
                '>
                Peso (kg)
                </p>
                """, unsafe_allow_html=True)
                peso = st.number_input("", min_value=30.0, max_value=200.0, value=st.session_state.data.get('weight', 70.0), step=0.1, key="peso_input")
                
                # Calcular y mostrar IMC
                if altura > 0:
                    imc = peso / (altura ** 2)
                    st.markdown(f"""
                        <div style='background-color: #E6F1FB; padding: 15px; border-radius: 8px; margin: 10px 0;'>
                            <p style='margin: 0; color: #0C447C; font-size: 14px;'>📊 Tu IMC</p>
                            <p style='margin: 5px 0 0 0; color: #185FA5; font-size: 28px; font-weight: bold;'>{imc:.2f}</p>
                        </div>
                    """, unsafe_allow_html=True)
                
                if st.button("Siguiente ➡️", use_container_width=True):
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
                st.markdown("### 🍽️ Tus Hábitos Alimenticios")
                
                fcvc_opciones = {
                    "Nunca": 1.0,
                    "Raramente": 1.5,
                    "A veces": 2.0,
                    "Frecuentemente": 2.5,
                    "Siempre": 3.0
                }
                st.markdown("""
                <p style='
                    font-size:25px;
                    font-weight:600;
                    margin-bottom:-50px;
                    margin-top:20px;
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
                    font-size:25px;
                    font-weight:600;
                    margin-bottom:-50px;
                    margin-top:20px;
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
                    font-size:25px;
                    font-weight:600;
                    margin-bottom:-50px;
                    margin-top:20px;
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
                    font-size:25px;
                    font-weight:600;
                    margin-bottom:-50px;
                    margin-top:20px;
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
                
                if st.button("Siguiente ➡️", use_container_width=True):
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
                st.markdown("### 💪 Tu Estilo de Vida")
                
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
                    font-size:25px;
                    font-weight:600;
                    margin-bottom:-50px;
                    margin-top:20px;
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
                    font-size:25px;
                    font-weight:600;
                    margin-bottom:-50px;
                    margin-top:20px;
                '>
                ¿Tienes antecedentes familiares de obesidad?
                </p>
                """, unsafe_allow_html=True)
                family = st.selectbox("", 
                                    ["No", "Sí"], key="family_input")
                st.markdown("""
                <p style='
                    font-size:25px;
                    font-weight:600;
                    margin-bottom:-50px;
                    margin-top:20px;
                '>
                ¿Fumas?
                </p>
                """, unsafe_allow_html=True)
                
                smoke = st.selectbox("", ["No", "Sí"], key="smoke_input")
                
                if st.button("Ver Mi Diagnóstico 🎯", use_container_width=True):
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
            <p class="avatar-text" style="font-size: 12px;">Paso {st.session_state.step + 1} de 5</p>
        </div>
    """, unsafe_allow_html=True)