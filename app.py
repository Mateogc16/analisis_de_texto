import streamlit as st
import pandas as pd
from textblob import TextBlob
import re
from googletrans import Translator

# ----------------------------------------
# Configuración de la página con detalles de realeza
# ----------------------------------------
st.set_page_config(
    page_title="📜 Analizador de Texto - El Reino",
    page_icon="🏰",
    layout="wide"
)

# ----------------------------------------
# Estilos de la corte: dorado, morado y tipografía clásica
# ----------------------------------------
st.markdown("""
    <style>
        body {
            background-color: #F5E1A4;  /* Dorado suave */
            color: #4A148C;             /* Texto morado oscuro */
            font-family: 'Georgia', serif;
        }
        h1, h2, h3, .title {
            color: #6A1B9A;             /* Morado real */
            font-family: 'Georgia', serif;
        }
        .sidebar .sidebar-content {
            background-color: #6A1B9A;  /* Morado real */
            color: #ffffff;
            font-family: 'Georgia', serif;
        }
        .stButton>button {
            background-color: #6A1B9A;
            color: white;
            font-family: 'Georgia', serif;
            font-size: 16px;
            border-radius: 8px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        }
        .stTextArea>div>textarea {
            background-color: #fff8e1;  /* Pergamino dorado claro */
            color: #4A148C;
            font-family: 'Georgia', serif;
        }
        .stFileUploader>div {
            background-color: #fff8e1;
            border: 1px solid #6A1B9A;
            border-radius: 6px;
            padding: 0.5em;
        }
        hr {
            border-top: 2px solid #6A1B9A;
        }
    </style>
""", unsafe_allow_html=True)

# ----------------------------------------
# Título y descripción del reino
# ----------------------------------------
st.title("📝 Analizador de Texto del Reino Real")
st.markdown("""
En este noble salón del castillo, analizamos el discurso de súbditos y aliados:
- **Sentimiento** y **subjetividad** de cada palabra  
- **Palabras clave** más usadas  
- **Frases** destacadas  
""", unsafe_allow_html=True)

# ----------------------------------------
# Barra lateral de opciones nobles
# ----------------------------------------
st.sidebar.title("Opciones Nobles")
modo = st.sidebar.selectbox(
    "Seleccione el modo de entrada:",
    ["Texto directo", "Archivo de texto"]
)

# ----------------------------------------
# Función: contar palabras (sin NLTK)
# ----------------------------------------
def contar_palabras(texto):
    stop_words = set([
        # Español (ejemplo reducido)
        "de","la","que","el","en","y","a","los","del","se","las","por","un","para","con",
        # Inglés (ejemplo reducido)
        "the","and","to","of","a","in","is","it","you","that"
    ])
    palabras = re.findall(r'\b\w+\b', texto.lower())
    filtradas = [p for p in palabras if p not in stop_words and len(p) > 2]
    freq = {}
    for p in filtradas:
        freq[p] = freq.get(p, 0) + 1
    return dict(sorted(freq.items(), key=lambda x: x[1], reverse=True)), filtradas

# ----------------------------------------
# Función: traducir texto al inglés
# ----------------------------------------
def traducir_texto(texto):
    translator = Translator()
    try:
        traduccion = translator.translate(texto, src='es', dest='en')
        return traduccion.text
    except Exception as e:
        st.error(f"Error al traducir: {e}")
        return texto

# ----------------------------------------
# Función: procesar texto con TextBlob
# ----------------------------------------
def procesar_texto(texto):
    texto_original = texto.strip()
    texto_ingles = traducir_texto(texto_original)
    blob = TextBlob(texto_ingles)
    sentimiento = blob.sentiment.polarity
    subjetividad = blob.sentiment.subjectivity
    frases_originales = [f.strip() for f in re.split(r'[.!?]+', texto_original) if f.strip()]
    return sentimiento, subjetividad, frases_originales, texto_original, texto_ingles

# ----------------------------------------
# Función: mostrar resultados en la corte
# ----------------------------------------
def mostrar_resultados(sentimiento, subjetividad, palabras_ordenadas, frases):
    # Sentimiento y subjetividad
    st.subheader("🔮 Sentimiento y Subjetividad")
    sent_label = ("Positivo" if sentimiento>0 else 
                  "Negativo" if sentimiento<0 else "Neutral")
    st.write(f"**Sentimiento:** {sent_label} ({sentimiento:.2f})")
    st.write(f"**Subjetividad:** {subjetividad:.2f}")
    # Palabras más frecuentes
    st.subheader("⚔️ Palabras Más Frecuentes")
    if palabras_ordenadas:
        df = pd.DataFrame(palabras_ordenadas.items(), columns=["Palabra","Frecuencia"])
        st.bar_chart(df.set_index("Palabra"))
    else:
        st.write("No se encontraron palabras destacadas.")
    # Frases destacadas
    st.subheader("🛡️ Frases Destacadas")
    if frases:
        for i, frase in enumerate(frases, 1):
            st.markdown(f"**{i}.** {frase}")
    else:
        st.write("No se encontraron frases.")

# ----------------------------------------
# Lógica principal: carga y análisis
# ----------------------------------------
def main():
    if modo == "Texto directo":
        texto = st.text_area("Escribe o pega el texto del reino aquí:", height=200)
        if st.button("Analizar"):
            if texto:
                palabras_ordenadas, _ = contar_palabras(texto)
                sent, subj, frases, orig, trad = procesar_texto(texto)
                mostrar_resultados(sent, subj, palabras_ordenadas, frases)
            else:
                st.warning("Debes introducir algún texto.")
    else:
        archivo = st.file_uploader("Carga un archivo de texto (.txt):", type=["txt"])
        if archivo:
            contenido = archivo.read().decode("utf-8")
            if st.button("Analizar Archivo"):
                palabras_ordenadas, _ = contar_palabras(contenido)
                sent, subj, frases, orig, trad = procesar_texto(contenido)
                mostrar_resultados(sent, subj, palabras_ordenadas, frases)

if __name__ == "__main__":
    main()

# ----------------------------------------
# Pie de página señorial
# ----------------------------------------
st.markdown("---")
st.markdown("👑 Desarrollado por la Corte de Datos 2025")```

