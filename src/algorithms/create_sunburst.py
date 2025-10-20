"""
Module for visualizing medals awarded by Olympic Games, broken down by
gender and discipline.

This module defines the `SunburstByGender` class, which generates a
sunburst chart for analyzing medal distributions.

Used by `medals_by_committee.py`.
"""

from typing import Optional

import pandas as pd
import plotly.express as px
from algorithms.context import GenderCategoryColorMap
from plotly.graph_objs import Figure


class SunburstByGender:
    """Handles sunburst data preparation and chart generation for medals by gender."""

    def __init__(
        self,
        df_olympic_medals: pd.DataFrame,
        gender_colors: Optional[GenderCategoryColorMap] = None,
    ):
        """
        Initialize the SunburstByGender class.

        Args:
            df_olympic_medals (pd.DataFrame): DataFrame containing Olympic medal data.
            gender_colors (GenderCategoryColorMap, optional): Custom color map
            for genders. Defaults to a new GenderCategoryColorMap instance.
        """
        self.gender_colors = gender_colors or GenderCategoryColorMap()
        self.df_sunburst = self._make_initial_sunburst(df_olympic_medals)

    def _make_initial_sunburst(self, df_olympic_medals: pd.DataFrame) -> pd.DataFrame:
        """
        Prepare a DataFrame suitable for sunburst visualization.

        Args:
            df_olympic_medals (pd.DataFrame): Raw Olympic medals DataFrame containing
                at least ['Olympiad', 'Gender', 'Discipline', 'Event'] columns.

        Returns:
            pd.DataFrame: Processed DataFrame containing string representations of
            the necessary columns for building the sunburst chart.
        """
        return (
            df_olympic_medals[["Olympiad", "Gender", "Discipline", "Event"]]
            .astype(str)
            .copy()
        )

    def _compute_sunburst_data(
        self, selected_olympiad_for_sunburst: str = "All"
    ) -> pd.DataFrame:
        """
        Internal helper: returns the sunburst DataFrame filtered by Olympiad.

        Args:
            selected_olympiad_for_sunburst (str, optional): Olympiad name to filter by.
                Defaults to "All", which includes all Olympiads.

        Returns:
            pd.DataFrame: Filtered DataFrame ready for sunburst chart generation.
        """
        df_filtered = self.df_sunburst

        # Apply filtering by Olympiad if specified
        if selected_olympiad_for_sunburst != "All":
            df_filtered = df_filtered[
                df_filtered["Olympiad"] == selected_olympiad_for_sunburst
            ]
        return df_filtered

    def _plot_sunburst_medals(
        self, df_sunburst: pd.DataFrame, selected_olympiad_for_sunburst: str
    ) -> Figure:
        """
        Internal helper: create the Plotly sunburst figure.

        Args:
            df_sunburst (pd.DataFrame): The prepared DataFrame to visualize.
            selected_olympiad_for_sunburst (str): Olympiad name for title context.

        Returns:
            plotly.graph_objs.Figure: Plotly sunburst chart object.
        """
        fig = px.sunburst(
            df_sunburst,
            path=["Gender", "Discipline", "Event"],
            color="Gender",
            color_discrete_map=self.gender_colors.as_dict(),
            title=f"Total Medals by Gender, Discipline, and Event -\
                  {selected_olympiad_for_sunburst}",
        )
        return fig

    def create_sunburst_medals(
        self, selected_olympiad_for_sunburst: str = "All"
    ) -> Figure:
        """
        Creates a sunburst chart that breaks data for a Olympic game (or "ALl" of
        them) by gender and by event.

        Args:
            selected_olympiad_for_sunburst (str, optional): Olympiad name to
            visualize. Defaults to "All" to include all Olympiads.

        Returns:
            plotly.graph_objs.Figure: Sunburst chart showing medal distribution by
            gender, discipline, and event.
        """
        df_filtered = self._compute_sunburst_data(selected_olympiad_for_sunburst)
        return self._plot_sunburst_medals(df_filtered, selected_olympiad_for_sunburst)
