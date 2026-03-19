import streamlit as st
import pandas as pd
import joblib
import os
from datetime import datetime

# --- CONFIGURACIÓN ---
st.set_page_config(page_title="HealthCheck AI", page_icon="⚖️", layout="centered")

# Estilo profesional
st.markdown("""
    <style>
    .stApp { background-color: #f8fafc; }
    .chat-bubble { background: white; padding: 25px; border-radius: 15px; border: 1px solid #e2e8f0; margin-bottom: 20px; }
    .stButton>button { background-color: #059669; color: white; border-radius: 10px; height: 3em; width: 100%; border: none; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

@st.cache_resource
def load_assets():
    path = 'models/modelo_obesidad_final_g.pkl'
    return joblib.load(path) if os.path.exists(path) else None

assets = load_assets()

if 'step' not in st.session_state:
    st.session_state.step = 0
if 'data' not in st.session_state:
    st.session_state.data = {}

def next_step(): 
    st.session_state.step += 1
    # Compatible con versiones viejas y nuevas
    if hasattr(st, 'rerun'): st.rerun()
    else: st.experimental_rerun()

# --- FLUJO DEL CHATBOT ---
st.title("⚖️ Asistente Nutricional")

with st.container():
    st.markdown('<div class="chat-bubble">', unsafe_allow_html=True)
    
    if st.session_state.step == 0:
        st.subheader("¡Hola! Soy tu asistente. ¿Cómo te llamas?")
        st.session_state.data['nombre'] = st.text_input("Nombre", "Usuario")
        st.session_state.data['gender'] = st.selectbox("Género", ["Female", "Male"])
        if st.button("Empezar"): next_step()

    elif st.session_state.step == 1:
        st.markdown(f"**{st.session_state.data['nombre']}**, dime tus medidas:")
        st.session_state.data['age'] = st.number_input("Edad", 1, 100, 25)
        st.session_state.data['height'] = st.number_input("Altura (m)", 1.20, 2.30, 1.70)
        st.session_state.data['weight'] = st.number_input("Peso (kg)", 30.0, 200.0, 75.0)
        if st.button("Siguiente"): 
            # IMC obligatorio para tu modelo
            st.session_state.data['imc'] = st.session_state.data['weight'] / (st.session_state.data['height']**2)
            next_step()

    elif st.session_state.step == 2:
        st.markdown("Háblame de tus hábitos:")
        st.session_state.data['fcvc'] = st.slider("Consumo vegetales (1-3)", 1.0, 3.0, 2.0)
        st.session_state.data['ncp'] = st.slider("Comidas al día", 1.0, 4.0, 3.0)
        st.session_state.data['faf'] = st.slider("Actividad física", 0.0, 3.0, 1.0)
        st.session_state.data['ch2o'] = st.slider("Agua (Litros)", 1.0, 3.0, 2.0)
        if st.button("Siguiente"): next_step()

    elif st.session_state.step == 3:
        st.markdown("Casi terminamos:")
        st.session_state.data['family_history'] = st.selectbox("Antecedentes familiares", ["yes", "no"])
        st.session_state.data['favc'] = st.selectbox("Comida calórica frecuente", ["yes", "no"])
        st.session_state.data['smoke'] = st.selectbox("¿Fumas?", ["no", "yes"])
        if st.button("Ver Resultado"): next_step()

    elif st.session_state.step == 4:
        # CONSTRUCCIÓN DE LAS 17 COLUMNAS (Minúsculas)
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
            pred = assets['pipeline'].predict(df_input)
            label = assets['label_encoder'].inverse_transform(pred)[0]
            
            st.success(f"### Diagnóstico: {label.replace('_', ' ')}")
            
            # Guardar en CSV
            if not os.path.exists('data'): os.makedirs('data')
            df_input['nombre'] = st.session_state.data['nombre']
            df_input['prediccion'] = label
            df_input.to_csv('data/historico.csv', mode='a', index=False, header=not os.path.exists('data/historico.csv'))
            
            st.markdown("---") # Reemplazo de st.divider()
            st.write("¿Es correcta la predicción?")
            if st.button("Confirmar Resultado"):
                st.balloons()
            
            if st.button("Nueva Consulta"):
                st.session_state.step = 0
                if hasattr(st, 'rerun'): st.rerun()
                else: st.experimental_rerun()
                
        except Exception as e:
            st.error(f"Error técnico: {e}")

    st.markdown('</div>', unsafe_allow_html=True)