import streamlit as st
import pandas as pd
import plotly.graph_objects as go


def udpate_plot(
    df_country_indicators, xaxis, xaxis_type, yaxis, yaxis_type, year, country_color
):
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
    st.plotly_chart(fig, use_container_width=True)

    st.markdown(
        "- Source: [Plolty dataset](https://github.com/plotly/datasets/blob/master/country_indicators.csv)"
    )


def main():
    st.title("Key Indicators")

    df_country_indicators = pd.read_csv(
        "https://plotly.github.io/datasets/country_indicators.csv"
    )
    all_axis_options = list(df_country_indicators["Indicator Name"].unique())

    col1, col2 = st.columns([3, 1])
    # xaxis widget
    xaxis_widget = col1.selectbox(
        options=all_axis_options,
        index=all_axis_options.index("Industry, value added (% of GDP)"),
        label="Xaxis :",
    )

    xaxis_type_widget = col2.radio(options=["linear", "log"], index=1, label="")

    # xaxis widget
    yaxis_widget = col1.selectbox(
        options=all_axis_options,
        index=all_axis_options.index("Services, etc., value added (% of GDP)"),
        label="Yaxis :",
    )

    yaxis_type_widget = col2.radio(options=["linear", "log"], index=0, label="")

    col1_a, col2_a = st.columns([1, 3])

    year_slider_widget = col1_a.slider(
        label="Year: ",
        value=2007,
        min_value=int(df_country_indicators["Year"].min()),
        max_value=int(df_country_indicators["Year"].max()),
        step=5,
    )

    country_color_widget = col2_a.multiselect(
        options=df_country_indicators["Country Name"].unique(),
        default=[
            "Canada",
            "United States",
            "Mexico",
            "India",
            "China",
            "United Kingdom",
            "Norway",
            "Germany",
        ],
        label="Color: ",
    )

    udpate_plot(
        df_country_indicators,
        xaxis_widget,
        xaxis_type_widget,
        yaxis_widget,
        yaxis_type_widget,
        year_slider_widget,
        country_color_widget,
    )


if __name__ == "__main__":
    main()
