import streamlit as st

st.title("Aplicación Principal")

st.info("💡 Usa los botones para navegar entre páginas.")

# Botones de navegación
if st.button("Abrir Chatbot"):
    st.switch_page("pages/chatbot.py")

if st.button("Ir a CLU"):
    st.switch_page("pages/clu.py")
