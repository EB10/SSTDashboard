import streamlit as st
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
