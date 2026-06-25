import streamlit as st
from groq import Groq
import json

# ==========================================
# CONFIGURACIÓN DE LA PÁGINA Y ESTILOS
# ==========================================
st.set_page_config(
    page_title="Suite Digital Docente - Demo Comercial",
    page_icon="🏫",
    layout="wide"
)

# Control de estado para el Login Simulado
if "autenticado" not in st.session_state:
    st.session_state.autenticado = False

# Inicializar cliente Groq con la API Key desde Secrets de Streamlit
try:
    client = Groq(api_key=st.secrets["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"])
except Exception:
    client = None

# ==========================================
# PANTALLA DE LOGIN SIMULADO (DEMO)
# ==========================================
if not st.session_state.autenticado:
    col_l1, col_l2, col_l3 = st.columns([1, 1.5, 1])
    
    with col_l2:
        st.write("")
        st.write("")
        st.markdown("<h1 style='text-align: center;'>🏫 Suite Digital Docente</h1>", unsafe_allow_html=True)
        st.markdown("<h4 style='text-align: center; color: gray;'>Gestión Pedagógica Avanzada con IA</h4>", unsafe_allow_html=True)
        
        st.image("https://images.unsplash.com/photo-1577896851231-70ef18881754?q=80&w=500", use_column_width=True)
        
        with st.form("form_login"):
            st.markdown("### 🔐 Ingreso al Sistema (Demo de Ventas)")
            usuario = st.text_input("Correo Electrónico o Usuario:", value="demo@escuela.edu.ar")
            contrasena = st.text_input("Contraseña:", type="password", value="123456")
            st.caption("ℹ️ Podés ingresar con los datos por defecto para probar la experiencia de cliente.")
            
            boton_ingresar = st.form_submit_button("Iniciar Sesión Premium", type="primary")
            
            if boton_ingresar:
                st.session_state.autenticado = True
                st.rerun()
else:
    # ==========================================
    # MENÚ LATERAL (SIDEBAR) - CONFIGURACIÓN
    # ==========================================
    with st.sidebar:
        st.image("https://images.unsplash.com/photo-1577896851231-70ef18881754?q=80&w=300", caption="Licencia Premium Activa 2026")
        st.title("⚙️ Panel del Docente")
        
        st.markdown("### 👤 Usuario Activo")
        st.info("📍 Docente: Gerardo Sobrino\n🏫 Escuela: Escuela Primaria San Pedro\n🟢 Grado: 4° Grado - Turno Mañana")
        
        st.markdown("---")
        st.markdown("### 🧠 Configuración de IA")
        modelo_complejo = "llama-3.3-70b-versatile"
        modelo_rapido = "llama-3.1-8b-instant"
        st.text_input("Motor de Planificación/Rúbricas:", value=modelo_complejo, disabled=True)
        st.text_input("Motor de Actas/Alertas:", value=modelo_rapido, disabled=True)
        
        st.markdown("---")
        if st.button("🚪 Cerrar Sesión Demo"):
            st.session_state.autenticado = False
            st.rerun()

    # ==========================================
    # TÍTULO PRINCIPAL Y PESTAÑAS
    # ==========================================
    st.title("🏫 Suite Digital de Automatización Docente")
    st.subheader("Herramientas de Inteligencia Artificial para el Aula Heterogénea")

    tab1, tab2, tab3, tab4 = st.tabs([
        "📝 Generador Pedagógico", 
        "💬 Sintetizador de Actas", 
        "📊 Registro de Rúbricas", 
        "📅 Agenda de Alertas"
    ])

    # ==========================================
    # PESTAÑA 1: GENERADOR PEDAGÓGICO MULTINIVEL
    # ==========================================
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
                    st.error("❌ Cliente de Groq no inicializado. Verifica las claves en Streamlit Cloud Secrets.")
                else:
                    with st.spinner("Llama 3.3 70B analizando el Diseño Curricular..."):
                        try:
                            prompt_sistema = (
                                "Sos un asesor técnico-pedagógico experto de la Provincia de Buenos Aires. "
                                "Tu tarea es analizar el contenido y devolver una planificación académica y secuencias adaptadas.\n\n"
                                "DEBES RESPONDER ESTRICTAMENTE EN FORMATO JSON, con la siguiente estructura de claves:\n"
                                "{\n"
                                "  \"planificacion\": \"Texto con fundamentación formal, objetivos y criterios.\",\n"
                                "  \"nivel_inicial\": \"Texto con la versión adaptada simple y actividades directas.\",\n"
                                "  \"nivel_medio\": \"Texto con la secuencia didáctica estándar para el grado.\",\n"
                                "  \"nivel_avanzado\": \"Texto con desafíos de producción escrita compleja o pensamiento crítico.\"\n"
                                "}"
                            )
                            
                            completion = client.chat.completions.create(
                                messages=[
                                    {"role": "system", "content": prompt_sistema},
                                    {"role": "user", "content": f"Área Curricular: {area}\nEje Temático: {eje_tematico}\nTexto:\n{texto_soporte}"}
                                ],
                                model=modelo_complejo,
                                temperature=0.3,
                                response_format={"type": "json_object"}
                            )
                            
                            respuesta_json = json.loads(completion.choices[0].message.content)
                            
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
                                
                            # BOTÓN DE DESCARGA DE LA PLANIFICACIÓN COMPLETA
                            documento_completo = f"=== PLANIFICACIÓN FORMAL ===\n{plan_txt}\n\n=== SECUENCIA ADAPTADA: INICIAL ===\n{ini_txt}\n\n=== SECUENCIA ADAPTADA: MEDIO ===\n{med_txt}\n\n=== SECUENCIA ADAPTADA: AVANZADO ===\n{av_txt}"
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

    # ==========================================
    # PESTAÑA 2: SINTETIZADOR DE ACTAS
    # ==========================================
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
                    st.error("❌ Cliente de Groq no inicializado.")
                else:
                    with st.spinner("Llama 3.1 8B formalizando el texto..."):
                        try:
                            prompt_sistema_acta = (
                                "Sos un asistente administrativo escolar experto. Procesá el texto e informal "
                                "y devolvé un objeto JSON con claves: alumno, adulto, categoria, compromiso, nota_formal."
                            )
                            
                            completion_acta = client.chat.completions.create(
                                messages=[
                                    {"role": "system", "content": prompt_sistema_acta},
                                    {"role": "user", "content": texto_crudo}
                                ],
                                model=modelo_rapido,
                                temperature=0.1,
                                response_format={"type": "json_object"}
                            )
                            
                            res_acta = json.loads(completion_act
