import streamlit as st

# Her kan du definere yderligere funktioner og importere nødvendige biblioteker

def main():
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Vælg en side:", ["Introduktion", "Data Side", "Søgeside"])

    if page == "Introduktion":
        vis_introduktion()
    elif page == "Data Side":
        vis_data_side()
    elif page == "Søgeside":
        vis_søgeside()

def vis_introduktion():
    st.title("Velkommen til vores Streamlit App")
    st.markdown("""
    'Velkommen til Sundhedsstyrelsens overblik over covid-19 i Danmark. Denne side giver dig mulighed for at undersøge data '
    'over tid og efter begivenheder og data på udviklingen.\n\n Visningen bygger på meget data. Det kan derfor tage mellem 15-30 sekunder at indlæse, når du filtrerer. Du kan se indlæsningsstatus i højre øverste hjørne på siden.  \n\n'
    '### Sådan bruger du appen:\n'
    '- **Zoom på datoer:** Du kan zoome ind på specifikke datoer på to måder:  \n'
    '  - **Ved hjælp af datofilteret:** Vælg den ønskede datointerval i datofilteret for at zoome ind på et bestemt tidsrum.  \n'
    '  - **Ved at markere et område på grafen:** Træk for at markere det tidsrum, du ønsker at fokusere på, direkte på grafen.  \n'
    '- **Nulstil visningen:** For at nulstille visningen og se alle data igen, kan du klikke på "Genstart visningen" herunder.  \n\n'
    '### Filtrer efter emner:\n'
    'Vælg specifikke emner, såsom restriktioner eller vaccinationsindsats, for at fokusere visningen af begivenheder. '
    'Tidslinjen viser begivenheder sorteret efter betydningsgrad, fra kategori 1 (mest betydningsfuld) til kategori 4 (mindst betydningsfuld). '
    'Som standard vises kun begivenheder i kategori 1.  \n\n'
    'Tidslinjen præsenterer både vigtige begivenheder og kvantitative daglige data, som antal indlagte og smittede. '
    'Dette giver dig en detaljeret oversigt over udviklingen i den valgte periode.', unsafe_allow_html=True)
    """)

def vis_data_side():
    st.title("Data Side")
    # Her kan du indsætte logikken for datavisning, f.eks. ved at indlæse og vise data.
    st.markdown("Her kan du udforske og interagere med data.")

def vis_søgeside():
    st.title("Søgeside")
    # Her kan du indsætte logik for en søgefunktion, f.eks. en tekstboks til søgeforespørgsler.
    søgeord = st.text_input("Indtast søgeord")
    if søgeord:
        st.write(f"Resultater for søgningen: {søgeord}")
        # Her kan du tilføje logik for at vise søgeresultater

if __name__ == "__main__":
    main()
