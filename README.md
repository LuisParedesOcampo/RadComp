# 🧬 RadComp: Radiobiology Calculator for Medical Physics

**RadComp** is a clinical decision support tool designed to streamline the conversion of physical doses into biologically equivalent doses ($BED$ and $EQD2$) and to perform risk analysis in complex re-irradiation scenarios, including **SBRT/SRS**.

🚀 **Live App Access:** [https://radcomp.streamlit.app/]

## ✨ Key Features
- **Dual-Engine Modeling:** Seamless switching between Standard LQ and **Linear-Quadratic-Linear (LQL)** models based on dose per fraction.
- **Smart Clinical Alerts:** Dynamic detection of biological validity thresholds ($d_T = 2\cdot\alpha/\beta$) specific to the selected tissue (e.g., Spinal Cord vs. Tumor), preventing model misuse.
- **Clinical Database:** Pre-configured $\alpha/\beta$ ratios and dose-volume constraints based on QUANTEC, HyTEC, and international peer-reviewed literature.
- **Advanced Re-irradiation Module:**
  - Time-based biological recovery modeling (12-24 months).
  - Spatial overlap penalty adjustment for high-dose regions.
  - Logic validation to prevent penalties on zero-dose structures.
  - Cumulative dose assessment with dynamic stacked charts.

## 🧮 Radiobiological Models

RadComp utilizes a hybrid approach to prevent the known overestimation of cell kill by the LQ model at high doses per fraction (SBRT/SRS).

### 1. Standard Linear-Quadratic (LQ) Model
Used for conventional fractionation where dose per fraction $d$ is within the "shoulder" of the survival curve.

$$BED = D \times \left(1 + \frac{d}{\alpha/\beta}\right)$$

### 2. High-Dose Correction (LQL Model)
For hypofractionated treatments (SBRT/SRS), RadComp implements the **Linear-Quadratic-Linear (LQL)** model proposed by *Astrahan (2008)*  https://doi.org/10.1118/1.2969065. The model transitions from a quadratic curve to a straight line at a specific threshold dose $d_T$:

**Validity Threshold:**
$$d_T = 2 \cdot (\alpha/\beta)$$

**Calculation ($d > d_T$):**
$$BED_{LQL} = \frac{1}{\alpha} \left[ \alpha d_T + \beta d_T^2 + \gamma (d - d_T) \right] \times N$$

*This correction is suggested automatically by the interface when the dose per fraction exceeds the specific biological threshold of the selected organ.*

### 3. Equivalent Dose in 2 Gy (EQD2)
To normalize treatment schemes to a standard 2 Gy fractionation:
   
$$EQD2 = \frac{BED}{1 + \frac{2}{\alpha/\beta}}$$

## 🧪 Clinical Validation
Reliability is our priority. RadComp's calculation engine has been validated using test vectors compared against reference clinical cases:

| Test Case | Reference Model | Expected Cumulative EQD2 | Status |
| :--- | :--- | :--- | :--- |
| Spinal Cord Re-irrad | Nieder et al. (2006) | ~56 Gy | ✅ Validated |
| Lung Re-irrad | Central Toxicity Protocols | ~69 Gy | ✅ Validated |

*Note: Validation assumes a 50% recovery factor at 12 months and an overlap penalty applied to RT1 (Previous Course).*

## ⚖️ License
This project is licensed under the **MIT License**. Feel free to use, modify, and collaborate. See the [LICENSE](LICENSE) file for details.

⚠️ Disclaimer

For Research and Educational Use Only. This tool is not a medical device and has not been cleared for clinical use by any regulatory authority. All calculations must be independently verified by a certified Medical Physicist or Radiation Oncologist. The author assumes no liability for clinical errors or misuse of this software.

✉️ Contact & Collaboration
I am a Medical Physicist interested about the intersection of oncology and software development. I am open to feedback, collaborations, and professional opportunities.

LinkedIn: Luis Fernando Paredes https://www.linkedin.com/in/lfparedes1/
Email: luisfernandoparedes2@gmail.com


## 🛠️ Tech Stack
- **Python 3.10+**
- **Streamlit** (UI Framework)
- **Plotly** (Interactive Visualizations)
- **NumPy/Pandas** (Calculation Engine)

## 🚀 Installation & Local Run
To run this project locally, clone the repository and install the dependencies:

```bash
git clone [https://github.com/LuisParedesOcampo/RadComp.git](https://github.com/LuisParedesOcampo/RadComp.git)
cd RadComp
pip install -r requirements.txt
streamlit run main.py
