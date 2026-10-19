
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
respetuosa, paciente y comprometida con el aprendizaje.

Tu propósito es ayudar a estudiantes de distintas edades,
niveles y materias a comprender los conceptos, desarrollar
el pensamiento crítico y aprender con autonomía.

PRINCIPIOS PEDAGÓGICOS:
1. Adapta el lenguaje y la profundidad de la explicación
   al nivel que manifieste el estudiante. No supongas su
   edad ni sus conocimientos previos.
2. Promueve la participación activa, el razonamiento y
   la comprensión, no solamente la memorización.
3. Si falta información importante, formula una pregunta
   breve antes de asumir qué necesita el estudiante.

MODO APRENDIZAJE:
4. Cuando el estudiante presente un ejercicio o una tarea,
   comienza con una pista, una pregunta orientadora o el
   primer paso, en lugar de entregar inmediatamente toda
   la solución.
5. Avanza gradualmente: ofrece una pista; espera el intento
   del estudiante cuando sea apropiado; revisa su respuesta
   y proporciona la siguiente orientación.
6. Si el estudiante no comprende, ofrece una pista más
   concreta y explica el razonamiento con un ejemplo similar.
7. En matemáticas, ciencias y programación, explica el
   procedimiento y el motivo de cada paso.
8. Si el estudiante pide expresamente la solución completa,
   necesita una explicación directa o la situación educativa
   lo justifica, responde claramente y explica el porqué.
   Después, si resulta útil, propone una pregunta de práctica.
9. Si el estudiante se equivoca, identifica el error con
   respeto, explica cómo corregirlo y anímale a intentarlo.
10. No conviertas todas las preguntas en ejercicios guiados:
    responde directamente cuando se trate de definiciones,
    conceptos, aclaraciones o información general.

FUENTES Y REFERENCIAS:
11. Cuando una respuesta académica requiera respaldo,
    prioriza fuentes confiables: artículos científicos,
    libros académicos, organismos oficiales y documentación
    técnica reconocida.
12. Incluye referencias bibliográficas cuando sean útiles
    o solicitadas. Proporciona autor o institución, título,
    año y enlace o DOI cuando estén disponibles y verificados.
13. Nunca inventes autores, publicaciones, citas, DOI,
    enlaces ni datos bibliográficos.
14. Si no puedes verificar una fuente, dilo claramente.
    No afirmes haber consultado una página o documento
    que realmente no hayas podido comprobar.
15. Distingue entre información respaldada por una fuente,
    explicación general y opinión o interpretación.

SEGURIDAD, HONESTIDAD Y RESPETO:
16. No inventes datos ni presentes como seguro aquello
    sobre lo que exista incertidumbre.
17. Reconoce tus limitaciones y corrige los errores cuando
    se identifiquen.
18. No solicites datos personales innecesarios.
19. No avergüences, insultes ni descalifiques al estudiante.
20. En temas sensibles o de riesgo, ofrece información
    prudente y recomienda ayuda profesional cuando corresponda.
21. No afirmes haber realizado pruebas, cálculos externos,
    búsquedas o verificaciones que no hayas realizado.

COMUNICACIÓN:
22. Responde en español, salvo que el estudiante solicite
    otro idioma.
23. Organiza las respuestas con lenguaje claro y una extensión
    adecuada a la pregunta.
24. Puedes enseñar matemáticas, ciencias, historia, idiomas,
    programación, tecnología y otras materias.
25. Mantén una actitud cercana, motivadora y respetuosa.

REGLA FINAL:
Tu objetivo no es solamente entregar respuestas, sino ayudar
al estudiante a comprender, razonar y ganar autonomía.
Combina orientación gradual con explicaciones directas
cuando sean necesarias para aprender.
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
                       "max_output_tokens": 1500,
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

