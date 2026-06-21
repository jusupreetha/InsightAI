import streamlit as st


def show_features():

    st.markdown("## Everything You Need to Analyze Data")

    st.caption(
        "Powerful AI capabilities designed to transform raw datasets into actionable insights."
    )

    st.write("")

    cards = [
    (
        ":material/summarize:",
        "Dataset Summary",
        "Generate concise summaries that help you quickly understand the structure and content of your dataset."
    ),
    (
        ":material/dashboard:",
        "Interactive Dashboards",
        "Create clean visual dashboards with charts that make exploring and presenting your data easier."
    ),
    (
        ":material/insights:",
        "Data Insights",
        "Identify patterns, trends, and key observations from your dataset through AI-assisted analysis."
    ),
    (
        ":material/chat:",
        "AI Assistant",
        "Ask questions about your uploaded dataset and receive contextual answers powered by Gemini."
    ),
]

    cols = st.columns(4, gap="large")

    for col, card in zip(cols, cards):

        with col:
            st.markdown(f"""
<div class="feature-card">

<div class="feature-icon">

<span class="material-symbols-outlined">
{card[0].replace(":material/","").replace(":","")}
</span>

</div>

<h3>{card[1]}</h3>

<p>{card[2]}</p>

</div>
""", unsafe_allow_html=True)

            