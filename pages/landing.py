import streamlit as st
from components.hero import show_hero
from components.cta import show_cta
from components.features import show_features
from components.workflow import show_workflow

def show_landing():
    show_hero()

    st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)
    show_features()

    st.markdown("<br>", unsafe_allow_html=True)
    show_workflow()

    st.markdown("<br>", unsafe_allow_html=True)
    
