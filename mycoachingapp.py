import streamlit as st
import openai
import os

# Configura tu clave de API de OpenAI usando variables de entorno
openai.api_key = os.getenv("OPENAI_API_KEY")

if not openai.api_key:
    st.error("No se encontró la API Key. Por favor, configura la variable de entorno 'OPENAI_API_KEY' con tu clave API de OpenAI.")

# Función para generar un plan personalizado
def generar_plan_personalizado(nombre, coaching, areas):
    prompt = f"Soy un coach experto. Un usuario llamado {nombre} ha seleccionado el coaching de tipo '{coaching}' y desea trabajar en las siguientes áreas: {', '.join(areas)}. Diseña un plan personalizado con dos secciones: una estrategia general y un trabajo práctico para cada área, incorporando el nombre del usuario."
    try:
        respuesta = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Eres un coach experto que ayuda a las personas a desarrollar planes personalizados."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=700,
            temperature=0.7
        )
        return respuesta['choices'][0]['message']['content'].strip()
    except Exception as e:
        st.error(f"Error al generar el plan: {e}")
        return None

# Configuración de la app
if "step" not in st.session_state:
    st.session_state.step = 1
if "name" not in st.session_state:
    st.session_state.name = ""
if "coaching" not in st.session_state:
    st.session_state.coaching = ""
if "areas" not in st.session_state:
    st.session_state.areas = []

# Paso 1: Introducción de nombre
if st.session_state.step == 1:
    st.title("¡Bienvenido a tu Asistente de Coaching!")
    st.header("Paso 1: Tu información personal")
    st.text_input("Escribe tu nombre completo:", key="name")
    if st.button("Siguiente"):
        if st.session_state.name:
            st.session_state.step = 2
        else:
            st.warning("Por favor, completa tu nombre.")

# Paso 2: Selección de coaching
if st.session_state.step == 2:
    st.title("Selecciona tu tipo de coaching")
    st.header("Paso 2: Tipo de Coaching")
    tipos_coaching = ["Coaching Personal", "Coaching Profesional", "Coaching de Salud", "Coaching Deportivo", "Coaching de Relaciones"]
    st.selectbox("Elige un tipo de coaching:", tipos_coaching, key="coaching")
    if st.button("Siguiente"):
        if st.session_state.coaching:
            st.session_state.step = 3
        else:
            st.warning("Por favor, selecciona un tipo de coaching.")
    if st.button("Atrás"):
        st.session_state.step = 1

# Paso 3: Selección de áreas de interés
if st.session_state.step == 3:
    st.title("Selecciona las áreas que deseas trabajar")
    st.header("Paso 3: Áreas de Interés")
    areas_disponibles = {
        "Coaching Personal": ["Gestión del estrés", "Autoestima", "Toma de decisiones"],
        "Coaching Profesional": ["Liderazgo", "Gestión del tiempo", "Trabajo en equipo"],
        "Coaching de Salud": ["Hábitos alimenticios", "Ejercicio", "Salud mental"],
        "Coaching Deportivo": ["Resistencia", "Técnica", "Mentalidad ganadora"],
        "Coaching de Relaciones": ["Comunicación", "Resolución de conflictos", "Empatía"]
    }
    st.multiselect("Elige las áreas que deseas trabajar:", areas_disponibles[st.session_state.coaching], key="areas")
    if st.button("Siguiente"):
        if st.session_state.areas:
            st.session_state.step = 4
        else:
            st.warning("Por favor, selecciona al menos un área de interés.")
    if st.button("Atrás"):
        st.session_state.step = 2

# Paso 4: Mostrar plan personalizado
if st.session_state.step == 4:
    st.title("Tu Plan de Trabajo Personalizado")
    st.header("Paso 4: Plan Personalizado")
    plan = generar_plan_personalizado(
        st.session_state.name,
        st.session_state.coaching,
        st.session_state.areas
    )
    if plan:
        st.write(plan)
    if st.button("Atrás"):
        st.session_state.step = 3

# Instrucciones para ejecutar la app
st.sidebar.title("Instrucciones")
st.sidebar.write("1. Asegúrate de tener Streamlit instalado: `pip install streamlit`.")
st.sidebar.write("2. Configura una variable de entorno 'OPENAI_API_KEY' con tu clave API de OpenAI.")
st.sidebar.write("3. Guarda este archivo como `app.py`.")
st.sidebar.write("4. Ejecuta el comando `streamlit run app.py` en tu terminal para iniciar la aplicación.")
