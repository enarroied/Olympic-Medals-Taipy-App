import plotly.express as px

from algorithms.context import MedalColorMap


def _create_bar_medal_season(
    df_medals_season, season, medal_colors: MedalColorMap = MedalColorMap()
):
    fig = px.bar(
        df_medals_season,
        x="Olympiad",
        y="Medal_count",
        color="Medal_type",
        color_discrete_map=medal_colors.as_dict(),
        title="Medal Count by Olympiad and Medal Type",
        labels={"Medal_count": "Medal Count", "Olympiad": "Olympiad"},
        category_orders={"Olympiad": df_medals_season["Olympiad"].unique()},
    )
    if season != "winter":
        fig.add_annotation(
            text="(*) Stockholm 1956: only equestrian games",
            font=dict(color="black", size=10),
            showarrow=False,
            xref="paper",
            yref="paper",
            x=0,  # Centered horizontally
            y=-1,  # Below the chart (adjust as needed)
            xanchor="left",
            yanchor="bottom",
            bgcolor="#E5F9FC",
            bordercolor="#c7c7c7",
            borderwidth=1,
            borderpad=4,
            opacity=0.8,
        )
    return fig


def create_bar_medals(df_medals_by_olympiad, season):
    """Creates a plotly bar chart with total olympic medals (broken by medal color).
        The dataframe is previously filtered by season (summer / winter).

    Args:
        df_medals_by_olympiad (pd.DataFrame): data with all the olympic medals.
        season (str): ""All", "winter" or "summer".

    Returns:
       px.bar: A plotly bar chart to display in the Taipy app
    """
    if season != "All":
        df_medals_season = df_medals_by_olympiad[
            df_medals_by_olympiad["Olympic_season"] == season
        ].reset_index(drop=True)
    else:
        df_medals_season = df_medals_by_olympiad

    return _create_bar_medal_season(df_medals_season, season)
