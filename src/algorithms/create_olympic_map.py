import plotly.express as px


class MedalMap:
    """Handles sunburst data preparation and chart generation for medals by gender."""

    def __init__(self, df_olympic_cities):
        self.df_olympic_cities = df_olympic_cities.copy()

    def _select_medal_column(self, medal_type):
        """
        Helper function to select the appropriate medal column based on medal_type.

        Args:
            medal_type (str): The type of medal. One of "All", "Gold", "Silver",
            or "Bronze".

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
                "Invalid medal_type. Should be one of 'All', 'Gold', 'Silver',\
                    or 'Bronze'."
            )
        return medal_map[medal_type]

    def _create_map_medals_by_country(self, country_counts, season, medal_type):
        fig = px.choropleth(
            country_counts,
            locations="ISO_code_mapping",
            color="Number of Medals",
            hover_name="Country",
            color_continuous_scale=px.colors.sequential.Plasma,
            title=f"{medal_type.capitalize()} Olympic Medals awarded by Host Country\
            ({season.capitalize()})",
            projection="natural earth",
        )
        fig.update_geos(
            showcountries=True,
            showland=True,
            landcolor="lightgray",
            countrycolor="white",
        )
        return fig

    def plot_olympic_medals_by_country(self, season, medal_type):
        """
        Plot a choropleth map of Olympic medals by country for a specified season
        and medal type.

        Args:
            df_olympic_cities (pandas.DataFrame): DataFrame containing Olympic
            medals data.
            season (str): The season for which to plot the medals. Should be either
            "winter" or "summer".
            medal_type (str): The type of medal to count. Should be one of "All",
            "Gold", "Silver", or "Bronze".

        Returns:
            plotly.graph_objs._figure.Figure: Choropleth map figure.
        """
        medal_column = self._select_medal_column(medal_type)
        df_olympic_cities = self.df_olympic_cities
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
        return self._create_map_medals_by_country(country_counts, season, medal_type)
