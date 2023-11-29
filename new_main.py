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
st.sidebar.title("Filtrering af data")

def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

local_css("style.css")

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
st.markdown('<style>#tidslinje-over-sundhedsstyrelsens-h-ndtering-af-covid-19 {font-size: 50px; font-family: Raleway, sans-serif;}</style>', unsafe_allow_html=True)

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


size_mapping = {
    1: 20,
    2: 16,
    3: 14,
    4: 12
}

df['størrelse'] = df['Vigtig'].map(size_mapping)

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
unique_categories = df['Kategori'].unique()
Labels = ["Alle begivenheder"] + [kategori for kategori in unique_categories if kategori != "Udgivelser"]


selected_y_value = st.sidebar.multiselect("Vælg begivenhedskategori", Labels, default="Alle begivenheder")

VigtighedLabels = []
VigtighedLabels.append("Alle begivenheder")

VigtighedLabels = list(df['Vigtig'].unique())

valgte_vigtigheder = st.sidebar.multiselect("Vælg betydningsniveau", VigtighedLabels, default=[1])
valgte_vigtigheder = set(valgte_vigtigheder)

# Filter df if valgte_vigtigheder is not empty, else use it as is
df = df[df["Vigtig"].isin(valgte_vigtigheder)] if valgte_vigtigheder else df


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
    'Antal indlagte på intensiv': 'rgba(100, 0, 300, 0.6)',
    'Antal indlagte i respirator': 'rgba(300, 100, 0, 0.6)',
    'Antal vaccinationsstik': 'rgba(0, 200, 100, 0.6)',
    'Antal PCR-test': 'rgba(100, 200, 0, 0.6)',
    'Antal positive PCR-test': 'rgba(200, 0, 100, 0.6)'

}

color_mapping_df = {
    1: '#003F36',
    2: '#FFDC3C',
    3: '#00D79B',
    4: '#FF7896'
}


df['color'] = df['Vigtig'].map(color_mapping_df)
# Add a title and some text explaining what the app does

search_df = df[['Dato', 'Beskrivelse', 'Vigtig', 'Kategori', 'Kategori_filter', 'Kilde', 'Link']]

search_df = df[['Dato', 'Beskrivelse', 'Vigtig', 'Kategori', 'Kategori_filter', 'Kilde', 'Link']].rename(columns={
    'Vigtig': 'Betydningsniveau',
    'Kategori': 'Overordnet kategori',
    'Kategori_filter': 'Underordnet kategori'
}).reset_index(drop=True)









def main():


    

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

    with st.expander("Datavisninger over begivenheder og smitteudvikling"):
        st.markdown('<div class="title-font">Her kan du se og analysere data.</div>', unsafe_allow_html=True)
        
        def update_plot(selected_date):
            fig = go.Figure()
        
            # Create a list of trace dictionaries
            trace_dicts = df.apply(lambda row: dict(
                type='scatter',
                x=[row['Dato']],
                y=[row['Kategori']],
                mode="lines+markers",
                name=f"Event {row.name+1}",
                text=f"{row['Dato'].date()}<br>{row['Beskrivelse']}",
                hoverinfo="text",
                line=dict(width=6),
                marker=dict(size=row['størrelse'], color=row['color'], symbol=row['Stjerne'], opacity=0.7),
                hoverlabel=dict(font=dict(size=30), bgcolor="white")
            ), axis=1).tolist()
        
            # Add all traces in bulk
            for trace_dict in trace_dicts:
                fig.add_trace(go.Scatter(trace_dict))
        
            return fig
        
        
        def create_test_graph(data):
            fig2 = make_subplots(specs=[[{"secondary_y": True}]])
        
            # Add all traces at once using a list comprehension
            traces = [
                go.Scatter(
                    x=data['Dato'],
                    y=data[GrafiskDataPunkt],
                    mode='lines',
                    fill='tozeroy',
                    fillcolor=color_mapping[GrafiskDataPunkt].replace("0.6", "0.2"),
                    line=dict(color=color_mapping[GrafiskDataPunkt]),
                    hoverinfo='x+y',
                    hoverlabel=dict(font=dict(size=40), bgcolor="white"),
                    name=GrafiskDataPunkt
                )
                for GrafiskDataPunkt in selected_data
            ]
        
            # Add the list of traces to the figure
            fig2.add_traces(traces, rows=[1] * len(traces), cols=[1] * len(traces), secondary_ys=[False] * len(traces))
        
            return fig2
        
        
        
        
        
        hide_default_format = """
               <style>
               #MainMenu {visibility: hidden; }
               footer {visibility: hidden;}
               </style>
               """
        st.markdown(hide_default_format, unsafe_allow_html=True)
        
        
        def combined_plot_with_layout(data, selected_date, selected_data):
            with st.spinner('Opdaterer data - vent venligst...'):
                success_message_placeholder = st.empty()
                # Create individual figures
                fig = update_plot(selected_date)
                fig2 = create_test_graph(data)
        
                # Create a combined figure with shared x-axes
                fig_combined = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.1)
        
                # Add traces from fig to the combined figure without showing their legend
                for trace in fig.data:
                    trace.showlegend = False
                    fig_combined.add_trace(trace, row=1, col=1)
        
                # Add traces from fig2 to the combined figure
                for trace in fig2.data:
                    fig_combined.add_trace(trace, row=2, col=1)
        
                # Define common layout settings
                common_layout = dict(
                    height=1260,
                    width=1800,
                    margin=dict(l=0, r=0),
                    font=dict(family="Arial, sans-serif", size=28, color="black"),
                    legend=dict(x=0.5, y=-0.1, xanchor='center', yanchor='top', orientation='h', font=dict(size=35))
                )
        
                # Update the layout based on the layouts of fig and fig2, and apply common settings
                fig_combined.update_layout(
                    title=f"Begivenhedsoverblik og udvikling i daglig statistik",
                    title_font=dict(size=35, family="Arial, sans-serif"),
                    separators="*.,*",
                    xaxis2=dict(tickfont=dict(size=28, color="black"), tickformat="%d-%m-%y", showgrid=True, gridcolor='Black'),
                    xaxis=dict(tickfont=dict(size=28, color="black"), tickformat="%d-%m-%y", showgrid=True, gridcolor='Black',
                               showticklabels=True),
                    yaxis=dict(tickfont=dict(size=28, color="black"), tickformat=" ,"),
                    yaxis2=dict(tickformat=" ,", title="Antal", gridcolor="black", titlefont=dict(size=28, color="black"),
                                tickfont=dict(size=28, color="black")),
                    **common_layout
                )
                # Display the success message
                success_message_placeholder.success('Data blev opdateret og vises om 5-10 sekunder')
        
                # Sleep for a few seconds to display the message
                time.sleep(3)  # Adjust the number of seconds as needed
        
                # Clear the success message
                success_message_placeholder.empty()
        
        
            return fig_combined
        
        legend_html = "<div style='margin-bottom: 2rem;'><h4>Betydningsniveauer</h4>"
        for value, color in color_mapping_df.items():
            legend_html += f"<span style='color:{color}; font-size: 32px; margin-right: 10px;'>●</span> {value}<br>"
        legend_html += "<span style='font-size: 32px;'>★</span> Milepæl</div>"
        st.markdown(legend_html, unsafe_allow_html=True)
        combined_figure = combined_plot_with_layout(df_HaendelsesData, selected_date, selected_data)
        st.plotly_chart(combined_figure)
        
           

if __name__ == "__main__":
    main()
