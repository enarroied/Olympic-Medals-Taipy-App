import pandas as pd
import plotly.express as px


class MedalMap:
    """Handles data aggregation and choropleth map generation for Olympic medals
    by host country."""

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

    def _compute_medal_counts(self, season: str, medal_type: str) -> pd.DataFrame:
        """Filters, groups, and aggregates medal counts from the raw data."""
        medal_column = self._select_medal_column(medal_type)
        df_filtered = self.df_olympic_cities

        if season != "All":
            df_filtered = df_filtered[df_filtered["Olympic_season"] == season]
        country_counts = (
            df_filtered.groupby(["Country", "ISO_code_mapping"], observed=True)[
                medal_column
            ]
            .sum()
            .reset_index(name="Number of Medals")
        )
        return country_counts

    def _generate_medal_counts(self, season, medal_type):
        """
        Generate the medals DataFrame filtered by season, w/ erro handling.

        Args:
            season (str): "All", "winter", or "summer".

        Returns:
            pd.DataFrame: Filtered DataFrame or empty DataFrame if an error occurs.
        """
        try:
            return self._compute_medal_counts(season, medal_type)
        except Exception as e:
            print(f"Error filtering data: {e}")
            print(self.df_olympic_cities.head(3))
            return pd.DataFrame()

    def _plot_map_medals_by_country(
        self, country_counts: pd.DataFrame, season: str, medal_type: str
    ):
        """Internal helper: create the Plotly choropleth figure."""
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

    def create_olympic_medals_by_country(self, season: str, medal_type: str):
        """
        Retrieves filtered data and generates a choropleth map.
        """
        country_counts = self._generate_medal_counts(season, medal_type)
        return self._plot_map_medals_by_country(country_counts, season, medal_type)
