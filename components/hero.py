import streamlit as st
from components.cta import show_cta

def show_hero():

    left, right = st.columns([1, 1.4], gap="large")
    with left:

        st.caption("WELCOME TO")

        st.title("InsightAI")

        st.subheader("Agentic AI-Powered Data Analytics Platform")

        st.write(
    """
    InsightAI is an AI-powered data analytics platform that helps you transform raw
    CSV datasets into meaningful insights. Upload your dataset to explore interactive
    dashboards, visualize trends, analyze patterns, and ask questions using Google
    Gemini-powered AI assistance.
    """
)

        st.markdown("""
- :material/upload_file: Upload CSV datasets instantly
- :material/dashboard: Explore interactive dashboards
- :material/analytics: Analyze trends and patterns
- :material/chat: Ask questions with Google Gemini
""")

    with right:

        st.image(
            "assets/hero_ai.png",
            use_container_width=True
        )
    st.write("")

    show_cta()