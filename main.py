import streamlit as st

st.title("RadComp")


# 1. Nuestra pequeña base de datos basada en QUANTEC y otras fuentes
datos_clinicos = {
    "Médula Espinal": {"ab": 2.0, "fuente": "QUANTEC (2010)", "limite": 45.0},
    "Cerebro (Tejido Sano)": {"ab": 3.0, "fuente": "QUANTEC (2010)", "limite": 100.0},
    "Corazon ": {"ab": 3.0, "fuente": "QUANTEC (2010)", "limite":50.0 },
    "Tronco Encefalico": {"ab": 2.1, "fuente": "QUANTEC (2010)", "limite": 50.0},
    "Próstata (Tumor)": {"ab": 1.5, "fuente": "Fowler et al.", "limite": 78.0},
    "Mama (Tumor)": {"ab": 4.0, "fuente": "START Trials", "limite": 40.0},
    "Pulmón (Tejido sano)": {"ab": 3.0, "fuente": "QUANTEC / TG-166", "limite": 20.0},
    "Recto": {"ab": 3.0, "fuente": "QUANTEC", "limite": 70.0},
    "Vejiga": {"ab": 3.0, "fuente": "QUANTEC", "limite": 70.0},
    "Higado": {"ab": 3.0, "fuente": "QUANTEC", "limite": 70.0},
    "Riñon": {"ab": 3.0, "fuente": "QUANTEC", "limite": 70.0},
    "Esofago": {"ab": 10.0, "fuente": "Emami/QUANTEC", "limite": 70.0},
    "Intestino Delgado": {"ab": 10.0, "fuente": "Emami/QUANTEC", "limite": 70.0},
    "Glándulas Parótidas": {"ab": 3.0, "fuente": "QUANTEC", "limite": 26.0},
     "Pulmón (NSCLC)": {"ab": 10.0, "fuente": "Generico", "limite": 20.0},
}

# 2. En la Sidebar: Vinculamos el selectbox con el valor alpha/beta
with st.sidebar:
    st.header("Parámetros Biológicos")
    seleccion = st.selectbox("Seleccionar valor Alpha/Beta", list(datos_clinicos.keys()))
   # st.metric("Fuente", datos_clinicos[seleccion]["fuente"])

    # El valor por defecto del número será el de la base de datos
    ab = st.number_input("Valor Alpha/Beta (Gy)",
                         min_value=0.1,
                         value=datos_clinicos[seleccion]["ab"])
    fuente_valor = datos_clinicos[seleccion]["fuente"]
    st.info(f"**Alfa/Beta:** {ab:.2f}  | **Fuente:** {fuente_valor}")




# Layout de dos columnas para comparar
col1, col2 = st.columns(2)

with col1:
    st.subheader("Esquema A (Referencia)")
    d_total_a = st.number_input("Dosis Total A (Gy)", min_value=0.0, value=45.0)
    fras_a = st.number_input("Nº Fracciones A", min_value=1, value=25)
    d_frac_a = d_total_a / fras_a

    st.metric("Dosis por fraccion A", f"{d_frac_a:.2f} Gy")
    bed_a = d_total_a * (1 + (d_frac_a / ab))
    st.metric("BED A", f"{bed_a:.2f} Gy")
    eqd2_a = bed_a / (1 + (2 / ab))  # Usando la fórmula que ya conocemos
    st.metric("EQD2 A", f"{eqd2_a:.2f} Gy")
    st.metric("Alpha/Beta", f"{ab:.2f} ")

with col2:
    st.subheader("Esquema B (Nuevo)")
    d_total_b = st.number_input("Dosis Total B (Gy)",min_value=0.0, value=30.0)
    fras_b = st.number_input("Nº Fracciones B",min_value=1, value=10)
    d_frac_b = d_total_b / fras_b
    st.metric("Dosis por fraccion B", f"{d_frac_b:.2f} Gy")
    bed_b = d_total_b * (1 + (d_frac_b / ab))
    st.metric("BED B", f"{bed_b:.2f} Gy")
    eqd2_b = bed_b / (1 + (2 / ab))  # Usando la fórmula que ya conocemos
    st.metric("EQD2 B", f"{eqd2_b:.2f} Gy")
    st.metric("Alpha/Beta", f"{ab:.2f} ")