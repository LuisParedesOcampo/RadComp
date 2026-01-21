RadComp: Clinical Radiobiology Suite 🧬

RadComp es una herramienta de software desarrollada por un Físico Médico para optimizar la toma de decisiones en radioterapia. Permite la comparación precisa de esquemas de fraccionamiento mediante el cálculo de dosis biológicas equivalentes, integrando parámetros de referencia clínica (QUANTEC). 

Características Principales:
Comparación Lado a Lado: Evaluación simultánea de esquemas de referencia (Convencionales) vs. nuevos esquemas (Hipofraccionamiento/SBRT).
Base de Datos QUANTEC Integrada: Selección automática de valores $\alpha/\beta$ y límites de tolerancia para Órganos a Riesgo (OAR).
Alertas de Seguridad Dinámicas: El sistema notifica automáticamente si un esquema supera los límites de dosis establecidos por la literatura científica.
Interfaz Web Intuitiva: Desarrollada en Python con Streamlit para un acceso rápido desde cualquier dispositivo.

🧮 Fundamentos Físicos
La aplicación utiliza el Modelo Lineal-Cuadrático (LQ) para calcular la respuesta biológica:
1.	Dosis Biológica Efectiva (BED):

$$BED = D \times \left(1 + \frac{d}{\alpha/\beta}\right)$$

2.	Dosis Equivalente en 2 Gy (EQD2):
   
$$EQD2 = \frac{BED}{1 + \frac{2}{\alpha/\beta}}$$

Donde $D$ es la dosis total y $d$ la dosis por fracción.

🚀 Tecnologías Utilizadas
•	Lenguaje: Python 3.x
•	Framework Web: Streamlit
•	Análisis de Datos: Pandas
•	Despliegue: Streamlit Cloud / Hugging Face Spaces

⚠️ Disclaimer (Aviso Legal)
IMPORTANTE: Esta herramienta ha sido desarrollada con fines educativos y de investigación para profesionales de la Física Médica y Oncología Radioterápica. No debe utilizarse como única base para la toma de decisiones clínicas. La validación final de cualquier plan de tratamiento es responsabilidad exclusiva del físico médico y el médico tratante.
