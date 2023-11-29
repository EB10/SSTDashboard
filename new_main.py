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
        Denne app er designet til at give en interaktiv oplevelse med data.
        - **Data Side:** Her kan du udforske forskellige datasæt.
        - **Søgeside:** Brug denne side til at søge efter specifikke oplysninger.
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
