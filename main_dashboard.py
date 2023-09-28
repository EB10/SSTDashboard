import pandas as pd
import plotly.graph_objects as go
import plotly.io as pio
import streamlit as st
from plotly.subplots import make_subplots
from PIL import Image
import time
import locale
import base64


@st.cache_data
def load_excel(file_path):
    return pd.read_excel(file_path)

locale.getlocale()

locale.setlocale(locale.LC_TIME, 'da_DK.UTF-8')

st.set_page_config(layout="wide")

image = Image.open(r"SSTLogo.png")

def get_image_base64(image):
    with open(image, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode('utf-8')

image_base64 = get_image_base64(r"SSTLogo.png")

st.markdown(
    f'<a href="https://sst.dk" target="_blank">\
        <img src="data:image/png;base64,{image_base64}" width="200">\
    </a>',
    unsafe_allow_html=True
)


st.title('Tidslinje over covid-19')
st.markdown('<style>h1 {font-size: 100px;font-family: Arial, sans-serif;}</style>', unsafe_allow_html=True)


pio.renderers.default = "browser"
st.sidebar.title("Vejledning til brug af tidslinjen")

st.sidebar.markdown(
    'Velkommen til Sundhedsstyrelsens overblik over covid-19 i Danmark. Denne side giver dig mulighed for at undersøge data '
    'over tid og efter begivenheder og data på udviklingen.\n\n Visningen bygger på meget data. Det kan derfor tage mellem 15-30 sekunder at indlæse, når du filtrerer. Du kan se indlæsningsstatus i højre øverste hjørne på siden.  \n\n'
    '### Sådan bruger du appen:\n'
    '- **Zoom på datoer:** Du kan zoome ind på specifikke datoer på to måder:  \n'
    '  - **Ved hjælp af datofilteret:** Vælg den ønskede datointerval i datofilteret for at zoome ind på et bestemt tidsrum.  \n'
    '  - **Ved at markere et område på grafen:** Træk for at markere det tidsrum, du ønsker at fokusere på, direkte på grafen.  \n'
    '- **Nulstil visningen:** For at nulstille visningen og se alle data igen, kan du klikke på "Genstart visningen" herunder.  \n\n'
    '### Filtrer efter emner:\n'
    'Vælg specifikke emner, såsom restriktioner eller vaccinationsindsats, for at fokusere visningen af begivenheder. '
    'Tidslinjen viser begivenheder sorteret efter vigtighed, fra kategori 1 (mest vigtige) til kategori 4 (mindst vigtige). '
    'Som standard vises kun begivenheder i kategori 1.  \n\n'
    'Tidslinjen præsenterer både vigtige begivenheder og kvantitative daglige data, som antal indlagte og smittede. '
    'Dette giver dig en detaljeret oversigt over udviklingen i den valgte periode.', unsafe_allow_html=True)


df = load_excel(r"Begivenheder_appdata.xlsx")
df_HaendelsesData = load_excel(r"Samlet.xlsx")

df.columns = df.columns.str.strip()
df_HaendelsesData.coumns = df.columns.str.strip()
samlet_data = df
df_HaendelsesData['Dato'] = pd.to_datetime(df_HaendelsesData['Dato'])

df = df[df["Dobbelt"] != 1]
df = df[df['Vigtig'] != 0]
min_date = df['Dato'].min()
max_date = df['Dato'].max()

df['størrelse'] = 20 / df['Vigtig']

df['størrelse'] = df['størrelse'].round().astype(int)

color_mapping_df = {
    1: '#003F36',
    2: '#FFDC3C',
    3: '#00D79B',
    4: '#FF7896'
}


df['color'] = df['Vigtig'].map(color_mapping_df)
legend_text = '<div style="font-size:14px;">Vigtighedsniveauer:'
for value, color in color_mapping_df.items():
    legend_text += f"{value}: " + f'<span style="color:{color};">●</span>'
st.sidebar.markdown(legend_text +'<br><br>' , unsafe_allow_html=True)

if st.sidebar.button('Genstart visningen'):
    st.markdown('<meta http-equiv="refresh" content="0">', unsafe_allow_html=True)




start_date = st.sidebar.date_input('Startdato', min_date)
end_date = st.sidebar.date_input('Slutdato', max_date)


if start_date > end_date:
    st.warning('End date should be after the start date.')
    st.stop()
df["Dato"] = pd.to_datetime(df["Dato"])
selected_date = (start_date, end_date)
start = selected_date[0]
slut = selected_date[1]
start = pd.to_datetime(start)
slut = pd.to_datetime(slut)
samlet_data = samlet_data[(samlet_data["Dato"] >= pd.to_datetime(start)) & (samlet_data["Dato"] <= pd.to_datetime(slut))]

df = df[(df["Dato"] >= pd.to_datetime(start)) & (df["Dato"] <= pd.to_datetime(slut))]

df_HaendelsesData = df_HaendelsesData[(df_HaendelsesData["Dato"] >= pd.to_datetime(start)) & (df_HaendelsesData["Dato"] <= pd.to_datetime(slut))]


df['CustomLabel'] = df['Vigtig'].map(lambda x: x + 0.5)
Labels = []
Labels.append("Alle begivenheder")
for kategori in df['Kategori'].unique():
    if kategori != "Udgivelser":
        Labels.append(kategori)


selected_y_value = st.sidebar.multiselect("Vælg begivenhedskategori", Labels, default="Alle begivenheder")

VigtighedLabels = []
VigtighedLabels.append("Alle begivenheder")

VigtighedLabels = list(df['Vigtig'].unique())

valgte_vigtigheder = st.sidebar.multiselect("Vælg vigtighed", VigtighedLabels, default=[1])

if valgte_vigtigheder:
    df = df[df["Vigtig"].isin(valgte_vigtigheder)]
else:
    df = df.copy()


if "Alle begivenheder" not in selected_y_value:
    selected_y_value = list(set(selected_y_value))
    df = df[df["Kategori_filter"].isin(selected_y_value)]
else:
    df = df.copy()

selected_data = st.sidebar.multiselect(
    "Vælg statistik på dagsniveau",
    ['Antal indlagte i alt', 'Antal indlagte på intensiv', 'Antal indlagte i respirator', 'Antal vaccinationsstik', 'Antal PCR-test', 'Antal positive PCR-test'],
    default=['Antal indlagte i alt']
)

y_order = ["Udgivelser","Øvrige tiltag","Vaccinationsindsats","Test og smitteforebyggelse", "Sundhedsvæsen","Restriktioner", 'Epidemiologisk udvikling'  ]
order_mapping = {category: i for i, category in enumerate(y_order)}
df = df.copy()
df['order'] = df['Kategori'].map(order_mapping)
df = df.sort_values('order')
color_mapping = {
    'Antal indlagte i alt': 'rgba(0, 100, 300, 0.6)',
    'Antal indlagte på intensiv ': 'rgba(100, 0, 300, 0.6)',
    'Antal indlagte i respirator': 'rgba(300, 100, 0, 0.6)',
    'Antal vaccinationsstik': 'rgba(0, 200, 100, 0.6)',
    'Antal PCR-test': 'rgba(100, 200, 0, 0.6)',
    'Antal positive PCR-test': 'rgba(200, 0, 100, 0.6)'

}

def update_plot(selected_date):


    fig = go.Figure()

    for i, row in df.iterrows():

        fig.add_trace(go.Scatter(
            x=[row['Dato']],
            y=[row['Kategori']],
            mode="lines+markers",
            name=f"Event {i+1}",
            text=f"{row['Dato'].date()}<br>{row['Beskrivelse']}",
            hoverinfo="text",
            line=dict(width=6),
                marker=dict(size=row['størrelse'], color = row['color'], symbol = "circle", opacity = 0.7),
            hoverlabel=dict(font=dict(size=30), bgcolor = "white")
        ))
        fig.update_layout(
         title="Tidslinje over vigtige nyheder",title_font=dict(size=50),
         xaxis=dict(title="Dato", type = "date", tickfont = dict(size = 28,color = "black")),
         yaxis=dict( tickfont = dict(size = 28, color = "black"), categoryorder="array",
            categoryarray=y_order),
         showlegend=False,
         height=630,
         width = 1800,
     )
    fig.update_xaxes(
        showgrid=True,
        gridwidth=1,
        gridcolor='Black',
    )


    return fig


def create_test_graph(data):
    fig2 = make_subplots(specs=[[{"secondary_y": True}]])

    for GrafiskDataPunkt in selected_data:
        fig2.add_trace(
            go.Scatter(
                x=data['Dato'],
                y=data[GrafiskDataPunkt],
                mode='lines',
                fill='tozeroy',
                fillcolor=color_mapping[GrafiskDataPunkt].replace("0.6", "0.2"),  # Use a lighter shade for fill
                line=dict(color=color_mapping[GrafiskDataPunkt]),
                hoverinfo='x+y',
                hoverlabel=dict(font=dict(size=40), bgcolor="white"),
                name=GrafiskDataPunkt  # Name to show in legend
            ),
            secondary_y=False
        )
    fig2.update_layout(
        title="Antal indlagte", titlefont = dict(size =28),
        xaxis=dict(title='Dato', titlefont = dict(size =28, color = "black"), showgrid = True, gridcolor = 'black'),
        yaxis=dict(title="Antal", gridcolor = "black", titlefont = dict(size =28, color = "black"), tickformat = "."),
        xaxis_tickangle=-45,
        showlegend=True,
        height=630,
        width=1800,
        legend=dict(x=0.1, y=1.0),
        xaxis_tickfont = dict(size = 28, color = "black"),
        yaxis_tickfont = dict(size=28, color = "black"),
        margin=dict(l=300, r=0),


    )

    return fig2




div_element_titel = """
<div>Tidslinje over Corona</div>
"""

# Create the Streamlit app
st.markdown('<style>.div_element_title {font-size: 200px;}</style>', unsafe_allow_html=True)


container1 = st.container()

hide_default_format = """
       <style>
       #MainMenu {visibility: hidden; }
       footer {visibility: hidden;}
       </style>
       """
st.markdown(hide_default_format, unsafe_allow_html=True)


def combined_plot_with_layout(data, selected_date, selected_data):
    # Create individual figures
    fig = update_plot(selected_date)
    fig2 = create_test_graph(data)

    # Create a combined figure with shared x-axes
    fig_combined = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.1)

    # Add traces from fig to the combined figure
    for trace in fig.data:
        trace.showlegend = False
        fig_combined.add_trace(trace)

    # Add traces from fig2 to the combined figure
    for trace in fig2.data:
        fig_combined.add_trace(trace, row=2, col=1)

    # Update the layout based on the layouts of fig and fig2
    fig_combined.update_layout(
        title = f"Begivenhedsoverblik og udvikling i daglig statistik",
        title_font = dict(size = 50, family="Arial, sans-serif"),
        xaxis2=dict(
            showgrid=True,
            gridcolor='Black',
            tickfont=dict(size=28, color="black"),
            tickformat="%d-%m-%y",


        ),
        xaxis=dict(
            title_font = dict(size=50),
            showgrid=True,
            gridcolor='Black',
            tickfont=dict(size=28, color="black")),
        yaxis=dict(
           tickfont=dict(size=28, color="black")
        ),
        yaxis2=dict(tickformat = ".",
            title=f"Antal indlagte",
            gridcolor="black",
            titlefont=dict(size=28, color="black"), tickfont =dict(size=28, color="black")
        ),
        height=1260,
        width=1800,
        margin=dict(l=300, r=0),
        font = dict(family="Arial, sans-serif",
        size=28,
        color="black"), legend=dict(
        x=0.5,
        y=-0.1,
        xanchor='center',
        yanchor='top',
        orientation='h',
            font = dict(size = 35)
    )
    )

    return fig_combined


with st.spinner('Indlæser data - vent venligst!'):
    time.sleep(20)

#st.text_area("Sundhedsstyrelsens covid-19 tidslinje dækker perioden fra den 5. januar 2020 og frem til den 5. maj 2023. Det er muligt at zoome ind og ud på både et bestemt tidsrum og et specifikt emne, man ønsker at undersøge. Tidslinjen indeholder derfor både en filterfunktion på datoer og på temaer såsom restriktioner, vaccinationsindsats og mere. Det er også muligt at vælge, hvilket vigtighedsniveau tidslinjen skal vise. Alle begivenheder er opdelt på vigtighedsniveauer fra 1 (mest vigtige) til 4 (mindst vigtige). Hvis intet andet angives, viser tidslinjen udelukkende begivenheder med den højeste vigtighed (vigtighedskategori 1)")




combined_figure = combined_plot_with_layout(df_HaendelsesData, selected_date, selected_data)
st.plotly_chart(combined_figure)

