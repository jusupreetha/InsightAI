import plotly.express as px

def sales_by_region(df):

    sales_region = df.groupby("Region")["Sales"].sum().reset_index()

    fig = px.bar(
        sales_region,
        x="Region",
        y="Sales",
        title="Sales by Region"
    )

    return fig