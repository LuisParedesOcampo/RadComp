RadComp: Clinical Radiobiology Suite 🧬

https://radcomp.streamlit.app/

RadComp is a specialized software tool designed by a Medical Physicist to assist in clinical decision-making and radiobiological research. It enables the comparison of radiation fractionation schemes by calculating biological doses based on the Linear-Quadratic (LQ) model and international safety standards.

🌟 Key Features
Side-by-Side Comparison: Simultaneously evaluate a Reference Schedule vs. a New/Hypofractionated Schedule.

Integrated QUANTEC Database: Automatic selection of α/β ratios and dose constraints for various Organs at Risk (OARs) and tumor types.

Custom Overrides: Flexibility to input user-defined α/β values while maintaining data traceability.

Interactive Visualizations: (Coming soon) Comparative charts for BED and EQD2 analysis.

🧮 Radiobiological Model
The tool utilizes the Linear-Quadratic (LQ) Model to calculate cell survival and biological effectiveness:

1. Biologically Effective Dose (BED)
The BED represents the total dose required to produce a specific biological effect if delivered in infinitely small fractions:

$$BED = D \times \left(1 + \frac{d}{\alpha/\beta}\right)$$

2. Equivalent Dose in 2 Gy (EQD2)
To normalize treatment schemes to a standard 2 Gy fractionation:
   
$$EQD2 = \frac{BED}{1 + \frac{2}{\alpha/\beta}}$$

Where $D$ is the total dose, $d$ is the dose per fraction, and $\alpha/\beta$ is the tissue-specific radiosensitivity ratio.

🛠️ Tech Stack
Language: Python 3.x

Web Framework: Streamlit

Data Handling: Pandas

Visualization: Plotly (Optional / In-development)

🚀 Installation & Local Run
To run this project locally, clone the repository and install the dependencies:

git clone https://github.com/your-username/RadComp.git

cd RadComp

pip install -r requirements.txt

streamlit run main.py

⚠️ Disclaimer

For Research and Educational Use Only. This tool is not a medical device and has not been cleared for clinical use by any regulatory authority. All calculations must be independently verified by a certified Medical Physicist or Radiation Oncologist. The author assumes no liability for clinical errors or misuse of this software.

✉️ Contact & Collaboration
I am a Medical Physicist interested about the intersection of oncology and software development. I am open to feedback, collaborations, and professional opportunities.

LinkedIn: Luis Fernando Paredes https://www.linkedin.com/in/lfparedes1/
Email: luisfernandoparedes2@gmail.com
