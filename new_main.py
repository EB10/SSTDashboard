import streamlit as st

import pandas as pd
import plotly.graph_objects as go
import plotly.io as pio
import streamlit as st
from plotly.subplots import make_subplots
from PIL import Image
import time
import locale
import base64
from io import BytesIO


@st.cache_data
def load_excel(file_path):
    return pd.read_excel(file_path)

st.set_page_config(layout="wide")

image = Image.open(r"SSTLogo.png")

def get_image_base64(image):
    with open(image, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode('utf-8')

image_base64 = get_image_base64(r"SSTLogo.png")

st.markdown(
    f'<a href="https://www.sst.dk/da/corona" target="_blank">\
        <img src="data:image/png;base64,{image_base64}" width="300">\
    </a>',
    unsafe_allow_html=True
)



st.title('Tidslinje over Sundhedsstyrelsens håndtering af covid-19')
st.markdown('<style>h1 {font-size: 50px;font-family: Raleway, sans-serif;}</style>', unsafe_allow_html=True)

pio.renderers.default = "browser"



df = load_excel(r"Begivenheder_appdata1.xlsx")
df_HaendelsesData = load_excel(r"Samlet.xlsx")


df.columns = df.columns.str.strip()
df_HaendelsesData.coumns = df.columns.str.strip()
samlet_data = df
df_HaendelsesData['Dato'] = pd.to_datetime(df_HaendelsesData['Dato'])

df = df[df['Vigtig'] != 0]
min_date = df['Dato'].min()
max_date = df['Dato'].max()

import streamlit as st

def main():
    st.markdown("""
        <style>
        .big-font {
            font-size:30px !important;
        }
        .title-font {
            font-size:24px !important;
            font-weight:bold;
        }
        </style>
        """, unsafe_allow_html=True)

    st.markdown('<div class="big-font">Velkommen til Sundhedsstyrelsens overblik over covid-19 i Danmark. Denne side giver dig mulighed for at undersøge data "\
            "over tid og efter begivenheder og data på udviklingen.\n\n Visningen bygger på meget data. Det kan derfor tage mellem 15-30 sekunder at indlæse, når du filtrerer. Du kan se indlæsningsstatus i højre øverste hjørne på siden.  \n\n"\
            "**Sådan bruger du appen:**\n"\
            "- **Zoom på datoer:** Du kan zoome ind på specifikke datoer på to måder:\n"\
            "  - **Ved hjælp af datofilteret:** Vælg den ønskede datointerval i datofilteret for at zoome ind på et bestemt tidsrum.\n"\
            "  - **Ved at markere et område på grafen:** Træk for at markere det tidsrum, du ønsker at fokusere på, direkte på grafen.\n"\
            "**Nulstil visningen:** For at nulstille visningen og se alle data igen, kan du klikke på 'Genstart visningen' herunder.\n\n"\
            "**Filtrer efter emner:**\n"\
            "Vælg specifikke emner, såsom restriktioner eller vaccinationsindsats, for at fokusere visningen af begivenheder. "\
            "Tidslinjen viser begivenheder sorteret efter betydningsgrad, fra kategori 1 (mest betydningsfuld) til kategori 4 (mindst betydningsfuld). "\
            "Som standard vises kun begivenheder i kategori 1.\n\n"\
            "Tidslinjen præsenterer både vigtige begivenheder og kvantitative daglige data, som antal indlagte og smittede. "\
            "Dette giver dig en detaljeret oversigt over udviklingen i den valgte periode.</div>', unsafe_allow_html=True)

    with st.expander(""):
        st.markdown('<div class="title-font">Introduktion</div>', unsafe_allow_html=True)
        # Resten af din introduktionstekst

    with st.expander(""):
        st.markdown('<div class="title-font">Data Side</div>', unsafe_allow_html=True)
        # Resten af din datasidetekst

    with st.expander(""):
        st.markdown('<div class="title-font">Søgeside</div>', unsafe_allow_html=True)
        # Resten af din søgesidetekst

if __name__ == "__main__":
    main()

