"""
Module for visualizing Olympic medal by Olympics.

This module defines the MedalsByOlympics class, which filter the dataset by
Olympiad. The`create_medals_by_olympics` method returns a bar chart with all
medals awarded for a each Olympic committee.

Used by `all_time_medals.py`.
"""

from typing import Optional

import pandas as pd
import plotly.express as px
from plotly.graph_objs import Figure

from algorithms.context import MedalColorMap


class MedalsByOlympics:
    """Handles data aggregation and generates a bar chart by Olympiad."""

    def __init__(
        self,
        df_grouped_medals_olympiads: pd.DataFrame,
        medal_colors: Optional[MedalColorMap] = None,
    ):
        """Initialize the MedalsByOlympics class with aggregated medal data."""
        self.df_grouped_medals_olympiads = df_grouped_medals_olympiads.copy()
        self.medal_colors = medal_colors or MedalColorMap()

    def create_medals_by_olympics(self, olympiad: str) -> Figure:
        """
        Generates a Plotly bar chart displaying the count of Gold, Silver, and
        Bronze medals won by each Committee (Nation) for a specific Olympiad.

        Args:
            olympiad (str): Olympic event to visualize (e.g., 'Rio 2016').
                            Pass the special string "All" to include all Olympiads.

        Returns:
            plotly.graph_objects.Figure: An interactive Plotly bar chart figure object.
                                         Returns empty fig if data retrieval fails.
        """
        df_medals_to_plot = self._generate_data_by_olympics(olympiad)
        return self._plot_by_committee(df_medals_to_plot)

    def _generate_data_by_olympics(self, olympiad: str) -> pd.DataFrame:
        """
        Retrieves medal data for a specific Olympiad.

        Args:
            olympiad (str): ""All", or name of the Olympiad.

        Returns:
            pd.DataFrame: The DataFrame to plot, with medals awarded to each Nation
            by Olympic game. Returns an empty DataFrame on failure.
        """
        try:
            return self._compute_data_by_olympics(olympiad)
        except Exception as e:
            print(f"Error filtering data: {e}")
            print(self.df_grouped_medals_olympiads.head(3))
            return pd.DataFrame()

    def _plot_by_committee(self, df_aggregated: pd.DataFrame) -> Figure:
        """Generate a grouped bar chart of medal counts by committee."""
        fig = px.bar(
            df_aggregated,
            x="Committee",
            y=["Gold", "Silver", "Bronze"],
            barmode="group",
            orientation="v",
            color_discrete_map=self.medal_colors.as_dict(),
            labels={"value": "Count", "variable": "Medal Type"},
            title="Count of Gold, Silver, Bronze Medals by Committee",
        )
        fig.update_layout(xaxis={"title": "Committee"}, yaxis={"title": "Count"})
        return fig

    def _compute_data_by_olympics(self, olympiad: str) -> pd.DataFrame:
        """
        Filters the aggregated medals DataFrame for a specific Olympiad and
        cleans the resulting data for plotting.

        Args:
            olympiad (str): The name of the Olympiad to filter by.

        Returns:
            pd.DataFrame: A filtered DataFrame containing medal counts ('Gold',
                         'Silver', 'Bronze') grouped by 'Committee' for the
                         specified Olympiad, with the 'Olympiad' column dropped.
        """
        df_medals_to_plot = self.df_grouped_medals_olympiads.copy()
        df_medals_to_plot = df_medals_to_plot[df_medals_to_plot["Olympiad"] == olympiad]
        df_medals_to_plot = df_medals_to_plot.drop(columns="Olympiad")
        return df_medals_to_plot
