import plotly.express as px

from parameters.gender_category_colors import GenderCategoryColorMap
from parameters.medal_colors import MedalColorMap


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


def _create_bar_plot_by_committee(
    df_aggregated, medal_colors: MedalColorMap = MedalColorMap()
):
    fig = px.bar(
        df_aggregated,
        x=df_aggregated.index,
        y=["Gold", "Silver", "Bronze"],
        barmode="group",
        orientation="v",
        color_discrete_map=medal_colors.as_dict(),
        labels={"value": "Count", "variable": "Medal Type"},
        title="Count of Gold, Silver, Bronze Medals by Committee",
    )
    fig.update_layout(xaxis={"title": "Committee"}, yaxis={"title": "Count"})
    return fig


def create_bar_by_committee(df_medals, olympiad="All"):
    """Creates a plotly bar chart with total olympic medals (medal colorS by each other).
        The dataframe is previously filtered by season (summer / winter).

    Args:
        df_medals (pd.DataFrame): data with all the olympic medals.
        olympiad (str): ""All", or name of the Olympiad.

    Returns:
       px.bar: A plotly bar chart to display in the Taipy app
    """
    df_medals_by_committee = df_medals.copy()

    if olympiad != "All":
        df_medals_by_committee = df_medals_by_committee[
            df_medals_by_committee["Olympiad"] == olympiad
        ]
    # Aggregating data to get count of medals by Medal_type for each Committee
    df_aggregated = (
        df_medals_by_committee.groupby(["Committee", "Medal_type"], observed=True)
        .size()
        .unstack(fill_value=0)
    )
    # Sort DataFrame by count of gold and silver medals
    df_aggregated = df_aggregated.sort_values(by=["Gold", "Silver"], ascending=False)

    return _create_bar_plot_by_committee(df_aggregated)


def _select_medal_column(medal_type):
    """
    Helper function to select the appropriate medal column based on medal_type.

    Args:
        medal_type (str): The type of medal. One of "All", "Gold", "Silver", or "Bronze".

    Returns:
        str: The corresponding column name in the DataFrame.
    """
    medal_map = {
        "All": "total_medals",
        "Gold": "total_medals_gold",
        "Silver": "total_medals_silver",
        "Bronze": "total_medals_bronze",
    }
    if medal_type not in medal_map:
        raise ValueError(
            "Invalid medal_type. Should be one of 'All', 'Gold', 'Silver', or 'Bronze'."
        )
    return medal_map[medal_type]


def plot_olympic_medals_by_country(df_olympic_cities, season, medal_type):
    """
    Plot a choropleth map of Olympic medals by country for a specified season and medal type.

    Args:
        df_olympic_cities (pandas.DataFrame): DataFrame containing Olympic medals data.
        season (str): The season for which to plot the medals. Should be either "winter" or "summer".
        medal_type (str): The type of medal to count. Should be one of "All", "Gold", "Silver", or "Bronze".

    Returns:
        plotly.graph_objs._figure.Figure: Choropleth map figure.
    """
    medal_column = _select_medal_column(medal_type)

    if season != "All":
        df_olympic_cities = df_olympic_cities[
            df_olympic_cities["Olympic_season"] == season
        ]

    country_counts = (
        df_olympic_cities.groupby(["Country", "ISO_code_mapping"], observed=True)[
            medal_column
        ]
        .sum()
        .reset_index(name="Number of Medals")
    )

    fig = px.choropleth(
        country_counts,
        locations="ISO_code_mapping",
        color="Number of Medals",
        hover_name="Country",
        color_continuous_scale=px.colors.sequential.Plasma,
        title=f"{medal_type.capitalize()} Olympic Medals awarded by Host Country ({season.capitalize()})",
        projection="natural earth",
    )

    fig.update_geos(
        showcountries=True,
        showland=True,
        landcolor="lightgray",
        countrycolor="white",
    )
    return fig


def _create_sunburnst_medals(
    df_sunburst,
    selected_olympiad_for_sunburst,
    gender_category_colors: GenderCategoryColorMap = GenderCategoryColorMap(),
):
    fig = px.sunburst(
        df_sunburst,
        path=["Gender", "Discipline", "Event"],
        color="Gender",
        color_discrete_map=gender_category_colors.as_dict(),
        title=f"Total Medals by Gender, Discipline, and Event - {selected_olympiad_for_sunburst}",
    )
    return fig


def create_sunburnst_medals(
    df_sunburst,
    selected_olympiad_for_sunburst,
):
    if selected_olympiad_for_sunburst != "All":
        df_sunburst = df_sunburst[
            df_sunburst["Olympiad"] == selected_olympiad_for_sunburst
        ]
    return _create_sunburnst_medals(df_sunburst, selected_olympiad_for_sunburst)
