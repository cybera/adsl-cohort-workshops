from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

app = Dash(__name__)

df = pd.read_csv("https://plotly.github.io/datasets/country_indicators.csv")

app.layout = html.Div(
    [
        html.Div(html.H2("Key Indicators")),
        html.Div(
            [
                html.Div(
                    [
                        dcc.Dropdown(
                            df["Indicator Name"].unique(),
                            "Industry, value added (% of GDP)",
                            id="xaxis-column",
                        ),
                        dcc.RadioItems(
                            ["linear", "log"], "log", id="xaxis-type", inline=True
                        ),
                    ],
                    style={"width": "48%", "display": "inline-block"},
                ),
                html.Div(
                    [
                        dcc.Dropdown(
                            df["Indicator Name"].unique(),
                            "Services, etc., value added (% of GDP)",
                            id="yaxis-column",
                        ),
                        dcc.RadioItems(
                            ["linear", "log"], "linear", id="yaxis-type", inline=True
                        ),
                    ],
                    style={"width": "48%", "float": "right", "display": "inline-block"},
                ),
            ]
        ),
        dcc.Slider(
            df["Year"].min(),
            df["Year"].max(),
            step=None,
            id="year--slider",
            value=df["Year"].max(),
            marks={str(year): str(year) for year in df["Year"].unique()},
        ),
        dcc.Dropdown(
            options=df["Country Name"].unique(),
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
            id="country-color",
            multi=True,
        ),
        dcc.Graph(id="indicator-graphic"),
    ]
)


@app.callback(
    Output("indicator-graphic", "figure"),
    Input("xaxis-column", "value"),
    Input("yaxis-column", "value"),
    Input("xaxis-type", "value"),
    Input("yaxis-type", "value"),
    Input("year--slider", "value"),
    Input("country-color", "value"),
)
def update_graph(
    xaxis_column_name,
    yaxis_column_name,
    xaxis_type,
    yaxis_type,
    year_value,
    country_values,
):
    df_widget = df[df["Year"] == year_value]

    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            mode="markers",
            x=df_widget[
                (df_widget["Indicator Name"] == xaxis_column_name)
                & (~df_widget["Country Name"].isin(country_values))
            ]["Value"],
            y=df_widget[
                (df_widget["Indicator Name"] == yaxis_column_name)
                & (~df_widget["Country Name"].isin(country_values))
            ]["Value"],
            marker=dict(
                color="dimgrey", opacity=0.75, line=dict(color="darkgrey", width=1)
            ),
            showlegend=False,
            hoverinfo="text",
            hovertext=df_widget[
                (df_widget["Indicator Name"] == xaxis_column_name)
                & (~df_widget["Country Name"].isin(country_values))
            ]["Country Name"],
        )
    )

    fig.add_trace(
        go.Scatter(
            mode="markers",
            marker_symbol="hexagram",
            x=df_widget[
                (df_widget["Indicator Name"] == xaxis_column_name)
                & (df_widget["Country Name"].isin(country_values))
            ]["Value"],
            y=df_widget[
                (df_widget["Indicator Name"] == yaxis_column_name)
                & (df_widget["Country Name"].isin(country_values))
            ]["Value"],
            marker=dict(
                color="palevioletred", size=10, line=dict(color="darkred", width=1)
            ),
            showlegend=False,
            hoverinfo="text",
            hovertext=df_widget[
                (df_widget["Indicator Name"] == xaxis_column_name)
                & (df_widget["Country Name"].isin(country_values))
            ]["Country Name"],
        )
    )

    fig.update_xaxes(title=xaxis_column_name + " [" + xaxis_type + "]", type=xaxis_type)
    fig.update_yaxes(title=yaxis_column_name + " [" + yaxis_type + "]", type=yaxis_type)
    fig.update_layout(
        width=750, height=500, title="Country Indicators - " + str(year_value)
    )

    # fig = px.scatter(
    #     x=dff[dff["Indicator Name"] == xaxis_column_name]["Value"],
    #     y=dff[dff["Indicator Name"] == yaxis_column_name]["Value"],
    #     hover_name=dff[dff["Indicator Name"] == yaxis_column_name]["Country Name"],
    # )

    # fig.update_layout(margin={"l": 40, "b": 40, "t": 10, "r": 0}, hovermode="closest")

    # fig.update_xaxes(
    #     title=xaxis_column_name, type="linear" if xaxis_type == "Linear" else "log"
    # )

    # fig.update_yaxes(
    #     title=yaxis_column_name, type="linear" if yaxis_type == "Linear" else "log"
    # )

    return fig


if __name__ == "__main__":
    app.run_server(debug=True, host="0.0.0.0")
