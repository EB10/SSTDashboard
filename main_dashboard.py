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
if st.sidebar.button('Genstart visningen'):
    st.markdown('<meta http-equiv="refresh" content="0">', unsafe_allow_html=True)
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

st.markdown("""
    <style>
    .dataframe-widget .stDataFrame { 
        width: 100%; 
    }
    </style>
    """, unsafe_allow_html=True)

st.title('Tidslinje over Sundhedsstyrelsens håndtering af covid-19')
st.markdown('<style>#tidslinje-over-sundhedsstyrelsens-h-ndtering-af-covid-19 {font-size: 50px; font-family: Raleway, sans-serif;}</style>', unsafe_allow_html=True)

pio.renderers.default = "browser"



df = load_excel(r"Begivenheder_appdata2.xlsx")
df_HaendelsesData = load_excel(r"Samlet.xlsx")


df.columns = df.columns.str.strip()
df_HaendelsesData.coumns = df.columns.str.strip()
samlet_data = df
df_HaendelsesData['Dato'] = pd.to_datetime(df_HaendelsesData['Dato'])

df = df[df['Betydning'] != 0]
min_date = df['Dato'].min()
max_date = df['Dato'].max()


size_mapping = {
    1: 20,
    2: 16,
    3: 14,
    4: 12
}

df['størrelse'] = df['Betydning'].map(size_mapping)




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


df['CustomLabel'] = df['Betydning'].map(lambda x: x + 0.5)
unique_categories = df['Kategori'].unique()
Labels = ["Alle begivenheder"] + [kategori for kategori in unique_categories if kategori != "Udgivelser"]


selected_y_value = st.sidebar.multiselect("Vælg begivenhedskategori", Labels, default="Alle begivenheder")

BetydninghedLabels = []
BetydninghedLabels.append("Alle begivenheder")

BetydninghedLabels = list(df['Betydning'].unique())

valgte_Betydningheder = st.sidebar.multiselect("Vælg betydningsniveau", BetydninghedLabels, default=[1])
valgte_Betydningheder = set(valgte_Betydningheder)

# Filter df if valgte_Betydningheder is not empty, else use it as is
df = df[df["Betydning"].isin(valgte_Betydningheder)] if valgte_Betydningheder else df


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


df['color'] = df['Betydning'].map(color_mapping_df)
# Add a title and some text explaining what the app does

search_df = df[['Dato', 'Beskrivelse', 'Betydning', 'Kategori', 'Kategori_filter', 'Kilde', 'Link']]

search_df = df[['Dato', 'Beskrivelse', 'Betydning', 'Kategori', 'Kategori_filter', 'Kilde', 'Link']].rename(columns={
    'Betydning': 'Betydningsniveau',
    'Kategori': 'Overordnet kategori',
    'Kategori_filter': 'Underordnet kategori'
}).reset_index(drop=True)
search_df['Dato'] = search_df['Dato'].dt.date






def main():


    

    with st.expander("Introduktion", expanded=True):
        st.markdown("""
            <div style='font-size: 20px;'>
            Denne side giver dig mulighed for at genbesøge begivenheder relateret til myndighedshåndteringen af pandemien og dykke ned i historisk statistik på den epidemiologisk udvikling og vaccinationsindsatsen.<br>
            Visningen bygger på store mængder data. Det kan derfor tage mellem 15-30 sekunder for siden at indlæse, når du filtrerer og ændrer visningen af tidslinjen.<br>
            Når siden indlæser og opdaterer, fremgår et ikon for indlæsningsstatus i højre øverste hjørne på siden.<br>
            <h4>Sådan bruger du tidslinjen</h4>
            Den interaktive tidslinje kan findes under fanen <b>Tidslinje over begivenheder og smitteudvikling</b> herunder. Du kan klikke på fanen for at folde datavisningerne ud. Du kan frit tilpasse indholdet af tidslinjen ved brug af følgende funktioner, som du finder i menuen til venstre:<br><br>
            <b>1. Filtrer efter emner og betydning</b>Alle begivenheder og udgivelser er inddelt efter emne og betydning.<br>
            Fokuser søgningen på et eller flere specifikke begivenhedsemner ved at vælge en eller flere kategorier i feltet <b>Vælg begivenhedskategori i menuen til venstre for tidslinjen.</b><br>
            Du kan også fokusere din søgning efter begivenheders Betydninggennem valg i feltet <b>Vælg betydningsgrad</b> i menuen til venstre for tidslinjen. Her indikerer 1 de mest betydningsfulde begivenheder og 4 de mindst betydningsfulde begivenheder.<br><br>
            <b>2. Zoom på datoer</b> Du kan zoome ind på specifikke datoer ved at ændre på datointervallet til en særlig tidsperiode ved brug af felterne <b>Startdato</b> og <b>Slutdato</b> i menuen til venstre for tidslinjen.<br>
            Det er også muligt at zoome ind på et specifikt område af tidslinjen ved at markere det område, du ønsker at fokusere på direkte grafen.<br>
            Du zoomer ud igen ved at dobbeltklikke et vilkårligt sted på tidslinjen.<br><br>
            <b>3. Nulstil visningen</b>For at nulstille visningen og dermed dine valg af filtre for at se alle data igen, kan du klikke på <b>Genstart visningen</b> øverst til venstre på siden.<br><br>
            <b>4. Statistik på dagsniveau</b>Under tidslinjen fremgår en graf, der viser udvalgte statistikker på dagsniveau i samme periode som i tidslinjen. I feltet <b>Vælg statistik på dagsniveau</b> i menuen til venstre for tidslinjen har du mulighed for at vælge, hvilke statistikker du ønsker inkluderet i grafen.<br><br>
            <b>5. Søg efter specifikke begivenheder og udgivelser</b>Ønsker du et mere detaljeret indblik i specifikke begivenheder eller udgivelser, kan du anvende søgefeltet i fanen <b>Søg efter begivenheder og udgivelser.</b><br>
            Det er muligt at søge efter specifikke ord eller begivenheder i søgefeltet. Resultatet er en tabel med alle relevante begivenheder og udgivelser.<br>
            Nogle begivenheder har tilhørende links, som kan kopieres for at læse mere om den specifikke begivenhed. Udgivelser kan findes ved at søge efter titlen på Sundhedsstyrelsens hjemmeside www.sst.dk.<br>
            Vær opmærksom på at eventuelle valg af filtre til venstre på siden også påvirker resultaterne i søgetabellen.<br><br>
            Vi håber, at du går på opdagelse i vores tidslinje!
        </div>
        """, unsafe_allow_html=True)

    with st.expander("Tidslinje over begivenheder og smitteudvikling"):
        st.markdown("""<div style='font-size: 25px;'>Her kan du se og navigere rundt i data - benyt menuen til venstre for at filtrere. Du kan zoome ind på en periode i graferne enten ved at markere området i grafen eller ved at filtrere på datoer i menuen til venstre.<br>
        Den øverste graf viser alle begivenheder i den valgte tidsperiode fordelt på bevienhedskategorier og med markører for betydningsniveau. Du kan se, hvilke farver de forskellige begivenhedsniveauer angiver i menuen til venstre. ★-symbolet angiver de to største milepæle i perioden.<br> Den nederste graf angiver forskellige data på indlæggelser, tests og antal vaccinationsstik alt efter, hvad du har valgt i menuen til venstre. </div>'""", unsafe_allow_html=True)
        
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
                line=dict(width=20),
                marker=dict(size=row['størrelse'], color=row['color'], symbol=row['Stjerne'], opacity=0.7),
                hoverlabel=dict(font=dict(size=25), bgcolor="white")
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
                    #width=1800,
                    margin=dict(l=0, r=0),
                    font=dict(family="Raleway, sans-serif", size=28, color="black"),
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
                fig_combined.update_layout(autosize=True)
                # Display the success message
                success_message_placeholder.success('Data blev opdateret og vises om 5-10 sekunder')
        
                # Sleep for a few seconds to display the message
                time.sleep(3)  # Adjust the number of seconds as needed
        
                # Clear the success message
                success_message_placeholder.empty()
        
        
            return fig_combined

                
        legend_html = "<div style='margin-bottom: -1rem;'><span style='font-size: 25px; font-weight: bold;'>Betydningsniveauer i tidslinjen</span><br>"


        for value, color in color_mapping_df.items():
            legend_html += f"<span style='color:{color}; font-size: 52px; margin-top: 2px; margin-bottom: 2px;'>●</span> <span style='font-size: 25px;'>{value}</span><br>"

        legend_html += "<span style='font-size: 52px;'>★</span> <span style='font-size: 25px;margin-top: 2px; margin-bottom: 2px; '>Milepæl</span></div>"

        st.sidebar.markdown(legend_html, unsafe_allow_html=True)
            
        combined_figure = combined_plot_with_layout(df_HaendelsesData, selected_date, selected_data)
        st.plotly_chart(combined_figure)
        
    with st.expander("Søg efter begivenheder og udgivelser"):
        st.markdown("""<div style='font-size: 25px;'>Her kan du søge på specifikke ord, som du er interesseret i at se mere information på. Søgeresultatet er det bagvedliggende data til begivenhedstidslinjen. Bemærk at filtrene i menuen i venstre også sorterer i resultatet i denne søgefunktion. </div>'""", unsafe_allow_html=True)
        search_term = st.text_input("Angiv et søgeord her")

       
        if search_term:
            mask = search_df['Beskrivelse'].str.contains(search_term, na=False, case=False)
            search_term_df = search_df[mask]
            if not search_term_df.empty:
                st.write("Søgeresultater:")
                st.dataframe(search_term_df, hide_index=True)
            else:
                st.info("Ingen resultater fundet for din søgning.")
        else:
            st.info("Indtast et søgeord for begivenheder for at se resultater.")
        
        # Optional: Add some styling to the DataFrame display
        st.markdown("""
        <style>
        .dataframe {
            border: 1px solid #1e1e1e;
            border-radius: 5px;
            overflow: hidden;
            font-size: 0.85em;
        }
        </style>
        """, unsafe_allow_html=True)


           

if __name__ == "__main__":
    main()
