import streamlit as st


def show_workflow():

    st.markdown("## How InsightAI Works")

    st.caption(
        "Analyze your dataset in four simple AI-powered steps."
    )

    steps = [
        (
            ":material/upload_file:",
            "Upload",
            "Upload your CSV dataset."
        ),
        (
            ":material/psychology:",
            "Understand",
            "AI understands your dataset."
        ),
        (
            ":material/analytics:",
            "Visualize",
            "Generate interactive charts."
        ),
        (
            ":material/insights:",
            "Discover",
            "Receive meaningful insights."
        ),
    ]
    st.write("")

    cols = st.columns(4, gap="large")

    for col, step in zip(cols, steps):

        with col:

            st.markdown(
            f"""
<div style="text-align:center;">

<span class="material-symbols-outlined"
style="
font-size:42px;
color:#C99A1C;
">
{step[0].replace(':material/','').replace(':','')}
</span>

<h4 style="margin-top:10px;">
{step[1]}
</h4>

<p style="
color:#6B5B4A;
font-size:15px;
">
{step[2]}
</p>

</div>
""",
            unsafe_allow_html=True
        )
    