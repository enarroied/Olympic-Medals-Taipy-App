import pandas as pd
import plotly.express as px
from algorithms.context import MedalColorMap


class MedalsBySeason:
    def __init__(self, df_medals_season, medal_colors=None):
        self.df_medals_season = df_medals_season.copy()
        self.medal_colors = medal_colors or MedalColorMap()

    def _plot_bar_medal_season(
        self,
        df_medals_filtered_by_season,
        season,
    ):
        fig = px.bar(
            df_medals_filtered_by_season,
            x="Olympiad",
            y="Medal_count",
            color="Medal_type",
            color_discrete_map=self.medal_colors.as_dict(),
            title="Medal Count by Olympiad and Medal Type",
            labels={"Medal_count": "Medal Count", "Olympiad": "Olympiad"},
            category_orders={
                "Olympiad": df_medals_filtered_by_season["Olympiad"].unique()
            },
        )
        if season != "winter":
            fig.add_annotation(
                text="(*) Stockholm 1956: only equestrian games",
                font=dict(color="black", size=10),
                showarrow=False,
                xref="paper",
                yref="paper",
                x=0,  # Centered horizontally
                y=-1,  # Below the chart
                xanchor="left",
                yanchor="bottom",
                bgcolor="#E5F9FC",
                bordercolor="#c7c7c7",
                borderwidth=1,
                borderpad=4,
                opacity=0.8,
            )
        return fig

    def _compute_medals_by_season(self, season):
        """Creates a plotly bar chart with total olympic medals (broken by medal color).
            The dataframe is previously filtered by season (summer / winter).

        Args:
            df_medals_by_olympiad (pd.DataFrame): data with all the olympic medals.
            season (str): ""All", "winter" or "summer".

        Returns:
        px.bar: A plotly bar chart to display in the Taipy app
        """

        if season != "All":
            return self.df_medals_season[
                self.df_medals_season["Olympic_season"] == season
            ].reset_index(drop=True)
        else:
            return self.df_medals_season

    def _generate_medals_by_season(self, season):
        """
        Generate the medals DataFrame filtered by season, w/ erro handling.

        Args:
            season (str): "All", "winter", or "summer".

        Returns:
            pd.DataFrame: Filtered DataFrame or empty DataFrame if an error occurs.
        """
        try:
            return self._compute_medals_by_season(season)
        except Exception as e:  # plot_total_medals_by_country_both_seasons,
            print(f"Error filtering data: {e}")
            print(self.df_medals_season.head(3))
            return pd.DataFrame()

    def create_bar_medal_season(self, season):
        """
        Generate and plot the medal distribution for a given Olympic season.

        Args:
            season (str): "All", "winter", or "summer".

        Returns:
            plotly.graph_objs.Figure: Plotly bar chart showing medals per Olympiad.
        """
        df_season = self._generate_medals_by_season(season)
        return self._plot_bar_medal_season(df_season, season)
