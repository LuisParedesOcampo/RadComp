import streamlit as st

# 1. Page Configuration (Metadata for SEO)
st.set_page_config(
    page_title="RadComp | Radiobiology Calculator for Medical Physics",
    page_icon="🧬",
    layout="wide",
    menu_items={
        'About': "RadComp: A clinical tool for BED and EQD2 calculations based on QUANTEC and international standards."
    }
)

st.title("RadComp")

# 2. International Clinical Database (QUANTEC & Global References)
clinical_data = {
    "OARs (General)": {"ab": 3.0, "source": "Generic Reference", "limit": 100.0},
    "Tumor (General)": {"ab": 10.0, "source": "Generic Reference", "limit": 100.0},
    "Spinal Cord": {"ab": 2.0, "source": "QUANTEC (2010)", "limit": 45.0},
    "Brain (Healthy Tissue)": {"ab": 3.0, "source": "QUANTEC (2010)", "limit": 60.0},
    "Heart": {"ab": 3.0, "source": "QUANTEC (2010)", "limit": 30.0},
    "Brainstem": {"ab": 2.1, "source": "QUANTEC (2010)", "limit": 54.0},
    "Prostate (Tumor)": {"ab": 1.5, "source": "Fowler et al.", "limit": 78.0},
    "Breast (Tumor)": {"ab": 4.0, "source": "START Trials", "limit": 40.0},
    "Lung (Healthy Tissue)": {"ab": 3.0, "source": "QUANTEC / TG-166", "limit": 20.0},
    "Rectum": {"ab": 3.0, "source": "QUANTEC", "limit": 70.0},
    "Bladder": {"ab": 3.0, "source": "QUANTEC", "limit": 70.0},
    "Liver": {"ab": 3.0, "source": "QUANTEC", "limit": 30.0},
    "Kidney": {"ab": 3.0, "source": "QUANTEC", "limit": 18.0},
    "Esophagus": {"ab": 10.0, "source": "Emami/QUANTEC", "limit": 35.0},
    "Small Bowel": {"ab": 10.0, "source": "Emami/QUANTEC", "limit": 45.0},
    "Parotid Glands": {"ab": 3.0, "source": "QUANTEC", "limit": 26.0},
    "Lung (NSCLC)": {"ab": 10.0, "source": "Generic Reference", "limit": 60.0},
}

# 3. Sidebar: Biological Configuration and Robustness Logic
with st.sidebar:
    st.header("⚙️ Biological Configuration")

    # Selectbox for the organ/tissue
    selection = st.selectbox("Select Organ or Tissue Reference", list(clinical_data.keys()))

    # Default values from the database
    ab_default = clinical_data[selection]["ab"]
    source_ref = clinical_data[selection]["source"]
    limit_ref = clinical_data[selection]["limit"]

    # Alpha/Beta Ratio Input with manual override detection
    ab_user = st.number_input(
        f"Alpha/Beta Ratio (Gy) for {selection}",
        min_value=0.1,
        max_value=25.0,
        value=ab_default,
        step=0.1,
        help="You can modify this value for custom calculations based on clinical criteria."
    )

    # Credibility and Traceability Logic
    if ab_user == ab_default:
        st.success(f"📚 **Reference Source:** {source_ref}")
        st.caption(f"Suggested Dose Limit: {limit_ref} Gy")
    else:
        st.warning("⚠️ **Custom Value Applied**")
        st.info("The standard reference source no longer applies due to manual override.")

    ab = ab_user

# 4. Main Layout: Comparative View
col1, col2 = st.columns(2)

with col1:
    st.subheader("Schedule A (Reference)")
    total_dose_a = st.number_input("Total Dose A (Gy)", min_value=0.0, value=45.0, key="dose_a")
    fractions_a = st.number_input("Number of Fractions A", min_value=1, value=25, key="frac_a")

    dose_per_frac_a = total_dose_a / fractions_a
    bed_a = total_dose_a * (1 + (dose_per_frac_a / ab))
    eqd2_a = bed_a / (1 + (2 / ab))

    st.metric("Dose per Fraction A", f"{dose_per_frac_a:.2f} Gy")
    st.metric("BED A", f"{bed_a:.2f} Gy")
    st.metric("EQD2 A", f"{eqd2_a:.2f} Gy")
    st.metric("Alpha/Beta Ratio", f"{ab:.2f}")

with col2:
    st.subheader("Schedule B (New)")
    total_dose_b = st.number_input("Total Dose B (Gy)", min_value=0.0, value=30.0, key="dose_b")
    fractions_b = st.number_input("Number of Fractions B", min_value=1, value=10, key="frac_b")

    dose_per_frac_b = total_dose_b / fractions_b
    bed_b = total_dose_b * (1 + (dose_per_frac_b / ab))
    eqd2_b = bed_b / (1 + (2 / ab))

    st.metric("Dose per Fraction B", f"{dose_per_frac_b:.2f} Gy")
    st.metric("BED B", f"{bed_b:.2f} Gy")
    st.metric("EQD2 B", f"{eqd2_b:.2f} Gy")
    st.metric("Alpha/Beta Ratio", f"{ab:.2f}")