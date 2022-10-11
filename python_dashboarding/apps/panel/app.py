import panel as pn
import pandas as pd
import plotly.graph_objs as go


df_country_indicators = pd.read_csv(
    "https://plotly.github.io/datasets/country_indicators.csv"
)


xaxis_widget = pn.widgets.Select(
    options=list(df_country_indicators["Indicator Name"].unique()),
    name="Xaxis :",
    value="Industry, value added (% of GDP)",
)

xaxis_type_widget = pn.widgets.RadioBoxGroup(
    options=["linear", "log"], value="log", name="Xaxis type: ", inline=True
)

row_1 = pn.Row(xaxis_widget, xaxis_type_widget)

# xaxis widget
yaxis_widget = pn.widgets.Select(
    options=list(df_country_indicators["Indicator Name"].unique()),
    name="Yaxis :",
    value="Services, etc., value added (% of GDP)",
)

yaxis_type_widget = pn.widgets.RadioBoxGroup(
    options=["linear", "log"], value="linear", name="Xaxis type: ", inline=True
)

row_2 = pn.Row(yaxis_widget, yaxis_type_widget)

year_slider_widget = pn.widgets.IntSlider(
    name="Year",
    start=int(df_country_indicators["Year"].min()),
    end=int(df_country_indicators["Year"].max()),
    step=5,
    width=200,
    value=2007,
)

country_color_widget = pn.widgets.MultiSelect(
    name="Color: ",
    options=list(df_country_indicators["Country Name"].unique()),
    value=[
        "Canada",
        "United States",
        "Mexico",
        "India",
        "China",
        "United Kingdom",
        "Norway",
        "Germany",
    ],
    size=10,
)

row_3 = pn.Row(year_slider_widget, country_color_widget)


def udpate_plot(xaxis, xaxis_type, yaxis, yaxis_type, year, country_color):
    df_widget = df_country_indicators[(df_country_indicators["Year"] == year)]

    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            mode="markers",
            x=df_widget[
                (df_widget["Indicator Name"] == xaxis)
                & (~df_widget["Country Name"].isin(country_color))
            ]["Value"],
            y=df_widget[
                (df_widget["Indicator Name"] == yaxis)
                & (~df_widget["Country Name"].isin(country_color))
            ]["Value"],
            marker=dict(
                color="dimgrey", opacity=0.75, line=dict(color="darkgrey", width=1)
            ),
            showlegend=False,
            hoverinfo="text",
            hovertext=df_widget[
                (df_widget["Indicator Name"] == xaxis)
                & (~df_widget["Country Name"].isin(country_color))
            ]["Country Name"],
        )
    )

    fig.add_trace(
        go.Scatter(
            mode="markers",
            marker_symbol="hexagram",
            x=df_widget[
                (df_widget["Indicator Name"] == xaxis)
                & (df_widget["Country Name"].isin(country_color))
            ]["Value"],
            y=df_widget[
                (df_widget["Indicator Name"] == yaxis)
                & (df_widget["Country Name"].isin(country_color))
            ]["Value"],
            marker=dict(
                color="palevioletred", size=10, line=dict(color="darkred", width=1)
            ),
            showlegend=False,
            hoverinfo="text",
            hovertext=df_widget[
                (df_widget["Indicator Name"] == xaxis)
                & (df_widget["Country Name"].isin(country_color))
            ]["Country Name"],
        )
    )

    fig.update_xaxes(title=xaxis + " [" + xaxis_type + "]", type=xaxis_type)
    fig.update_yaxes(title=yaxis + " [" + yaxis_type + "]", type=yaxis_type)
    fig.update_layout(
        width=750,
        height=500,
        title="Country Indicators - " + str(year),
        paper_bgcolor="rgb(0,0,0,0)",
    )

    plotly_pane = pn.pane.Plotly(fig)

    return plotly_pane


bound_fn = pn.bind(
    udpate_plot,
    xaxis_widget,
    xaxis_type_widget,
    yaxis_widget,
    yaxis_type_widget,
    year_slider_widget,
    country_color_widget,
)

bound_fn()

pn.Column(row_1, row_2, row_3, bound_fn, background="WhiteSmoke").servable()
