import plotly.express as px
from utils.report_generator import create_report
from pages.landing import show_landing
from agents.executive_agent import generate_executive_summary
from agents.chat_agent import chat_with_dataset
from utils.column_detector import detect_columns
from agents.visualization_agent import plan_visualizations
from agents.dataset_agent import understand_dataset
from agents.insight_agent import generate_insights
from agents.data_agent import analyze_data
import os
import pandas as pd
import streamlit as st

@st.dialog("📄 Export Report")
def export_report_dialog():
    st.subheader(":material/description: Report Details")
    default_title = (
    uploaded_file.name.rsplit(".", 1)[0]
    if uploaded_file is not None
    else "InsightAI Report"
)
    report_title = st.text_input(
    "Report Title",
    value=default_title,
    placeholder="Enter report title..."
)
    report_subtitle = st.text_input(
    "Subtitle (Optional)",
    placeholder="e.g., AI-Powered Data Analytics Report"
)
    st.divider()

    st.subheader(":material/checklist: Include in Report")

    include_summary = st.checkbox(
    "Executive Summary",
    value=True
)

    include_kpis = st.checkbox(
    "KPI Overview",
    value=True
)

    has_charts = any(
    card.get("created", False)
    for card in st.session_state.get("cards", [])
)
    include_charts = st.checkbox(
    "Charts",
    value=has_charts,
    disabled=not has_charts,
    help="Create at least one chart before exporting."
)
    
    has_ai_insights = st.session_state.ai_insights is not None

    include_insights = st.checkbox(
    "AI Insights",
    value=has_ai_insights,
    disabled=not has_ai_insights,
    help="Generate AI Business Insights before exporting."
)
    st.divider()

    st.subheader(":material/palette: Report Theme")

    report_theme = st.radio(
    "Choose a report style",
    ["Professional", "Modern", "Minimal"],
    horizontal=True,
    label_visibility="collapsed"
)
    st.divider()

    generate_report = st.button(
    ":material/picture_as_pdf: Generate Report",
    type="primary",
    use_container_width=True,
)

    if generate_report:

        pdf = create_report(
    title=report_title,
    subtitle=report_subtitle,
    dataset_name=uploaded_file.name if uploaded_file else "Unknown Dataset",
    executive_summary=executive_summary if include_summary else None,
    summary=st.session_state.summary,
    charts=st.session_state["cards"] if include_charts else [],
)

        st.success("Report generated successfully!")

        st.download_button(
        label=":material/download: Download Report",
        data=pdf,
        file_name=f"{report_title.replace(' ', '_')}.pdf",
        mime="application/pdf",
        use_container_width=True,
    )

@st.cache_data
def load_data(uploaded_file):
    uploaded_file.seek(0)
    return pd.read_csv(uploaded_file)
@st.cache_data
def get_detected_columns(df):
    return detect_columns(df)
st.set_page_config(
    page_title="InsightAI",
    page_icon="🤖",
    layout="wide"
)

CHART_COLOR = "#C99A1C"
def load_css():

    with open("styles.css") as f:

        st.markdown(
            f"<style>{f.read()}</style>",
            unsafe_allow_html=True
        )

load_css()
st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined" rel="stylesheet">
""", unsafe_allow_html=True)

if "show_dashboard" not in st.session_state:
    st.session_state.show_dashboard = False
uploaded_file = None

if "show_upload" not in st.session_state:
    st.session_state.show_upload = False

if "ai_insights" not in st.session_state:
    st.session_state.ai_insights = None

if "executive_summary" not in st.session_state:
    st.session_state.executive_summary = None

st.markdown("""
<style>

.block-container{

    max-width:95%;

    padding-top:1rem;

    padding-left:2rem;

    padding-right:2rem;

    padding-bottom:2rem;

}

</style>
""", unsafe_allow_html=True)


with st.sidebar:

    st.markdown(
    """
    <div style="text-align:center;">
        <h2 style="margin-bottom:4px;color:#8B5E00;">
            InsightAI
        </h2>
        <p style="margin-top:0;color:#8A7A62;font-size:14px;">
            AI-Powered Data Analytics Platform
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

    st.divider()

    st.subheader(":material/monitoring: System Status")

    st.success(":material/check_circle: Gemini Connected")
    st.success(":material/check_circle: Dataset Ready")
    st.success(":material/check_circle: Report Center Ready")

    st.divider()

    st.subheader(":material/folder_open: Supported Files")

    st.markdown("""
- :material/check_circle: CSV
- :material/schedule: Excel *(Coming Soon)*
- :material/schedule: JSON *(Coming Soon)*
""")
def landing_page():

#######################################################
# TOP SECTION
#######################################################

    hero_left, hero_right = st.columns([1.15, 0.85],gap='large')

    with hero_left:

        st.markdown("""
    <div class="landing-hero">

<div class="landing-tag">
Welcome to
</div>

<h1 class="landing-title">
InsightAI
</h1>

<div class="landing-subtitle">
Agentic AI-Powered Data Analyst
</div>

<div class="landing-description">
Upload your dataset and let AI uncover meaningful insights,
patterns and opportunities.
</div>

</div>
    """, unsafe_allow_html=True)

    with hero_right:

             st.image(
        "assets/hero_ai.png",
        use_container_width=True
    )

# ==========================
# TOP SECTION
# ==========================
if st.session_state.show_upload:
    upload_container = st.container()

    metric1, metric2, metric3, metric4, metric5 = st.columns(5)

#######################################################
# Upload Card
#######################################################

    st.markdown("""
<div class="section-header">

<div class="section-title">

<span class="material-symbols-outlined">
folder_open
</span>

<h2>Upload Dataset</h2>

</div>

</div>
""", unsafe_allow_html=True)
    uploaded_file = None
    uploaded_file = st.file_uploader(
    "",
    type=["csv"],
    label_visibility="collapsed"
)

    st.markdown(
    "<div style='height:12px'></div>",
    unsafe_allow_html=True
)

    c1,c2,c3,c4,c5=st.columns(5)

    if uploaded_file is not None:

            df = pd.read_csv(uploaded_file)
            st.session_state.df = df
            summary = analyze_data(df)
            st.session_state.summary = summary
            rows = summary["rows"]
            columns = summary["columns"]
            missing = summary["missing_values"]
            duplicates = summary["duplicates"]

            quality = round(
        (1 - (missing + duplicates)/(rows * columns)) * 100,
        1
    )


    else:

            rows = "--"
            columns = "--"
            missing = "--"
            duplicates = "--"
            quality = "98"


    cards = [
    ("table_rows", "Rows", rows, "Total Records"),
    ("view_column", "Columns", columns, "Dataset Fields"),
    ("warning", "Missing", missing, "Needs Review"),
    ("content_copy", "Duplicates", duplicates, "Duplicate Rows"),
    ("verified_user", "Quality", f"{quality}%", "Data Health"),
]

    for col, card in zip([c1, c2, c3, c4, c5], cards):

            with col:

                st.markdown(f"""
<div class="kpi-card">

<div class="kpi-icon">
 <span class="material-symbols-outlined">
        {card[0]}
    </span>
</div>

<div class="kpi-title">
        {card[1]}  
</div>

<div class="kpi-value">
        {card[2]}
</div>

<div class="kpi-subtitle">
        {card[3]}
</div>

</div>
""", unsafe_allow_html=True)
    st.markdown(
    "<div style='height:18px'></div>",
    unsafe_allow_html=True
)
    if uploaded_file is not None:
            st.divider()

            left, center, right = st.columns([2, 1, 2])

            with center:

                if st.button(
    ":material/analytics: Analyze Dataset",
    use_container_width=True,
    type="primary"
):
                    st.session_state.uploaded_filename = uploaded_file.name
                    st.session_state.show_dashboard = True
                    st.rerun()

if not st.session_state.show_upload:
    show_landing()

if st.session_state.show_dashboard:
    
    st.markdown("""
<div class="nav-title">

<h3>Workspace</h3>

<p>Navigate between dashboard modules</p>

</div>
""", unsafe_allow_html=True)
    tab1, tab2, tab3, tab4 = st.tabs([
    ":material/dashboard: Dashboard",
    ":material/analytics: Analytics",
    ":material/psychology: AI Insights",
    ":material/smart_toy: Copilot"
])
    st.markdown(
    "<div style='height:20px'></div>",
    unsafe_allow_html=True
)
    # -------------------------
    # OVERVIEW TAB
    # -------------------------
    with tab1:

        st.markdown(f"""
<div class="dataset-preview-card">

<div class="dataset-preview-header">

<span class="material-symbols-outlined">
table_view
</span>

<div>

<h3>{st.session_state.uploaded_filename}</h3>

<p>
Showing first 20 of
<strong>{st.session_state.summary['rows']}</strong>
records •
<strong>{st.session_state.summary['columns']}</strong>
columns
</p>

</div>

</div>

</div>
""", unsafe_allow_html=True)

        st.dataframe(
    st.session_state.df.head(20),
    use_container_width=True,
    height=500
)
        
        
    

        st.markdown("""
<div class="section-header">

<div class="section-title">
<span class="material-symbols-outlined">
analytics
</span>

<h2>Executive Summary</h2>
</div>

</div>
""", unsafe_allow_html=True)

        col1, col2 = st.columns(2)

        with col1:

            with st.spinner("Generating executive summary..."):
                try:
                        executive_summary = generate_executive_summary(st.session_state.df)
                except Exception:
                    executive_summary = """
    Dataset uploaded successfully.

    AI Executive Summary temporarily unavailable.

    Recommended Analysis:
    • Trend Analysis
    • Distribution Analysis
    • Correlation Analysis
    • Business Insights
    """


            st.session_state.executive_summary = executive_summary
            st.info(executive_summary)

        columns = get_detected_columns(st.session_state.df)

        numeric_count = len(columns["numeric"])
        categorical_count = len(columns["categorical"])

        with col2:
            st.success(f"""
### Analysis Ready

📈 Numeric Columns: {numeric_count}

📋 Categorical Columns: {categorical_count}

🎯 Recommended Analysis:
• Trend Analysis
• Distribution Analysis
• Correlation Analysis
• AI-Powered Insights
""")
    # -------------------------
    # VISUAL ANALYTICS TAB
    # -------------------------
    def create_visualization_card(index, card, df):
        
        card_container = st.container(border=True)
        
        with card_container:
           
        # Header
            title_col,delete_col = st.columns([9,1.2], vertical_alignment="center")

            with title_col:
                col_title, col_edit = st.columns([9, 1])

                with col_title:
                    st.markdown(f"### 📈 {card.get('title', f'Chart {index+1}')}")

                with col_edit:
                    if st.button(
            ":material/edit:",
            key=f"edit_chart_{index}",
            help="Rename chart"
        ):
                        card["editing"] = True

            with delete_col:
               
                if st.button(
                ":material/delete:",
                key=f"delete_{index}"
            ):

                    st.session_state["cards"].pop(index)
                    st.rerun()

            if card.get("editing", False):
                new_title = st.text_input(
        "Chart Name",
        value=card.get("title", f"Chart {index+1}"),
        key=f"rename_chart_{index}"
    )

                action1, action2, _ = st.columns([1, 1, 8])

                with action1:
                    if st.button(
        ":material/check:",
        key=f"save_chart_{index}",
        help="Save",
        use_container_width=True,
    ):
                        card["title"] = new_title
                        card["editing"] = False
                        st.rerun()

                with action2:
                    if st.button(
        ":material/close:",
        key=f"cancel_chart_{index}",
        help="Cancel",
        use_container_width=True,
    ):
                        card["editing"] = False
                        st.rerun()                  
            st.markdown(
    "<div style='height:6px'></div>",
    unsafe_allow_html=True
)

            columns = get_detected_columns(df)

            numeric_cols = columns["numeric"]
            categorical_cols = columns["categorical"]
            date_cols = columns.get("datetime", [])

            smart_categories = [
        col for col in categorical_cols
    if "id" not in col.lower()
    and "name" not in col.lower()
    and df[col].nunique() <= 20
]

            smart_numeric = [
    col for col in numeric_cols
    if "id" not in col.lower()
]
            
            col1, col2, col3 = st.columns([1,1,1],gap='medium')
            

            with col1:
                st.markdown("**Chart Type**")
                chart_type = st.selectbox(
        "",
        ["Bar", "Pie", "Line", "Scatter", "Histogram"],
        index=["Bar","Pie","Line","Scatter","Histogram"].index(card["type"]),
        key=f"type_{index}",
        label_visibility="collapsed",
        width="stretch"
    )

            card["type"] = chart_type
        
            if chart_type == "Bar":

                with col2:
                    st.markdown("**Category**")
                    x = st.selectbox(
            "",
            smart_categories,
            key=f"x_{index}",
            label_visibility="collapsed",
            width="stretch"
        )
                with col3:
                    st.markdown("**Value**")
                    y = st.selectbox(
            "",
            ["Count"] + smart_numeric,
            key=f"y_{index}",
            label_visibility="collapsed",
            width="stretch"
        )

        
            elif chart_type == "Pie":

                with col2:
                    st.markdown("**Category**")
                    x = st.selectbox(
            "",
            smart_categories,
            key=f"x_{index}",
            label_visibility="collapsed",
            width="stretch"
        )
                y = None
            
            elif chart_type == "Line":

                with col2:
                    st.markdown("**X Axis**")
                    x = st.selectbox(
            "",
            date_cols + smart_numeric,
            key=f"x_{index}",
            label_visibility="collapsed",
            width="stretch"
        )
                with col3:
                    st.markdown("**Y Axis**")
                    y = st.selectbox(
            "",
            smart_numeric,
            key=f"y_{index}",
            label_visibility="collapsed",
            width="stretch"
        )

            

            elif chart_type == "Scatter":

                with col2:
                    st.markdown("**X Axis**")
                    x = st.selectbox(
            "",
            smart_numeric,
            key=f"x_{index}",
            label_visibility="collapsed",
            width="stretch"
        )   
                with col3:
                    st.markdown("**Y Axis**")
                    y = st.selectbox(
            "",
            smart_numeric,
            key=f"y_{index}",
            label_visibility="collapsed",
            width="stretch"
        )



            elif chart_type == "Histogram":


                with col2:
                    st.markdown("**Numeric Column**")
                    x = st.selectbox(
            "",
            smart_numeric,
            key=f"x_{index}",
            label_visibility="collapsed",
            width="stretch"
        )

                    y = None
                  

            card["x"] = x
            card["y"] = y
            card['type']=chart_type
            if x is not None:

                if chart_type in ["Pie", "Histogram"]:

                    card["created"] = True

                elif y is not None:

                    card["created"] = True

                else:

                    card["created"] = False   

                    



            if (
    card["created"]
    and card["x"] is not None
    and (
        card["type"] in ["Pie", "Histogram"]
        or card["y"] is not None
    )
):

                x = card["x"]
                y = card["y"]
                chart_type = card["type"]

        
                if chart_type == "Bar":

                    if y == "Count":

                        chart_data = (
            df[x]
            .value_counts()
            .reset_index()
        )

                        chart_data.columns = [x, "Count"]

                        fig = px.bar(
            chart_data,
            x=x,
            y="Count",
            color_discrete_sequence=[CHART_COLOR]
        )

                    else:

                        chart_data = (
            df.groupby(x)[y]
            .sum()
            .reset_index()
        )

                        fig = px.bar(
            chart_data,
            x=x,
            y=y,
            color_discrete_sequence=[CHART_COLOR]
        )
                
                elif chart_type == "Line":
                    if x == y:
                        fig = px.line(df, y=y)
                    else:

                        chart_data = (
        df.groupby(x)[y]
        .sum()
        .reset_index()
    )
                    

                        fig = px.line(
        chart_data,
        x=x,
        y=y
    )
                

                    fig.update_traces(
        line_color=CHART_COLOR
    )           
                elif chart_type == "Pie":

                    chart_data = (
        df[x]
        .value_counts()
        .reset_index()
    )

                    chart_data.columns = [x, "Count"]

                    fig = px.pie(
        chart_data,
        names=x,
        values="Count",
        color_discrete_sequence=[
        "#355070",  # Navy
        "#6D597A",  # Mauve
        "#B56576",  # Rose
        "#E56B6F",  # Salmon
        "#EAAC8B",  # Peach
        "#2A9D8F",  # Teal
        "#457B9D",  # Blue
        "#A8DADC",  # Light Cyan
        "#E9C46A",  # Gold
        "#264653"   # Dark Teal
    ]
    )
                elif chart_type == "Scatter":

                    fig = px.scatter(
        df,
        x=x,
        y=y,
        color_discrete_sequence=[CHART_COLOR]
    )
           
                elif chart_type == "Histogram":

                    fig = px.histogram(
        df,
        x=x,
        color_discrete_sequence=[CHART_COLOR]
    )
                fig.update_layout(
    template="simple_white",
    paper_bgcolor="#FFFDF8",
    plot_bgcolor="#FFFDF8",
    height=280,
    margin=dict(l=10, r=10, t=5, b=10),
    title_text=""
)
                #os.makedirs("temp_charts", exist_ok=True)

                #chart_path = f"temp_charts/chart_{index}.png"

                #fig.write_image(chart_path, scale=2)

                card["figure"] = fig
                st.plotly_chart(
    fig,
    use_container_width=True,
    config={
        "displaylogo": False,
        "displayModeBar": "hover",
        "modeBarButtonsToRemove": [
            "lasso2d",
            "select2d",
            "zoomIn2d",
            "zoomOut2d",
            "autoScale2d",
            "resetScale2d",
        ],
        "toImageButtonOptions": {
            "format": "png",
            "filename": card["title"],
            "scale": 3,
        },
    },
)
                st.markdown("""
<div style="
padding-top:10px;
">
""", unsafe_allow_html=True)

                
            else:
                
                    st.markdown(
    """
    <div style="text-align:center;color:#8A7A62;padding:40px;">
        <span class="material-symbols-outlined"
              style="font-size:56px;color:#C99A1C;">
            bar_chart
        </span>
        <br><br>
        <b>No chart generated</b><br>
        Configure the chart and click <b>Generate Chart</b>
    </div>
    """,
    unsafe_allow_html=True
)
 
    with tab2:

        header_col, export_col = st.columns([8, 2], vertical_alignment="center")

        with header_col:
            st.title(":material/bar_chart: Visualization Workspace")
            st.caption("Create, compare and manage interactive charts.")

        with export_col:
            export_clicked = st.button(
        ":material/picture_as_pdf: Export Report",
        key="export_report",
        type="primary",
        use_container_width=True,
    )
        if export_clicked:
             export_report_dialog()

        if "cards" not in st.session_state:
            st.session_state["cards"] = []
        

        for row in range(0, len(st.session_state["cards"]), 2):

                left, right = st.columns(2, gap="large")

    # Left Card
                with left:
                    create_visualization_card(
        row,
        st.session_state["cards"][row],
        st.session_state.df
    )

    # Right Card
                if row + 1 < len(st.session_state["cards"]):

                 with right:
                    create_visualization_card(
        row + 1,
        st.session_state["cards"][row + 1],
        st.session_state.df
    )


        left, center1, center2, right = st.columns([3, 1.3, 1.3, 3])

        with center1:
            if st.button(
         ":material/add: Add Chart",
        key="add_chart",
        type="primary",
        use_container_width=True
    ):

                st.session_state["cards"].append({
    "title": f"Chart {len(st.session_state['cards'])+1}",
    "type": "Bar",
    "x": None,
    "y": None,
    "created": False
})
                st.rerun()

                
        with center2:
            if st.button(
        ":material/refresh: Reset Cards",
        key="reset_cards",
        use_container_width=True
    ):
                    st.session_state["cards"] = []
                    st.rerun()

            
        
    #-----------------------------------------------
    with tab3:

        col1, col2 = st.columns(2)

        with col1:

            st.subheader(":material/psychology: Dataset Understanding Agent")

            if st.button("Understand Dataset"):

                with st.spinner("Understanding dataset..."):

                    try:

                        dataset_analysis = understand_dataset(st.session_state.df)

                    except Exception:

                        dataset_analysis = f"""
### Dataset Summary

- Rows: {st.session_state.summary['rows']}
- Columns: {st.session_state.summary['columns']}
- Missing Values: {st.session_state.summary['missing_values']}
- Duplicates: {st.session_state.summary['duplicates']}

AI quota reached.

Showing local dataset analysis instead.
"""

                st.markdown(dataset_analysis)

        with col2:

            st.subheader(":material/lightbulb: AI Business Insights")

            if st.button("Generate Insights"):

                with st.spinner("Analyzing dataset..."):

                    try:

                        insights = generate_insights(st.session_state.summary)

                    except Exception:

                        insights = f"""
### Business Insights

✅ Dataset contains **{st.session_state.summary['rows']} records**

✅ Dataset contains **{st.session_state.summary['columns']} columns**

✅ Missing Values: **{st.session_state.summary['missing_values']}**

✅ Duplicates: **{st.session_state.summary['duplicates']}**

### Recommended Analysis

- Trend Analysis
- Distribution Analysis
- Correlation Analysis
- Customer Segmentation
- Predictive Modeling

AI quota reached.

Showing rule-based insights instead.
"""
                st.session_state.ai_insights = insights
                st.markdown(insights)
# ------------------------- #
#  CHAT TAB 
# # -------------------------
    with tab4:

        st.subheader(":material/chat: Chat With Your Dataset")

        st.write("### :material/help: Suggested Questions")

        user_question = None

        col1, col2, col3 = st.columns(3)

        with col1:
            if st.button(":material/summarize: Dataset Summary"):
                user_question = "Summarize this dataset"

        with col2:
            if st.button(":material/insights: Key Insights"):
             user_question = "What are the key insights in this dataset?"

        with col3:
            if st.button(":material/error: Missing Values"):
                user_question = "Are there any missing values in this dataset?"

        col4, col5, col6 = st.columns(3)

        with col4:
            if st.button(":material/analytics: Recommended Analysis"):
             user_question = "What analysis would you recommend for this dataset?"

        with col5:
            if st.button(":material/verified: Data Quality Report"):
                user_question = "Evaluate the data quality of this dataset"

        with col6:
            if st.button(":material/table_view: Explain Columns"):
                user_question = "Explain the columns in this dataset"

        custom_question = st.text_input(
        "Or ask your own question"
    )

        if custom_question:
            user_question = custom_question

        if user_question:

            with st.spinner("Thinking..."):

                try:

                    answer = chat_with_dataset(
                    st.session_state.df,
                    user_question
                )

                except Exception:

                    answer = f"""
### Local Response

Question: {user_question}

Dataset Statistics:

- Rows: {st.session_state.summary['rows']}
- Columns: {st.session_state.summary['columns']}
- Missing Values: {st.session_state.summary['missing_values']}
- Duplicates: {st.session_state.summary['duplicates']}

AI quota may have been reached.

Basic dataset information is still available.
"""

            st.markdown("### :material/smart_toy: AI Response")
            st.markdown(answer) 