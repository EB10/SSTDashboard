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

import streamlit as st

def main():
    st.markdown("""
        <style>
        .big-font {
            font-size:30px !important;
        }
        .title-font {
            font-size:20px !important;
            font-weight:bold;
        }
        </style>
        """, unsafe_allow_html=True)

    with st.expander("Introduktion", expanded=True):
        st.markdown("""
            <div class="big-font">
                Velkommen til Sundhedsstyrelsens overblik over covid-19 i Danmark. Denne side giver dig mulighed for at undersøge data over tid og efter begivenheder og data på udviklingen.<br><br>
                Visningen bygger på meget data. Det kan derfor tage mellem 15-30 sekunder at indlæse, når du filtrerer. Du kan se indlæsningsstatus i højre øverste hjørne på siden.<br><br>
                <b>Sådan bruger du appen:</b><br>
                - <b>Zoom på datoer:</b> Du kan zoome ind på specifikke datoer på to måder:<br>
                  - <b>Ved hjælp af datofilteret:</b> Vælg den ønskede datointerval i datofilteret for at zoome ind på et bestemt tidsrum.<br>
                  - <b>Ved at markere et område på grafen:</b> Træk for at markere det tidsrum, du ønsker at fokusere på, direkte på grafen.<br>
                <b>Nulstil visningen:</b> For at nulstille visningen og se alle data igen, kan du klikke på 'Genstart visningen'.<br><br>
                <b>Filtrer efter emner:</b><br>
                Vælg specifikke emner, såsom restriktioner eller vaccinationsindsats, for at fokusere visningen af begivenheder. 
                Tidslinjen viser begivenheder sorteret efter betydningsgrad, fra kategori 1 (mest betydningsfuld) til kategori 4 (mindst betydningsfuld). 
                Som standard vises kun begivenheder i kategori 1.<br><br>
                Tidslinjen præsenterer både vigtige begivenheder og kvantitative daglige data, som antal indlagte og smittede. 
                Dette giver dig en detaljeret oversigt over udviklingen i den valgte periode.
            </div>
            """, unsafe_allow_html=True)

    with st.expander("Data Side"):
        st.markdown('<div class="title-font">Her kan du se og analysere data.</div>', unsafe_allow_html=True)
        # Resten af din datasidetekst

    with st.expander("Søgeside"):
        st.markdown('<div class="title-font">Brug denne side til at søge efter specifikke oplysninger.</div>', unsafe_allow_html=True)
        # Resten af din søgesidetekst

if __name__ == "__main__":
    main()
