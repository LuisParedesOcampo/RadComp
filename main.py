import streamlit as st
import plotly.graph_objects as go


# 1. Page Configuration (Metadata for SEO)
st.set_page_config(
    page_title="RadComp | Radiobiology Calculator for Medical Physics",
    page_icon="🧬",
    layout="wide",
    menu_items={
        'About': "RadComp: A clinical tool for BED , EQD2 and Reirradiation calculations based on QUANTEC and international standards."
    }
)

# INYECCIÓN DE GOOGLE ANALYTICS
ga_id = st.secrets.get("GOOGLE_ANALYTICS_ID", None)

if ga_id:
    st.markdown(
        f"""
        <script async src="https://www.googletagmanager.com/gtag/js?id={ga_id}"></script>
        <script>
            window.dataLayer = window.dataLayer || [];
            function gtag(){{dataLayer.push(arguments);}}
            gtag('js', new Date());
            gtag('config', '{ga_id}');
        </script>
        """,
        unsafe_allow_html=True
    )

st.title("RadComp")
st.info("A clinical tool for BED , EQD2  and Reirradiation calculations based on QUANTEC and international standards")

# 2. International Clinical Database (QUANTEC & Global References)
# ===============================================================
# Valores para variable limit type
# ===================================================================
# "Dmax"          → dosis máxima puntual
# "Dmean"         → dosis media
# "Vx"            → volumen que recibe ≥ x Gy
# "Surrogate"     → aproximación BED/EQD2 de una métrica no BED
# "None"          → no aplica (α/β only)
# ====================================================================

clinical_data = {

    # =========================
    # Generic (α/β only)
    # =========================
    "OARs (General)": {
        "ab": 3.0,
        "source": "Radiobiology convention",
        "limit": None,
        "limit_type": "None"
    },
    "Tumor (General)": {
        "ab": 10.0,
        "source": "Radiobiology convention",
        "limit": None,
        "limit_type": "None"
    },

    # =========================
    # Central Nervous System
    # =========================
    "Spinal Cord": {
        "ab": 2.0,
        "source": "QUANTEC 2010",
        "limit": 52.0,
        "limit_type": "Dmax"
    },
    "Brainstem": {
        "ab": 2.1,
        "source": "QUANTEC 2010",
        "limit": 54.0,
        "limit_type": "Dmax"
    },
    "Brain (Healthy Tissue)": {
        "ab": 3.0,
        "source": "QUANTEC 2010",
        "limit": 60.0,
        "limit_type": "Surrogate"
    },

    # =========================
    # Thorax
    # =========================
    "Heart": {
        "ab": 3.0,
        "source": "QUANTEC 2010",
        "limit": 26,
        "limit_type": "Dmean"
    },
    "Lung (Healthy Tissue)": {
        "ab": 3.0,
        "source": "QUANTEC 2010",
        "limit": 20.0,
        "limit_type": "V20"  # "note": "Surrogate EQD2 approximation"
    },

    # =========================
    # Abdomen / Pelvis
    # =========================
    "Liver": {
        "ab": 3.0,
        "source": "QUANTEC 2010",
        "limit": 30.0,
        "limit_type": "Dmean"
    },
    "Kidney": {
        "ab": 3.0,
        "source": "QUANTEC 2010",
        "limit": 18.0,
        "limit_type": "Dmean"
    },
    "Small Bowel": {
        "ab": 10.0,
        "source": " QUANTEC",
        "limit": 54.0,
        "limit_type": "Dmax"
    },
    "Esophagus": {
        "ab": 10.0,
        "source": "Emami / QUANTEC",
        "limit": 34.0,
        "limit_type": "Dmean"
    },
    "Rectum": {
        "ab": 3.0,
        "source": "QUANTEC 2010 ",
        "limit": 79.0,
        "limit_type": "Dmax"
    },
    "Bladder": {
        "ab": 3.0,
        "source": "QUANTEC 2010",
        "limit": 79.0,
        "limit_type": "Dmax"
    },

    # =========================
    # Salivary glands
    # =========================
    "Parotid Glands": {
        "ab": 3.0,
        "source": "QUANTEC 2010",
        "limit": 25.0,
        "limit_type": "Dmean"
    },

    # =========================
    # Tumors (α/β only)
    # =========================
    "Prostate (Tumor)": {
        "ab": 1.5,
        "source": "Fowler et al.",
        "limit": None,
        "limit_type": "None"
    },
    "Breast (Tumor)": {
        "ab": 4.0,
        "source": "START Trials",
        "limit": None,
        "limit_type": "None"
    },
    "Lung (NSCLC)": {
        "ab": 10.0,
        "source": "Radiobiology convention",
        "limit": None,
        "limit_type": "None"
    },
}

# variable de penalizacion para tener en cuenta la superposicion de zonas de dosis
overlap_penalty = {
    "None": 0.0,
    "Partial": 0.15,
    "High": 0.30
}


# -------------------------------------------------------------------------
# Helper functions
# -------------------------------------------------------------------------
def biology_calculation(total_dose: float, fractions: int, ab: float, use_lql: bool = False):
    """
    Calcula BED y EQD2 con validación de seguridad.
    Soporta corrección LQL (Astrahan 2008) para dosis altas si use_lql=True.
    """
    if fractions <= 0 or ab <= 0:
        return 0.0, 0.0, 0.0

    d = total_dose / fractions  # Dosis por fracción

    # --- MODELO LQL (Linear-Quadratic-Linear) ---
    # Astrahan (2008): El umbral de transición (dT) es 2 * (alpha/beta)
    dt = 2 * ab

    if use_lql and d > dt:
        # Corrección para altas dosis (SBRT/SRS)
        # Parte A: Contribución hasta el umbral (Curva LQ)
        term_hq = dt * (1 + (dt / ab))

        # Parte B: Contribución lineal más allá del umbral
        term_lin = (d - dt) * (1 + ((2 * dt) / ab))

        # BED por fracción sumando ambas partes
        bed_per_frac = term_hq + term_lin
        bed = bed_per_frac * fractions
    else:
        # --- MODELO LQ ESTÁNDAR (Clásico) ---
        bed = total_dose * (1 + (d / ab))

    # Cálculo de EQD2 (Normalizado a 2Gy por fracción)
    # Se usa la fórmula estándar derivada del BED calculado
    eqd2 = bed / (1 + (2 / ab))

    return bed, eqd2, d


def recovery_factor(months):
    if months < 6:
        return 0.0
    elif months < 12:
        return 0.25
    elif months < 24:
        return 0.50
    else:
        return 0.65


# -------------------------------------------------------------------------
# Sidebar
# -------------------------------------------------------------------------

# 3. Sidebar: Biological Configuration and Robustness Logic
# ===============================================================================
with st.sidebar:
    st.header("⚙️ Calculation Settings")
    mode = st.radio(
        "Calculation Mode",
        ["Standard Comparison", "Re-irradiation"],
        index=0
    )
    selection = st.selectbox(
        "Select Organ or Tissue Reference",
        list(clinical_data.keys())
    )

    # Default values from the database
    ab_default = clinical_data[selection]["ab"]
    source_ref = clinical_data[selection]["source"]
    limit_ref = clinical_data[selection]["limit"]
    limit_type_ref = clinical_data[selection]["limit_type"]

    # Alpha/Beta Ratio Input with manual override detection
    ab_user = st.number_input(
        f"Alpha/Beta Ratio for {selection}",
        min_value=0.5,
        max_value=20.0,
        value=ab_default,
        step=0.1,
        help="You can modify this value for custom calculations based on clinical criteria."
    )

    # Credibility and Traceability Logic
    if ab_user == ab_default:
        st.success(f"📚 **Reference Source:** {source_ref}")

    else:
        st.warning("⚠️ **Custom Value Applied**")
        st.info("The standard reference source no longer applies due to manual override.")

    st.caption(f"Suggested Dose Limit: {limit_ref} Gy {limit_type_ref} ")
    ab = ab_user

    if mode == "Re-irradiation":
        st.divider()
        st.header("⏳ Re-irradiation Parameters")

        recovery_mode = st.radio(
            "Biological Recovery Assumption",
            [
                "No recovery (full BED summation)",
                "Partial recovery (time-based model)"
            ]
        )
        interval_months = st.slider(
            "Time interval between RT1 and RT2 (months)",
            0, 24, 12, disabled=(recovery_mode == "No recovery (full BED summation)")
        )
        st.caption("For intervals longer than 24 months, select the maximum value " "(model saturation assumption).")

        overlap = st.selectbox(
            "Overlap with previous high-dose region",
            ["None", "Partial", "High"]
        )
        if overlap != "None":
            overlap_application = st.radio(
                "How should the overlap penalty be applied?",
                options=["cumulative", "rt1_only"],
                format_func=lambda x:
                "Apply to cumulative dose (RT1 + RT2) (default, conservative)"
                if x == "cumulative"
                else "Apply only to first treatment (RT1)"
            )

        penalty = overlap_penalty[overlap]
        penalty_percentage = int(penalty * 100)

        if overlap == "None":
            st.info(
                """
                **No spatial overlap assumed**
  
                - No overlap-related biological penalty is applied.
                - Cumulative dose is calculated as:
                  **RT1 (with or without recovery) + RT2**.
  
                This option assumes that the re-irradiated volume does **not**
                significantly overlap with previously high-dose regions.
                """
            )

        else:
             if overlap_application == "cumulative":
                 st.info(
                    f"""
                        **Conservative overlap model**

                        - Selected overlap level: **{overlap}**
                        - Applied biological penalty (BED-based): **+{penalty_percentage}%**
                        - Penalty applied to: **Cumulative biological dose (RT1 + RT2)**

                        This conservative approach assumes that spatial overlap between
                        high-dose regions increases the overall biological risk of the
                        combined treatments.
                        """
                 )
             else:
                st.info(
                    f"""
                        **RT1-based overlap model**

                        - Selected overlap level: **{overlap}**
                        - Applied biological penalty (BED-based): **+{penalty_percentage}%**
                        - Penalty applied to: **Previous treatment only (RT1)**

                        This approach assumes that the increased biological risk associated
                        with overlap primarily reflects pre-existing tissue damage from
                        the first irradiation course.
                        """
                )

        st.caption(
        "Overlap adjustments are model-based assumptions and do not replace "
        "volumetric dose evaluation or clinical judgment."
         )
# ----------------------------------------------------------------------------------------------------------------
# 4. Main Layout: Comparative View
# -------------------------------------------------------------------------------------------------------------------
col1, col2 = st.columns(2)
# ------------------- Schedule A / RT1 -------------------
with (col1):
    title_a = "Schedule A (Reference)"
    if mode == "Re-irradiation":
        title_a = "Previous Radiation Course (RT1)"

    st.subheader(title_a)

    total_dose_a = st.number_input("Total Dose A (Gy)", min_value=0.0, value=45.0, key="dose_a")
    fractions_a = st.number_input("Number of Fractions A", min_value=1, value=25, key="frac_a")

    # --- LOGICA DUAL DE UMBRAL INTELIGENTE ---
    d_check_a = total_dose_a / fractions_a if fractions_a > 0 else 0
    astrahan_threshold = 2 * ab  # Umbral dinámico dT
    use_lql_a = False

    if d_check_a > astrahan_threshold:

        st.caption(
            f"⚠️ High Dose/Fx: Exceeds LQ validity for **{selection}**. "
            f"It is suggested to enable the LQL correction below."
        )
        use_lql_a = st.checkbox(
            "Enable LQL Correction (Astrahan 2008)",
            value=False,
            key="lql_a",
            help=f"Standard LQ overestimates cell kill when dose per fraction > {astrahan_threshold:.1f} Gy for ***{selection}***."

        )

    bed_a, eqd2_a, dose_per_frac_a = biology_calculation(total_dose_a, fractions_a,ab,use_lql_a)  # asi se pueden guardar los valores de una tupla

    st.metric("Dose per Fraction A", f"{dose_per_frac_a:.2f} Gy")
    st.metric("BED A", f"{bed_a:.2f} Gy")
    st.metric("EQD2 A", f"{eqd2_a:.2f} Gy")
    st.metric("Alpha/Beta Ratio", f"{ab:.2f}")
    if use_lql_a:
        st.caption("✅ LQL Model Active")
# ------------------- Schedule B / RT2 -------------------
with col2:
    title_b = "Schedule B (New)"
    if mode == "Re-irradiation":
        title_b = "Planned Radiation Course (RT2)"

    st.subheader(title_b)
    total_dose_b = st.number_input("Total Dose B (Gy)", min_value=0.0, value=30.0, key="dose_b")
    fractions_b = st.number_input("Number of Fractions B", min_value=1, value=10, key="frac_b")

    # --- LOGICA DUAL DE UMBRAL INTELIGENTE ---
    d_check_b = total_dose_b / fractions_b if fractions_b > 0 else 0
    # astrahan_threshold ya calculado arriba
    use_lql_b = False

    if d_check_b > astrahan_threshold:
        st.caption(
            f"⚠️ High Dose/Fx: Exceeds LQ validity for **{selection}**. "
            f"It is suggested to enable the LQL correction below."
        )
        use_lql_b = st.checkbox(
            "Enable LQL Correction (Astrahan 2008)",
            value=False,
            key="lql_b",
            help=f"Standard LQ overestimates cell kill when dose per fraction > {astrahan_threshold:.1f} Gy for ***{selection}***."
        )

    bed_b, eqd2_b, dose_per_frac_b = biology_calculation(total_dose_b, fractions_b, ab,use_lql_b)

    st.metric("Dose per Fraction B", f"{dose_per_frac_b:.2f} Gy")
    st.metric("BED B", f"{bed_b:.2f} Gy")
    st.metric("EQD2 B", f"{eqd2_b:.2f} Gy")
    st.metric("Alpha/Beta Ratio", f"{ab:.2f}")
    if use_lql_b:
        st.caption("✅ LQL Model Active")

# -------------------------------------------------------------------------
# Re-irradiation Analysis
# -------------------------------------------------------------------------
if mode == "Re-irradiation":

    st.divider()
    st.subheader("🔁 Cumulative Biological Dose Assessment")

    if recovery_mode == "No recovery (full BED summation)":
        effective_bed_a = bed_a
        st.warning(
            """
            **Conservative assumption applied**

            - No biological recovery from previous irradiation is assumed.
            - 100% of the BED from RT1 is carried forward.

            This conservative approach is commonly used for critical organs
            and risk-averse clinical decision-making.
            """
        )
    else:
        rec = recovery_factor(interval_months)
        effective_bed_a = bed_a * (1 - rec)

        # Las dos siguientes lineas de codigo solo se usan para mostrar los porcentajes en la info
        recovery_percentage = int(rec * 100)
        remaining_percentage = 100 - recovery_percentage

        st.info(
            f"""
                   **Biological recovery model active**

                   - Time interval between treatments: **{interval_months} months**
                   - Assumed biological recovery from RT1: **{recovery_percentage}%**
                   - Remaining biological effect from RT1: **{remaining_percentage}%**

                   The BED contribution from the previous irradiation course is
                   reduced according to this recovery assumption before being
                   combined with the new treatment.
                   """
        )
    # Validación de dosis para aplicar penalización
    # Solo existe riesgo biológico por solapamiento si AMBAS dosis son > 0
    has_overlap_risk = total_dose_a > 0 and total_dose_b > 0

    if overlap != "None" and has_overlap_risk:
            penalty_factor = 1 + overlap_penalty[overlap]

            if overlap_application == "cumulative":
                # Modelo conservador: penaliza la suma total
                bed_cumulative = (effective_bed_a + bed_b) * penalty_factor
            else:
                # Modelo estándar: penaliza solo la dosis remanente de RT1
                bed_cumulative = (effective_bed_a * penalty_factor) + bed_b
    else:
            # Si una dosis es 0 o el usuario eligió "None", no se aplica penalización
            bed_cumulative = effective_bed_a + bed_b

    eqd2_cumulative = bed_cumulative / (1 + (2 / ab))

    col3, col4 = st.columns(2)
    with col3:
        st.metric("Cumulative BED", f"{bed_cumulative:.2f} Gy")
    with col4:
        st.metric("Cumulative EQD2", f"{eqd2_cumulative:.2f} Gy")

    if limit_ref is None:
        if "Tumor" in selection:
            st.info(
                "Target volume selected. No upper dose constraint applies, "
                "as dose escalation may be clinically intended."
            )
        else:
            st.info(
                "No dose constraint applies for the selected structure. "
                "Cumulative dose comparison is not performed."
            )
    else:
        ratio = eqd2_cumulative / limit_ref

        st.caption(
            f"⚠️ Comparison performed using cumulative EQD2 against "
            f"reported {limit_type_ref} {selection} tolerance.")

        if ratio < 0.9:
            st.success("Within reported cumulative tolerance (model-based)")
        elif ratio < 1.0:
            st.warning("Borderline cumulative dose – caution advised")
        else:
            st.error("Above reported cumulative tolerance – high risk")

    st.caption(
        "⚠️ Cumulative dose estimates are model-based and do not replace "
        "DVH analysis or voxel-level dose accumulation."
    )

# --- VISUALIZATION SECTION ---

st.divider()
st.subheader("📊 Visual Biological Analysis")

# 1. Preparación de datos según el modo
if mode == "Re-irradiation":
    # Usamos la dosis efectiva de RT1 (con recuperación y penalización)
    # y la dosis de RT2 para mostrar el acumulado.

    # Calculamos el EQD2 efectivo de RT1 para que el "stack" sea matemáticamente correcto
    effective_eqd2_a = effective_bed_a / (1 + (2 / ab))

    label_a = "RT1 (Remaining Dose)"
    label_b = "RT2 (New Dose)"

    plot_values_a = [effective_bed_a, effective_eqd2_a]
    plot_values_b = [bed_b, eqd2_b]

    current_barmode = 'stack'
    y_axis_label = "Accumulated Dose (Gy)"
else:
    # Modo estándar: comparativa lateral simple
    label_a = "Schedule A (Ref)"
    label_b = "Schedule B (New)"

    plot_values_a = [bed_a, eqd2_a]
    plot_values_b = [bed_b, eqd2_b]

    current_barmode = 'group'
    y_axis_label = "Dose (Gy)"

# 2. Creación del gráfico
fig = go.Figure()

# Añadir Parte A (Base en Re-irrad o Izquierda en Estándar)
fig.add_trace(go.Bar(
    x=['BED (Gy)', 'EQD2 (Gy)'],
    y=plot_values_a,
    name=label_a,
    marker_color='#1f77b4',
    text=[f"{v:.1f}" for v in plot_values_a],
    textposition='auto',
))

# Añadir Parte B (Tope en Re-irrad o Derecha en Estándar)
fig.add_trace(go.Bar(
    x=['BED (Gy)', 'EQD2 (Gy)'],
    y=plot_values_b,
    name=label_b,
    marker_color='#ff7f0e',
    text=[f"{v:.1f}" for v in plot_values_b],
    textposition='auto',
))

# 3. Estilo del Layout
fig.update_layout(
    barmode=current_barmode,
    template='plotly_white',
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    yaxis_title=y_axis_label,
    margin=dict(l=20, r=20, t=60, b=20),
    height=450
)

st.plotly_chart(fig, width="stretch")

# Legal Disclaimer Section

st.divider()
st.subheader("⚠️ Disclaimer & Terms of Use")

st.markdown("""
<div style="background-color: #f8f9fa; padding: 20px; border-radius: 10px; border: 1px solid #dee2e6;">
    <p style="color: #6c757d; font-size: 0.9em;">
        <strong>Notice:</strong> This software is intended for <strong>educational and research purposes only</strong>. 
        It is not a medical device and has not been cleared by any regulatory body (FDA, CE, etc.) for clinical use.
    </p>
    <ul style="color: #6c757d; font-size: 0.85em;">
        <li><strong>Responsibility:</strong> The user assumes all responsibility for the interpretation and clinical application of the results provided by this tool.</li>
        <li><strong>Verification:</strong> Calculations must be independently verified by a certified Medical Physicist or Radiation Oncologist before any clinical decision.</li>
        <li><strong>Liability:</strong> The developers of RadComp shall not be held liable for any damages, clinical errors, or consequences arising from the use or misuse of this software.</li>
    </ul>
    <p style="color: #6c757d; font-size: 0.85em; font-style: italic;">
        By using this application, you acknowledge and agree to these terms.
    </p>
</div>
""", unsafe_allow_html=True)
# Contact & Collaboration Section
st.write("")  # Espacio en blanco
st.subheader("Contact & Feedback")
st.markdown("""
Are you interested in new features or have suggestions for future developments? 
I am open to collaborations and professional opportunities in Medical Physics and Software Development.

- **LinkedIn:** [Luis Fernando Paredes ](https://www.linkedin.com/in/lfparedes1/)
- **GitHub:** [Project Repository](https://github.com/LuisParedesOcampo/RadComp.git)
- **Email:** luisfernandoparedes2@gmail.com

*Developed by a Clinical Medical Physicist*
""")
