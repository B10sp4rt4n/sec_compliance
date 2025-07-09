# Calculadora de Cumplimiento - ThreatDown vs MRG Effitas (Streamlit MVP)

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# --- Cargar tabla de benchmark
@st.cache_data
def cargar_benchmark():
    df = pd.read_excel("Benchmark_MRG_Effitas_Consolidado.xlsx")
    return df

benchmark = cargar_benchmark()

# --- Funciones predefinidas por paquete
paquetes = {
    "Core": [
        "Next-gen AV",
        "Incident Response",
        "Device Control",
        "Application Block",
        "Vulnerability Assessment",
        "Browser Phishing Protection"
    ],
    "Advanced": ["Next-gen AV", "Incident Response", "Device Control", "Application Block",
                "Vulnerability Assessment", "Browser Phishing Protection", "Ransomware Rollback",
                "EDR (Endpoint Detection & Response)", "Patch Management", "Firewall Management",
                "Managed Threat Hunting"],
    "Elite": ["Next-gen AV", "Incident Response", "Device Control", "Application Block",
              "Vulnerability Assessment", "Browser Phishing Protection", "Ransomware Rollback",
              "EDR (Endpoint Detection & Response)", "Patch Management", "Firewall Management",
              "Managed Threat Hunting", "MDR (Managed Detection & Response)"],
    "Ultimate": ["Next-gen AV", "Incident Response", "Device Control", "Application Block",
                 "Vulnerability Assessment", "Browser Phishing Protection", "Ransomware Rollback",
                 "EDR (Endpoint Detection & Response)", "Patch Management", "Firewall Management",
                 "Managed Threat Hunting", "MDR (Managed Detection & Response)", "DNS Filtering",
                 "Premium Support"]
}

st.title("🛡️ Radar de Cumplimiento - ThreatDown vs MRG Effitas")

colA, colB = st.columns(2)

with colA:
    modo = st.radio("Selecciona modo de evaluación:", ["Paquete predefinido", "Configuración personalizada"])

    # --- Selección de funciones activas
    if modo == "Paquete predefinido":
        paquete = st.selectbox("Selecciona un paquete:", list(paquetes.keys()))
        funciones_activas = paquetes[paquete].copy()
        if st.checkbox("✳️ Antispam (opcional, refuerza Phishing & LFPDPPP)", value=True):
            funciones_activas.append("Antispam")
    else:
        funciones_disponibles = benchmark["Función"].unique().tolist() + ["Antispam"]
        funciones_activas = ["Next-gen AV"]  # Siempre activo
        st.write("**Nota:** Next-gen AV (EPP) siempre está activo.")
        for funcion in funciones_disponibles:
            if funcion == "Next-gen AV":
                st.checkbox("✅ " + funcion + " (obligatorio)", value=True, disabled=True)
            elif funcion == "Antispam":
                if st.checkbox("✳️ " + funcion + " (opcional, refuerza Phishing & LFPDPPP)", value=True):
                    funciones_activas.append(funcion)
            else:
                if st.checkbox(funcion, value=False):
                    funciones_activas.append(funcion)

# --- Cálculo de cumplimiento relativo al stack activo (Opción B)
categorias = ["Assessment", "Exploit", "Banking", "Ransomware", "Phishing"]
puntajes = {cat: 0.0 for cat in categorias}
totales = {cat: 0.0 for cat in categorias}
faltantes = {cat: [] for cat in categorias}

# Tabla de aportes funcionales por función y categoría
aporte_funcional = {
    "Next-gen AV": {"Assessment": 0.4, "Exploit": 0.6, "Banking": 0.2, "Ransomware": 0.5, "Phishing": 0.3},
    "Incident Response": {"Assessment": 0.6, "Exploit": 0.6, "Banking": 0.4, "Ransomware": 0.7, "Phishing": 0.5},
    "Device Control": {"Assessment": 0.3, "Exploit": 0.4, "Banking": 0.2, "Ransomware": 0.4, "Phishing": 0.3},
    "Application Block": {"Assessment": 0.4, "Exploit": 0.5, "Banking": 0.3, "Ransomware": 0.6, "Phishing": 0.4},
    "Vulnerability Assessment": {"Assessment": 0.8, "Exploit": 0.6, "Banking": 0.3, "Ransomware": 0.4, "Phishing": 0.3},
    "Browser Phishing Protection": {"Assessment": 0.2, "Exploit": 0.3, "Banking": 0.5, "Ransomware": 0.2, "Phishing": 0.8},
    "Ransomware Rollback": {"Assessment": 0.2, "Exploit": 0.4, "Banking": 0.2, "Ransomware": 0.9, "Phishing": 0.3},
    "EDR (Endpoint Detection & Response)": {"Assessment": 0.7, "Exploit": 0.8, "Banking": 0.4, "Ransomware": 0.7, "Phishing": 0.5},
    "Patch Management": {"Assessment": 0.6, "Exploit": 0.4, "Banking": 0.3, "Ransomware": 0.5, "Phishing": 0.2},
    "Firewall Management": {"Assessment": 0.5, "Exploit": 0.7, "Banking": 0.3, "Ransomware": 0.5, "Phishing": 0.3},
    "Managed Threat Hunting": {"Assessment": 0.6, "Exploit": 0.7, "Banking": 0.4, "Ransomware": 0.7, "Phishing": 0.6},
    "MDR (Managed Detection & Response)": {"Assessment": 0.6, "Exploit": 0.7, "Banking": 0.4, "Ransomware": 0.8, "Phishing": 0.6},
    "DNS Filtering": {"Assessment": 0.4, "Exploit": 0.4, "Banking": 0.6, "Ransomware": 0.3, "Phishing": 0.7},
    "Premium Support": {"Assessment": 0.5, "Exploit": 0.5, "Banking": 0.2, "Ransomware": 0.5, "Phishing": 0.4},
    "Antispam": {"Assessment": 0.2, "Exploit": 0.1, "Banking": 0.6, "Ransomware": 0.2, "Phishing": 0.9}
}

# Sumar los aportes de funciones activas
# Puntajes con funciones activas
for funcion in funciones_activas:
    if funcion in aporte_funcional:
        for cat in categorias:
            puntajes[cat] += aporte_funcional[funcion][cat]

# Totales con TODAS las funciones conocidas
for funcion in aporte_funcional:
    for cat in categorias:
        totales[cat] += aporte_funcional[funcion][cat]

# Calcular cumplimiento relativo al máximo que puede aportar el stack activo
scaled = [round(puntajes[cat] / totales[cat], 2) if totales[cat] > 0 else 0 for cat in categorias]
scaled += scaled[:1]  # para cerrar radar


st.write("### Radar de cumplimiento")
values = [puntajes[cat] for cat in categorias]
total_values = [totales[cat] for cat in categorias]
scaled = [v / t if t > 0 else 0 for v, t in zip(values, total_values)]
scaled += scaled[:1]
labels = categorias + [categorias[0]]
angles = [n / float(len(labels)) * 2 * 3.14159 for n in range(len(labels))]

fig, ax = plt.subplots(figsize=(5, 5), subplot_kw=dict(polar=True))
ax.plot(angles, scaled, linewidth=2, linestyle='solid')
ax.fill(angles, scaled, alpha=0.3)
ax.set_thetagrids([a * 180/3.14159 for a in angles[:-1]], categorias)
ax.set_title("Nivel de Cumplimiento por Evaluación MRG", size=12)
ax.set_ylim(0, 1)
ax.set_yticks([0.2, 0.4, 0.6, 0.8, 1.0])
ax.set_yticklabels(["0.2", "0.4", "0.6", "0.8", "1.0"])
ax.spines['polar'].set_visible(True)
ax.spines['polar'].set_linewidth(1.5)
st.pyplot(fig)

# --- Mostrar resultados extendidos
st.subheader("Resultados de Cumplimiento")

st.write("### Puntajes por categoría:")
for cat in categorias:
    st.write(f"{cat}: {round(puntajes[cat], 2)} / {round(totales[cat],2)}")

# --- Mapa de cumplimiento (nivel + comentario)
st.write("### Mapa de Evaluación por Dimensión")
def nivel_compliance(score, total):
    if total == 0:
        return "Sin datos", "⚪️"
    ratio = score / total
    if ratio >= 0.8:
        return "Alto", "🟢"
    elif ratio >= 0.4:
        return "Parcial", "🟠"
    else:
        return "Crítico", "🔴"

for cat in categorias:
    nivel, color = nivel_compliance(puntajes[cat], totales[cat])
    st.markdown(f"**{cat}**: {color} Nivel **{nivel}** — {round(puntajes[cat], 2)} de {round(totales[cat],2)} funciones clave activas")

    if faltantes[cat]:
        st.write(f"Funciones recomendadas para mejorar: {', '.join(faltantes[cat])}")

# --- Cruce normativo basado en ponderaciones
st.subheader("Mapa de Contribución Normativa")
normativas = {
    "ISO 27001": [1.0, 1.0, 0.3, 0.8, 0.6 + (0.2 if "Antispam" in funciones_activas else 0)],
    "NIST CSF":  [1.0, 1.0, 1.0, 1.0, 1.0],
    "PCI-DSS":   [1.0, 0.8, 1.0, 1.0, 1.0 + (0.3 if "Antispam" in funciones_activas else 0)],
    "SOC 2":     [0.8, 0.8, 0.3, 1.0, 0.3],
    "LFPDPPP":   [0.5, 0.3, 1.0, 1.0, 1.0 + (0.5 if "Antispam" in funciones_activas else 0)]
}

st.write("Cumplimiento relativo con base en los puntajes actuales y el cruce funcional:")
labels = list(normativas.keys())
valores_norma = []
for norma, pesos in normativas.items():
    contribucion = sum(p * s for p, s in zip(pesos, scaled[:-1]))
    maximo = sum(pesos)
    cumplimiento = contribucion / maximo * 10  # escalar a 0-10
    valores_norma.append(cumplimiento)
    st.write(f"{norma}: {cumplimiento:.1f} / 10")

# --- Radar de normativas
angles = [n / float(len(labels)) * 2 * 3.14159 for n in range(len(labels))]
angles += angles[:1]
valores_norma += [valores_norma[0]]

fig2, ax2 = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
ax2.plot(angles, valores_norma, color='orange', linewidth=2)
ax2.fill(angles, valores_norma, color='orange', alpha=0.25)
ax2.set_thetagrids([a * 180/3.14159 for a in angles[:-1]], labels)
ax2.set_title("Contribución de ThreatDown al Cumplimiento Normativo")
ax2.set_ylim(0, 10)
ax2.set_yticks([2, 4, 6, 8, 10])
ax2.set_yticklabels(["2", "4", "6", "8", "10"])
st.pyplot(fig2)

# --- Benchmark general por normativa (cobertura desde endpoint y meta total)
st.subheader("📊 Acelerador de Cumplimiento Normativo desde Endpoint")

normativas = ["ISO 27001", "NIST CSF", "PCI-DSS", "SOC 2", "LFPDPPP"]
tope_endpoint_maximo = [30, 40, 50, 30, 40]
aporte_estimado_global = [70, 85, 90, 75, 80]

# Aporte dinámico por tipo de paquete
aportes_por_paquete = {
    "Core":      [10, 15, 20, 10, 15],
    "Advanced":  [18, 22, 28, 15, 20],
    "Elite":     [22, 26, 30, 18, 25],
    "Ultimate":  [25, 30, 35, 20, 30]
}

if modo == "Paquete predefinido":
    aporte_endpoint = aportes_por_paquete.get(paquete, [0, 0, 0, 0, 0])
else:
    total_funciones = len(benchmark["Función"].unique()) + 1  # +1 por Antispam
    cobertura = len(funciones_activas) / total_funciones
    aporte_endpoint = [round(c * cobertura) for c in tope_endpoint_maximo]

fig3, ax3 = plt.subplots(figsize=(10, 6))
ax3.barh(normativas, aporte_estimado_global, color="#E0E0E0", edgecolor='black', label="Meta global")
ax3.barh(normativas, tope_endpoint_maximo, color="#A6CEE3", label="Tope desde endpoint", edgecolor="black")
ax3.barh(normativas, aporte_endpoint, color="#007ACC", label="Aporte actual (ThreatDown)")

for i, value in enumerate(aporte_endpoint):
    ax3.annotate(f"{value}%", xy=(value + 2, i), va='center', color="black", fontweight='bold')
    ax3.annotate("➡", xy=(value + 5, i), va='center', fontsize=14, color="gray")

ax3.set_xlim(0, 100)
ax3.set_xlabel("Porcentaje de cumplimiento alcanzado")
ax3.set_title("ThreatDown como Acelerador de Cumplimiento Normativo desde Endpoint")
ax3.legend(loc="lower right")
plt.tight_layout()
st.pyplot(fig3)

# --- Simulación de impacto adicional por herramienta en cumplimiento normativo
st.subheader("📈 Impacto Potencial de Herramientas Complementarias")
with st.expander("📈 Mostrar/Ocultar Simulación de Herramientas Complementarias", expanded=False):
    st.subheader("📈 Impacto Potencial de Herramientas Complementarias")

    mejora_por_herramienta = {
        "DLP Endpoint Agent": {"ISO 27001": 1.0, "PCI-DSS": 0.7, "SOC 2": 0.5, "LFPDPPP": 1.5},
        "SIEM / Logging Agent": {"ISO 27001": 1.0, "NIST CSF": 0.5, "PCI-DSS": 0.5, "SOC 2": 1.0},
        "Zero Trust Agent": {"ISO 27001": 0.8, "NIST CSF": 0.6, "SOC 2": 0.6},
        "Mobile Threat Defense": {"SOC 2": 0.4, "LFPDPPP": 1.2},
        "Endpoint Compliance Scanner": {"ISO 27001": 0.6, "NIST CSF": 0.4, "PCI-DSS": 0.6},
    }

    puntajes_actuales = dict(zip(labels, valores_norma[:-1]))

    filas_mejora = []
    for herramienta, contribuciones in mejora_por_herramienta.items():
        fila = []
        total_mejora = 0
        for norma in labels:
            mejora = contribuciones.get(norma, 0)
            if mejora > 0:
                fila.append(f"+{mejora:.1f}")
                total_mejora += mejora
            else:
                fila.append("—")
        impacto = "🔼 Alta" if total_mejora >= 2.0 else "🔼 Media" if total_mejora >= 1.0 else "🔼 Baja"
        fila.append(impacto)
        filas_mejora.append([herramienta] + fila)

    fila_base = ["ThreatDown (Ultimate)"] + [f"{puntajes_actuales.get(n, 0):.1f}" for n in labels] + ["—"]
    filas_mejora.insert(0, fila_base)

    tabla_impacto = pd.DataFrame(filas_mejora, columns=["Herramienta"] + labels + ["Mejora estimada"])
    st.dataframe(tabla_impacto.style.set_properties(**{
        'text-align': 'center'
    }).set_table_styles([dict(selector='th', props=[('text-align', 'center')])]), height=320)

    st.markdown("""
    🔹 La mejora estimada es una simulación del posible impacto si se integrara la herramienta al stack actual de endpoint.<br>
    🔼 **Alta**: mejora significativa en varias normativas<br>
    🔼 **Media**: aporta entre 1 y 2 puntos globales<br>
    🔼 **Baja**: impacto menor pero puntual
    """, unsafe_allow_html=True)

# --- Tabla extendida: Acelerador configurable con herramientas complementarias
with st.expander("⚙️ Mostrar/Ocultar Simulación Gráfica con Herramientas Complementarias", expanded=False):
    st.subheader("⚙️ Simulación con Herramientas Complementarias")

    st.markdown("Selecciona herramientas complementarias para visualizar su impacto en el cumplimiento desde endpoint por normativa:")

    use_dlp = st.checkbox("🛡️ DLP Endpoint Agent")
    use_siem = st.checkbox("📋 SIEM / Logging Agent")
    use_zta = st.checkbox("🔐 Zero Trust Agent")
    use_mtd = st.checkbox("📱 Mobile Threat Defense")
    use_scan = st.checkbox("🧪 Endpoint Compliance Scanner")

    aportes_adicionales = {
        "DLP":       [5, 0, 7, 4, 8],
        "SIEM":      [6, 4, 4, 6, 0],
        "ZTA":       [5, 5, 0, 4, 0],
        "MTD":       [0, 0, 0, 2, 6],
        "SCAN":      [4, 3, 5, 0, 0],
    }

    base = aporte_endpoint.copy()

    if use_dlp:
        base = [b + a for b, a in zip(base, aportes_adicionales["DLP"])]
    if use_siem:
        base = [b + a for b, a in zip(base, aportes_adicionales["SIEM"])]
    if use_zta:
        base = [b + a for b, a in zip(base, aportes_adicionales["ZTA"])]
    if use_mtd:
        base = [b + a for b, a in zip(base, aportes_adicionales["MTD"])]
    if use_scan:
        base = [b + a for b, a in zip(base, aportes_adicionales["SCAN"])]

    base = [min(b, 100) for b in base]

    fig4, ax4 = plt.subplots(figsize=(10, 6))
    ax4.barh(normativas, aporte_estimado_global, color="#E0E0E0", edgecolor='black', label="Meta global")
    ax4.barh(normativas, tope_endpoint_maximo, color="#A6CEE3", edgecolor='black', label="Tope desde endpoint")
    ax4.barh(normativas, base, color="#33A02C", edgecolor='black', label="Simulación total (incluye herramientas)")

    for i, value in enumerate(base):
        ax4.annotate(f"{value}%", xy=(value + 2, i), va='center', color="black", fontweight='bold')

    ax4.set_xlim(0, 100)
    ax4.set_xlabel("Porcentaje de cumplimiento alcanzado")
    ax4.set_title("Simulación: Acelerador Normativo con Herramientas Complementarias")
    ax4.legend(loc="lower right")
    plt.tight_layout()
    st.pyplot(fig4)

# --- Glosario de Normativas y Referencias en Expander
with st.expander("📚 Glosario de Normativas de Cumplimiento"):
    glosario_normativas = {
        "ISO 27001": {
            "descripcion": "Estándar internacional para sistemas de gestión de seguridad de la información (SGSI). Define requisitos para proteger la confidencialidad, integridad y disponibilidad de la información.",
            "link": "https://www.iso.org/isoiec-27001-information-security.html"
        },
        "NIST CSF": {
            "descripcion": "Marco de Ciberseguridad desarrollado por el Instituto Nacional de Estándares y Tecnología de EE. UU. para mejorar la seguridad y resiliencia de infraestructuras críticas.",
            "link": "https://www.nist.gov/cyberframework"
        },
        "PCI-DSS": {
            "descripcion": "Norma de Seguridad de Datos para la Industria de Tarjeta de Pago. Aplica a cualquier entidad que procese, almacene o transmita datos de tarjetas.",
            "link": "https://www.pcisecuritystandards.org/pci_security/"
        },
        "SOC 2": {
            "descripcion": "Marco de auditoría para servicios que almacenan datos del cliente en la nube. Evalúa controles sobre seguridad, disponibilidad, integridad, confidencialidad y privacidad.",
            "link": "https://secureframe.com/hub/soc-2/what-is-soc-2"
        },
        "LFPDPPP": {
            "descripcion": "Gestor Normativo Función Pública: norma completa, con principios, ámbito de aplicación y sanciones.",
            "link": "chrome-extension://oemmndcbldboiebfnladdacbdfmadadm/https://www.diputados.gob.mx/LeyesBiblio/pdf/LFPDPPP.pdf"
        }
    }

    for norma, info in glosario_normativas.items():
        st.markdown(f"**{norma}**: {info['descripcion']} [🔗 Más info]({info['link']})")

st.markdown("---")
st.markdown("### 🛡️ Términos y Consideraciones")
st.markdown("""
Este documento es un ejercicio de análisis técnico basado en hallazgos publicados por la firma evaluadora **MRG Effitas**. 
La información utilizada proviene de fuentes públicas disponibles en su sitio oficial. 
No se busca explotar ni representar su imagen institucional, ni emitir juicio alguno sobre marcas distintas a la evaluada. 
El objetivo es exclusivamente **académico, investigativo y comparativo**, y está destinado a uso interno o como insumo de análisis de ciberseguridad.
""")
