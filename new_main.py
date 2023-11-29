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

search_term = st.sidebar.text_input("Søg i nyheder og udgivelser")
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

def main():
    st.title("Fold-ud Sider med Expander i Streamlit")

    with st.expander("Introduktion"):
        st.write("Velkommen til denne Streamlit-app med fold-ud sider.")

    with st.expander("Data Side"):
        st.write("Her kan du se og analysere data.")

    with st.expander("Søgeside"):
        st.write("Brug denne side til at søge efter specifikke oplysninger.")

if __name__ == "__main__":
    main()
