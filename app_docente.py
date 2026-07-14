import streamlit as st
import anthropic
import json

st.set_page_config(
    page_title="Suite Digital Docente - Demo Comercial",
    page_icon="🏫",
    layout="wide"
)

# ==========================================
# ESTILOS PERSONALIZADOS
# ==========================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

:root {
    --primary: #0d9488;
    --primary-dark: #115e59;
    --accent: #f59e0b;
    --success: #10b981;
    --warning: #f59e0b;
    --danger: #ef4444;
    --info: #3b82f6;
    --card-bg: #ffffff;
    --text-main: #1e293b;
    --text-muted: #64748b;
    --border: #e2e8f0;
}

html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

.stApp { background: linear-gradient(180deg, #f0fdfa 0%, #eef2ff 100%); }

.app-header {
    background: linear-gradient(120deg, var(--primary) 0%, var(--primary-dark) 100%);
    padding: 1.75rem 2rem;
    border-radius: 16px;
    margin-bottom: 1rem;
    box-shadow: 0 10px 30px -12px rgba(13, 148, 136, 0.45);
}
.app-header h1 { color: #ffffff !important; font-weight: 800; font-size: 1.9rem; margin: 0; }
.app-header p { color: rgba(255,255,255,0.88) !important; font-size: 1rem; margin: 0.25rem 0 0 0; }

[data-testid="stSidebar"] { background: linear-gradient(180deg, #134e4a 0%, #0f766e 100%); }
[data-testid="stSidebar"] * { color: #f0fdfa !important; }
[data-testid="stSidebar"] input, [data-testid="stSidebar"] textarea {
    background: rgba(255,255,255,0.1) !important;
    color: #ffffff !important;
    border-radius: 8px !important;
    border: 1px solid rgba(255,255,255,0.25) !important;
}
[data-testid="stSidebar"] [data-testid="stAlert"] { background: rgba(255,255,255,0.1) !important; border-radius: 12px; }
[data-testid="stSidebar"] .stButton > button {
    background: rgba(255,255,255,0.12) !important;
    color: #ffffff !important;
    border: 1px solid rgba(255,255,255,0.35) !important;
}
[data-testid="stSidebar"] .stButton > button:hover { background: rgba(255,255,255,0.24) !important; }
[data-testid="stSidebar"] hr { border-color: rgba(255,255,255,0.25) !important; }

[data-testid="stForm"] {
    background: var(--card-bg);
    padding: 1.75rem 2rem;
    border-radius: 20px;
    border: 1px solid var(--border);
    box-shadow: 0 20px 45px -20px rgba(15, 23, 42, 0.25);
}

.stTabs [data-baseweb="tab-list"] { gap: 4px; background: #ffffff; padding: 6px; border-radius: 12px; border: 1px solid var(--border); }
.stTabs [data-baseweb="tab"] { border-radius: 8px; padding: 10px 18px; font-weight: 600; color: var(--text-muted); }
.stTabs [aria-selected="true"] { background: var(--primary) !important; color: #ffffff !important; }

.stButton > button, .stDownloadButton > button {
    border-radius: 10px;
    font-weight: 600;
    border: 1px solid var(--border);
    transition: all 0.15s ease;
}
.stButton > button[kind^="primary"], .stFormSubmitButton > button[kind^="primary"] {
    background: linear-gradient(120deg, var(--primary), var(--primary-dark)) !important;
    border: none !important;
    color: #ffffff !important;
}
.stButton > button:hover, .stDownloadButton > button:hover {
    transform: translateY(-1px);
    box-shadow: 0 8px 18px -8px rgba(13,148,136,0.5);
}

[data-testid="stAlert"] { border-radius: 12px; }
[data-testid="stImage"] img { border-radius: 16px; }

h2, h3 { color: var(--text-main); font-weight: 700; }
hr { border-color: var(--border) !important; }
</style>
""", unsafe_allow_html=True)

if "autenticado" not in st.session_state:
    st.session_state.autenticado = False

try:
    client = anthropic.Anthropic(api_key=st.secrets["ANTHROPIC_API_KEY"])
except Exception:
    client = None


MODELO_IA = "claude-sonnet-4-6"


def extraer_json(respuesta):
    """Extrae el objeto JSON del texto de la respuesta de Claude.
    Tolera que el modelo envuelva el JSON en texto o fences de markdown."""
    texto = next(b.text for b in respuesta.content if b.type == "text")
    inicio = texto.find("{")
    fin = texto.rfind("}")
    if inicio == -1 or fin == -1:
        raise ValueError("La respuesta no contiene un objeto JSON.")
    return json.loads(texto[inicio:fin + 1])

if not st.session_state.autenticado:
    col_l1, col_l2, col_l3 = st.columns([1, 1.5, 1])
    with col_l2:
        st.write("")
        st.markdown(
            """
            <div style='text-align:center; margin-bottom: 1rem;'>
                <div style='font-size:3rem; line-height:1;'>🏫</div>
                <h1 style='color:#115e59; font-weight:800; margin:0.3rem 0 0 0;'>Suite Digital Docente</h1>
                <p style='color:#64748b; font-size:1rem; margin-top:0.3rem;'>Gestión Pedagógica Avanzada con IA</p>
            </div>
            """,
            unsafe_allow_html=True
        )
        st.image("https://images.unsplash.com/photo-1577896851231-70ef18881754?q=80&w=500", width="stretch")
        with st.form("form_login"):
            st.markdown("### 🔐 Ingreso al Sistema (Demo de Ventas)")
            usuario = st.text_input("Correo Electrónico o Usuario:", value="demo@escuela.edu.ar")
            contrasena = st.text_input("Contraseña:", type="password", value="123456")
            st.caption("ℹ️ Podés ingresar con los datos por defecto para probar la experiencia de cliente.")
            boton_ingresar = st.form_submit_button("Iniciar Sesión Premium", type="primary", use_container_width=True)
            if boton_ingresar:
                st.session_state.autenticado = True
                st.rerun()
else:
    with st.sidebar:
        st.image("https://images.unsplash.com/photo-1577896851231-70ef18881754?q=80&w=300", caption="Licencia Premium Activa 2026")
        st.title("⚙️ Panel del Docente")
        st.markdown("### 👤 Usuario Activo")
        st.info("📍 Docente: Gerardo Sobrino\n🏫 Escuela: Escuela Primaria San Pedro\n🟢 Grado: 4° Grado - Turno Mañana")
        st.markdown("---")
        st.markdown("### 🧠 Configuración de IA")
        st.text_input("Motor de IA:", value=MODELO_IA, disabled=True)
        st.markdown("---")
        if st.button("🚪 Cerrar Sesión Demo", use_container_width=True):
            st.session_state.autenticado = False
            st.rerun()

    st.markdown(
        """
        <div class="app-header">
            <h1>🏫 Suite Digital de Automatización Docente</h1>
            <p>Herramientas de Inteligencia Artificial para el Aula Heterogénea</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    tab1, tab2, tab3, tab4 = st.tabs([
        "📝 Generador Pedagógico",
        "💬 Sintetizador de Actas",
        "📊 Registro de Rúbricas",
        "📅 Agenda de Alertas"
    ])

    with tab1:
        st.subheader("✒️ Planificación y Secuencias Didácticas Multinivel")
        st.write("Generá secuencias adaptadas a la heterogeneidad del aula alineadas al Diseño Curricular.")
        col_input, col_preview = st.columns([1, 1])
        with col_input:
            st.markdown("#### 📋 Parámetros de la Clase")
            area = st.selectbox("Área Curricular:", ["Prácticas del Lenguaje", "Matemática", "Ciencias Naturales", "Ciencias Sociales"])
            eje_tematico = st.text_input("Eje Temático / Contenido:", placeholder="Ej: Comprensión de textos narrativos (Mitos y Leyendas)")
            texto_soporte = st.text_area("Texto base o material didáctico (Raw Text):", placeholder="Pegá acá el cuento, el problema o el fragmento del manual...", height=180)
            ejecutar = st.button("Generar Material Académico", type="primary")
        with col_preview:
            st.markdown("#### 📄 Vista Previa del Material Adaptado")
            sub_tab_formal, sub_tab_inicial, sub_tab_medio, sub_tab_avanzado = st.tabs([
                "📋 Planificación", "🟢 Nivel Inicial (PPI)", "🔵 Nivel Medio", "🔴 Nivel Avanzado"
            ])
            if ejecutar:
                if not eje_tematico or not texto_soporte:
                    st.warning("⚠️ Por favor, completa el eje temático y el texto soporte.")
                elif client is None:
                    st.error("❌ Cliente de Anthropic no inicializado. Verifica las claves en Streamlit Cloud Secrets.")
                else:
                    with st.spinner("Claude analizando el Diseño Curricular..."):
                        try:
                            prompt_sistema = (
                                "Sos un asesor técnico-pedagógico experto de la Provincia de Buenos Aires, especializado en aulas heterogéneas de nivel primario. "
                                "Tu tarea es analizar el contenido y devolver una planificación académica completa con secuencias didácticas diferenciadas por nivel.\n\n"
                                "DEBES RESPONDER ESTRICTAMENTE EN FORMATO JSON, con la siguiente estructura de claves:\n"
                                "{\n"
                                "  \"planificacion\": \"Fundamentación formal alineada al Diseño Curricular bonaerense. Incluir: objetivos de aprendizaje, contenidos, criterios de evaluación y tiempo estimado.\",\n"
                                "  \"nivel_inicial\": \"Secuencia para alumnos con PPI o dificultades. Incluir: consignas simplificadas paso a paso, actividades concretas y manipulativas, preguntas guía con respuesta orientada, y una actividad de cierre accesible.\",\n"
                                "  \"nivel_medio\": \"Secuencia estándar para el grado. Incluir: actividades de exploración del texto, consignas de comprensión lectora o resolución de problemas, actividad de producción individual, y preguntas de reflexión.\",\n"
                                "  \"nivel_avanzado\": \"Secuencia para alumnos destacados. Incluir: actividades de análisis crítico, producción escrita compleja o resolución de problemas con múltiples pasos, consigna de investigación o creación original, y pregunta de pensamiento divergente.\"\n"
                                "}\n\n"
                                "Cada nivel debe tener al menos 3 actividades concretas y diferenciadas entre sí. Usá lenguaje claro y didáctico."
                            )
                            respuesta = client.messages.create(
                                model=MODELO_IA,
                                max_tokens=8192,
                                temperature=0.3,
                                system=prompt_sistema,
                                messages=[
                                    {"role": "user", "content": f"Área Curricular: {area}\nEje Temático: {eje_tematico}\nTexto base:\n{texto_soporte}"}
                                ],
                            )
                            respuesta_json = extraer_json(respuesta)
                            plan_txt = respuesta_json.get("planificacion", "")
                            ini_txt = respuesta_json.get("nivel_inicial", "")
                            med_txt = respuesta_json.get("nivel_medio", "")
                            av_txt = respuesta_json.get("nivel_avanzado", "")
                            with sub_tab_formal:
                                st.write(plan_txt)
                            with sub_tab_inicial:
                                st.write(ini_txt)
                            with sub_tab_medio:
                                st.write(med_txt)
                            with sub_tab_avanzado:
                                st.write(av_txt)
                            documento_completo = f"=== PLANIFICACIÓN FORMAL ===\n{plan_txt}\n\n=== SECUENCIA ADAPTADA: NIVEL INICIAL (PPI) ===\n{ini_txt}\n\n=== SECUENCIA ADAPTADA: NIVEL MEDIO ===\n{med_txt}\n\n=== SECUENCIA ADAPTADA: NIVEL AVANZADO ===\n{av_txt}"
                            st.markdown("---")
                            st.download_button(
                                label="📥 Descargar Planificación Completa (.txt)",
                                data=documento_completo,
                                file_name=f"Planificacion_{eje_tematico.replace(' ', '_')}.txt",
                                mime="text/plain"
                            )
                            st.success("✨ ¡Material multinivel generado con éxito!")
                        except Exception as e:
                            st.error(f"Error: {str(e)}")
            else:
                with sub_tab_formal: st.info("Esperando generación...")
                with sub_tab_inicial: st.info("Esperando generación...")
                with sub_tab_medio: st.info("Esperando generación...")
                with sub_tab_avanzado: st.info("Esperando generación...")

    with tab2:
        st.subheader("💬 Procesador de Reuniones y Notas al Cuaderno")
        st.write("Pegá los apuntes de una reunión con un padre o un mensaje de WhatsApp para estructurarlo formalmente.")
        col_acta_in, col_acta_out = st.columns([1, 1])
        with col_acta_in:
            texto_crudo = st.text_area("Notas rápidas o mensaje crudo:", placeholder="Vino la mamá de...", height=180)
            procesar_acta = st.button("Sintetizar y Formalizar", type="primary")
        with col_acta_out:
            st.markdown("#### 📄 Información Estructurada")
            if procesar_acta:
                if not texto_crudo:
                    st.warning("⚠️ Por favor, ingresá algún texto.")
                elif client is None:
                    st.error("❌ Cliente de Anthropic no inicializado.")
                else:
                    with st.spinner("Claude formalizando el texto..."):
                        try:
                            prompt_sistema_acta = (
                                "Sos un asistente administrativo escolar experto. Procesá el texto informal "
                                "y devolvé un objeto JSON con claves: alumno, adulto, categoria, compromiso, nota_formal."
                            )
                            respuesta_acta = client.messages.create(
                                model=MODELO_IA,
                                max_tokens=4096,
                                temperature=0.1,
                                system=prompt_sistema_acta,
                                messages=[
                                    {"role": "user", "content": texto_crudo}
                                ],
                            )
                            res_acta = extraer_json(respuesta_acta)
                            st.text_input("👦 Alumno:", value=res_acta.get("alumno", ""))
                            st.text_input("👤 Adulto Responsable:", value=res_acta.get("adulto", ""))
                            st.text_input("🏷️ Categoría:", value=res_acta.get("categoria", ""))
                            st.text_area("🤝 Compromiso Asumido:", value=res_acta.get("compromiso", ""), height=70)
                            st.markdown("---")
                            st.markdown("### 📝 Nota Formal sugerida:")
                            nota = res_acta.get("nota_formal", "")
                            st.info(nota)
                            st.download_button(
                                label="📥 Descargar Nota Formal (.txt)",
                                data=f"ACTA INSTITUCIONAL\nAlumno: {res_acta.get('alumno','')}\nResponsable: {res_acta.get('adulto','')}\n\n{nota}",
                                file_name=f"Acta_{res_acta.get('alumno','').replace(' ', '_')}.txt",
                                mime="text/plain"
                            )
                        except Exception as e:
                            st.error(f"Error: {str(e)}")
            else:
                st.info("Esperando datos para procesar...")

    with tab3:
        st.subheader("📊 Tracker de Progreso y Generación de Rúbricas")
        st.write("Ingresá el contenido o capacidad que querés evaluar para diseñar los descriptores de desempeño multinivel.")
        col_rub_in, col_rub_out = st.columns([1, 1])
        with col_rub_in:
            criterio_eval = st.text_input("Criterio / Capacidad a evaluar:", placeholder="Ej: Uso de mayúsculas y puntos...")
            generar_rubrica = st.button("Diseñar Matriz de Rúbricas", type="primary")
        with col_rub_out:
            st.markdown("#### 📋 Matriz de Desempeño Generada")
            if generar_rubrica:
                if not criterio_eval:
                    st.warning("⚠️ Por favor, ingresá un criterio para evaluar.")
                elif client is None:
                    st.error("❌ Cliente de Anthropic no inicializado.")
                else:
                    with st.spinner("Claude construyendo la matriz pedagógica..."):
                        try:
                            prompt_sistema_rubrica = (
                                "Sos un especialista en evaluación educativa. Devolvé un objeto JSON con las claves "
                                "\"en_proceso\", \"satisfactorio_basico\", \"alcanzado\" y \"avanzado\" con descriptores detallados."
                            )
                            respuesta_rubrica = client.messages.create(
                                model=MODELO_IA,
                                max_tokens=4096,
                                temperature=0.3,
                                system=prompt_sistema_rubrica,
                                messages=[
                                    {"role": "user", "content": criterio_eval}
                                ],
                            )
                            res_rub = extraer_json(respuesta_rubrica)
                            st.error(f"🔴 **En Proceso / Inicial:**\n\n{res_rub.get('en_proceso', '')}")
                            st.warning(f"🟡 **Básico / En Camino:**\n\n{res_rub.get('satisfactorio_basico', '')}")
                            st.success(f"🟢 **Alcanzado / Esperado:**\n\n{res_rub.get('alcanzado', '')}")
                            st.info(f"🔵 **Avanzado / Destacado:**\n\n{res_rub.get('avanzado', '')}")
                        except Exception as e:
                            st.error(f"Error: {str(e)}")
            else:
                st.info("Esperando definición de criterio...")

    with tab4:
        st.subheader("📅 Panel de Alertas Tempranas y Seguimiento de Alumnos")
        st.write("Evaluá situaciones críticas de vulnerabilidad educativa o necesidades de inclusión pedagógica (PPI).")
        col_al_in, col_al_out = st.columns([1, 1])
        with col_al_in:
            observacion_alumno = st.text_area("Observaciones del comportamiento o trayectoria del estudiante:", placeholder="Ej: Faltó 12 días seguidos...", height=150)
            evaluar_alerta = st.button("Evaluar Alerta Temprana", type="primary")
        with col_al_out:
            st.markdown("#### 🚨 Diagnóstico de Trayectoria")
            if evaluar_alerta:
                if not observacion_alumno:
                    st.warning("⚠️ Por favor, ingresá la observación del alumno.")
                elif client is None:
                    st.error("❌ Cliente de Anthropic no inicializado.")
                else:
                    with st.spinner("Claude analizando indicadores de riesgo escolar..."):
                        try:
                            prompt_sistema_alerta = (
                                "Sos un orientador de la Provincia de Buenos Aires. Analizá y devolvé un JSON estricto "
                                "con las claves: nivel_riesgo, requiere_ppi, analisis_situacion, pasos_a_seguir."
                            )
                            respuesta_alerta = client.messages.create(
                                model=MODELO_IA,
                                max_tokens=4096,
                                temperature=0.1,
                                system=prompt_sistema_alerta,
                                messages=[
                                    {"role": "user", "content": observacion_alumno}
                                ],
                            )
                            res_alerta = extraer_json(respuesta_alerta)
                            riesgo = res_alerta.get("nivel_riesgo", "Bajo")
                            if riesgo == "Alto":
                                st.error(f"🚨 **Nivel de Riesgo Escolar:** {riesgo}")
                            elif riesgo == "Medio":
                                st.warning(f"⚠️ **Nivel de Riesgo Escolar:** {riesgo}")
                            else:
                                st.success(f"🟢 **Nivel de Riesgo Escolar:** {riesgo}")
                            st.text_input("📋 Requiere Configuración PPI / Inclusión:", value=res_alerta.get("requiere_ppi", ""))
                            st.text_area("🧠 Análisis del Factor de Riesgo:", value=res_alerta.get("analisis_situacion", ""), height=80)
                            st.markdown("---")
                            st.markdown("### 📋 Protocolo de Acción Institucional:")
                            st.write(res_alerta.get("pasos_a_seguir", ""))
                        except Exception as e:
                            st.error(f"Error: {str(e)}")
            else:
                st.info("Esperando carga de observaciones...")