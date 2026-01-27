# 🧬 RadComp: Radiobiology Calculator for Medical Physics

**RadComp** is a clinical decision support tool designed to streamline the conversion of physical doses into biologically equivalent doses ($BED$ and $EQD2$) and to perform risk analysis in re-irradiation scenarios.

🚀 **Live App Access:** [https://radcomp.streamlit.app/]

## ✨ Key Features
- **LQ Modeling:** Precise fractionation conversion using the Linear-Quadratic model.
- **Clinical Database:** Pre-configured $\alpha/\beta$ ratios and dose-volume constraints based on QUANTEC and international peer-reviewed literature.
- **Advanced Re-irradiation Module:**
  - Time-based biological recovery modeling.
  - Spatial overlap penalty adjustment for high-dose regions.
  - Cumulative dose assessment with dynamic stacked charts.

🧮 Radiobiological Model
The tool utilizes the Linear-Quadratic (LQ) Model to calculate cell survival and biological effectiveness:

1. Biologically Effective Dose (BED)
The BED represents the total dose required to produce a specific biological effect if delivered in infinitely small fractions:

$$BED = D \times \left(1 + \frac{d}{\alpha/\beta}\right)$$

2. Equivalent Dose in 2 Gy (EQD2)
To normalize treatment schemes to a standard 2 Gy fractionation:
   
$$EQD2 = \frac{BED}{1 + \frac{2}{\alpha/\beta}}$$

Where $D$ is the total dose, $d$ is the dose per fraction, and $\alpha/\beta$ is the tissue-specific radiosensitivity ratio.

## 🛠️ Tech Stack
- **Python 3.x**
- **Streamlit** (UI Framework)
- **Plotly** (Interactive Visualizations)

🚀 Installation & Local Run
To run this project locally, clone the repository and install the dependencies:

git clone https://github.com/your-username/RadComp.git

- cd RadComp
- pip install -r requirements.txt
- streamlit run main.py


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
