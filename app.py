
import streamlit as st
from google import genai

st.set_page_config(
    page_title="ChatbotJESS | Asistente Educativo",
    page_icon="🤖",
    layout="centered",
    initial_sidebar_state="expanded",
)

# ---------- CONTRATO PEDAGÓGICO ----------
INSTRUCCIONES_JESS = """
Eres ChatbotJESS, una tutora virtual educativa, amable,
respetuosa y paciente, capaz de ayudar con cualquier materia.

Tu objetivo es promover el aprendizaje y la autonomía.

REGLAS PEDAGÓGICAS:
1. Explica los conceptos con claridad y adapta el lenguaje
   al nivel que manifieste el estudiante.
2. Anima al estudiante a razonar y participar activamente.
3. Cuando sea apropiado, ofrece pistas antes de mostrar
   la solución completa.
4. Si el estudiante se equivoca, explica el error con
   respeto y ayúdale a intentarlo de nuevo.
5. En ejercicios escolares, guía el procedimiento paso
   a paso y procura que el estudiante comprenda el porqué.
6. Si solicita una explicación directa, responde claramente
   y después ofrece un ejemplo o una pregunta de práctica.
7. No inventes datos. Reconoce las dudas y limitaciones.
8. No afirmes haber comprobado información que no verificaste.
9. No solicites datos personales innecesarios.
10. No avergüences ni descalifiques al estudiante.
11. Responde en español, salvo que solicite otro idioma.
12. Mantén las respuestas organizadas y adecuadas a la pregunta.

No asumas la edad ni el nivel académico si no se conocen.
Puedes enseñar ciencias, matemáticas, historia, idiomas,
programación, tecnología y otras materias.
"""



# ---------- DISEÑO EDUCATIVO ----------
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(
            180deg, #edf4ff 0%, #ffffff 75%
        );
    }

    .main .block-container {
        max-width: 950px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    h1, h2, h3 {
        color: #1e3a68;
    }

    .hero {
        background: linear-gradient(
            135deg, #244b8f, #6489d8
        );
        padding: 28px 24px;
        border-radius: 22px;
        color: white;
        margin-bottom: 22px;
        box-shadow: 0 8px 24px rgba(36, 75, 143, 0.16);
    }

    .hero h1 {
        color: white;
        margin-bottom: 8px;
    }

    .hero p {
        color: #edf4ff;
        margin-bottom: 0;
    }

    .info-card {
        background: white;
        border: 1px solid #e1e9f7;
        border-radius: 16px;
        padding: 18px;
        margin-bottom: 16px;
        box-shadow: 0 3px 12px rgba(40, 70, 120, 0.05);
    }

    .status {
        color: #2457a7;
        font-weight: 600;
    }

    div[data-testid="stChatMessage"] {
        border: 1px solid #e1e9f7;
        border-radius: 16px;
        padding: 12px;
        margin-bottom: 12px;
    }

    section[data-testid="stSidebar"] {
        background: #edf3ff;
    }
</style>
""", unsafe_allow_html=True)


# ---------- ESTILOS ----------
st.markdown(
    """
    <style>
    .stApp {
        background-color: #F5F7FB;
    }
    .main .block-container {
        max-width: 900px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }
    .hero {
        background: linear-gradient(135deg, #173B67, #3976B8);
        padding: 2rem;
        border-radius: 20px;
        color: white;
        margin-bottom: 1.5rem;
    }
    .hero h1 {
        color: white;
        font-size: 2.2rem;
        margin-bottom: 0.4rem;
    }
    .hero p {
        color: #EAF2FF;
        font-size: 1rem;
        margin-bottom: 0;
    }
    .info-card {
        background: white;
        padding: 1rem 1.2rem;
        border: 1px solid #E1E8F0;
        border-radius: 14px;
        margin-bottom: 1rem;
    }
    .status {
        color: #2457A7;
        font-weight: 600;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------- HISTORIAL ----------
if "mensajes" not in st.session_state:
    st.session_state.mensajes = []

# ---------- BARRA LATERAL ----------
with st.sidebar:
    st.image("jess_avatar.png", width=200)

    st.markdown("## 🤖 ChatbotJESS")
    st.caption("Tu tutora educativa: inteligente y cercana.")

    st.divider()
    st.markdown("### 📚 Áreas de aprendizaje")
    st.write("🐍 Programación y tecnología")
    st.write("➗ Matemáticas")
    st.write("🔬 Ciencias")
    st.write("🌎 Historia y cultura")
    st.write("🇬🇧 Idiomas")
    st.write("📖 Otras materias")

    st.divider()
    st.markdown("### 🛡️ Uso responsable")
    st.caption(
        "No compartas contraseñas, datos personales "
        "ni información privada en el chat."
    )

    if st.button("🗑️ Limpiar conversación",
                 use_container_width=True):
        st.session_state.mensajes = []
        st.rerun()


# ---------- ENCABEZADO ----------
col_avatar, col_titulo = st.columns(
    [1, 3],
    vertical_alignment="center"
)

with col_avatar:
    st.image("jess_avatar.png", width=125)

with col_titulo:
    st.markdown(
        """
        <div class="hero">
            <h1>🤖 ChatbotJESS</h1>
            <p>
                Tu compañera de aprendizaje.
                Aprende, practica y descubre algo nuevo cada día.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown(
    """
    <div class="info-card">
        <span class="status">● Tutora educativa</span>
        <p>
            JESS te ayudará a comprender los temas,
            razonar, practicar y aprender de tus errores.
            Recuerda que sus respuestas pueden contener errores.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)


# ---------- MATERIAS ----------
st.markdown("### 📚 ¿Qué quieres aprender hoy?")
st.caption("Selecciona una materia para comenzar.")

if "materia" not in st.session_state:
    st.session_state.materia = ""

col1, col2 = st.columns(2)

with col1:
    if st.button("🐍 Programación y tecnología", use_container_width=True):
        st.session_state.materia = "Programación y tecnología"

    if st.button("➗ Matemáticas", use_container_width=True):
        st.session_state.materia = "Matemáticas"

    if st.button("🔬 Ciencias", use_container_width=True):
        st.session_state.materia = "Ciencias"

with col2:
    if st.button("🌎 Historia y cultura", use_container_width=True):
        st.session_state.materia = "Historia y cultura"

    if st.button("🇬🇧 Idiomas", use_container_width=True):
        st.session_state.materia = "Idiomas"

    if st.button("📖 Otras materias", use_container_width=True):
        st.session_state.materia = "Otras materias"

if st.session_state.materia:
    st.info(
        f"Materia seleccionada: {st.session_state.materia}. "
        "¡Escribe tu pregunta en el chat de abajo!"
    )

# ---------- MODO DE APRENDIZAJE ----------

st.divider()
st.markdown("## 🎓 Modo de aprendizaje")
st.caption("Elige cómo quieres que JESS te ayude a aprender.")

if "modo_aprendizaje" not in st.session_state:
    st.session_state.modo_aprendizaje = "Explicación paso a paso"

modo = st.radio(
    "¿Cómo quieres aprender hoy?",
    [
        "Explicación paso a paso",
        "Ejemplos prácticos",
        "Ayuda con mi tarea"
    ],
    horizontal=False,
    key="modo_aprendizaje"
)

if modo == "Explicación paso a paso":
    st.info("📚 JESS explicará el tema desde lo más básico.")
elif modo == "Ejemplos prácticos":
    st.info("💡 JESS utilizará ejemplos para ayudarte a comprender.")
else:
    st.info("✍️ JESS te guiará para resolver tu tarea y entenderla.")

# ---------- MOSTRAR HISTORIAL ----------
for mensaje in st.session_state.mensajes[-6:]:
    with st.chat_message(mensaje["role"]):
        st.markdown(mensaje["content"])


# ---------- CHAT CON IA ----------
pregunta = st.chat_input("¿Qué te gustaría aprender hoy?")

if pregunta:
    st.session_state.mensajes.append(
        {"role": "user", "content": pregunta}
    )

    with st.chat_message("user"):
        st.markdown(pregunta)

    with st.chat_message("assistant"):
        try:
            cliente = genai.Client(
                api_key=st.secrets["GEMINI_API_KEY"]
            )

            
            # Convertir el historial de la conversación en texto.
            historial_texto = "\n\n".join(
                (
                    "Estudiante: "
                    if mensaje["role"] == "user"
                    else "JESS: "
                ) + mensaje["content"]
                for mensaje in st.session_state.mensajes
            )

            with st.spinner("JESS está preparando tu explicación..."):
                resultado = cliente.interactions.create(
                    model="gemini-3.5-flash-lite",
                    input=(
    "Materia seleccionada: "
    + (st.session_state.get("materia", "") or "Ninguna")
    + "\n\nConversación:\n"
    + historial_texto
),
                    

system_instruction=(
    INSTRUCCIONES_JESS
    + "\n\nMATERIA SELECCIONADA: "
    + (st.session_state.get("materia", "") or "Ninguna")
    + "\n\nMODO DE APRENDIZAJE: "
    + st.session_state.get(
        "modo_aprendizaje",
        "Explicación paso a paso"
    )
    + "\n\nAdapta tu respuesta al modo elegido por el estudiante:"
    + "\n- Explicación paso a paso: explica desde lo básico, "
      "con lenguaje sencillo y ordenado."
    + "\n- Ejemplos prácticos: enseña mediante ejemplos claros "
      "y relacionados con la materia."
    + "\n- Ayuda con mi tarea: guía al estudiante paso a paso, "
      "haz preguntas cuando sea útil y ayúdalo a comprender "
      "el procedimiento, sin limitarte a darle la respuesta."
    + "\nMantén siempre un tono amable, paciente y educativo."
),


                    generation_config={
                        "thinking_level": "low",
                        "max_output_tokens": 800,
                    },
                )

            respuesta = resultado.output_text or (
                "No pude generar una respuesta esta vez. "
                "Inténtalo de nuevo, por favor."
            )

        except Exception as error:
            print(f"Error de Gemini en ChatbotJESS: {error}")
            respuesta = (
                "No pude conectarme con Gemini. "
                "Revisa el error que aparece en la Terminal "
                "para que podamos solucionarlo."
            )

        st.markdown(respuesta)

    st.session_state.mensajes.append({
        "role": "assistant",
        "content": respuesta,
    })

# ---------- PIE DE PÁGINA ----------
st.divider()
st.caption(
    "ChatbotJESS · Tutora educativa · "
    "Aprendizaje responsable y autónomo."
)

