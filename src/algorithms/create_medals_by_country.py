"""
Module for visualizing Olympic medal counts by country and Olympic season.

This module defines the MedalsByCountry class, which filters, computes,
and plots total or percentage-based medal counts for different Olympic
committees using pandas and Plotly.

Used by `medals_by_committee.py`.
"""

from typing import List

import pandas as pd
import plotly.express as px
from plotly.graph_objs import Figure


class MedalsByCountry:
    """Handles data aggregation and generates line plots with medals by
    committee, for summer and for winter Olympics."""

    def __init__(self, df_total_medals_by_olympiad_and_committee: pd.DataFrame):
        self.total_medals = df_total_medals_by_olympiad_and_committee.copy()
        self.columns_for_plot = [
            "Olympic_year",
            "Olympiad",
            "Total_medals",
        ]

    def _filter_dataset(
        self, committee_list: List[str], season: str, medal_type: str
    ) -> pd.DataFrame:
        """Filter the medals dataset by Olympic season and medal type."""
        df_filtered = self.total_medals[
            (self.total_medals["Olympic_season"] == season)
            & (self.total_medals["Medal_type"] == medal_type)
        ]

        columns_to_plot = self.columns_for_plot + committee_list
        return df_filtered[columns_to_plot].copy()

    def _compute_percentage(
        self, df_to_plot: pd.DataFrame, committee_list: List[str]
    ) -> pd.DataFrame:
        """Compute percentage of medals per committee based on total medals."""
        for committee in committee_list:
            df_to_plot.loc[:, committee] = (
                df_to_plot[committee] * 100 / df_to_plot["Total_medals"]
            ).fillna(0)
        return df_to_plot

    def _compute_medals_by_committee(
        self,
        committee_list: List[str],
        season: str,
        medal_type: str,
        percentage: str,
    ) -> pd.DataFrame:
        """Compute medals by committee, optionally converting to percentages."""
        df_to_plot = self._filter_dataset(committee_list, season, medal_type)
        if percentage == "Percentage":
            df_to_plot = self._compute_percentage(df_to_plot, committee_list)
        return df_to_plot.drop(columns=["Total_medals"])

    def _plot_fig_total_medals_by_country(
        self,
        df_to_plot: pd.DataFrame,
        committee_list: List[str],
        value_label: str,
        title: str,
    ) -> Figure:
        """Create a Plotly line chart showing total medals by committee over time."""
        fig = px.line(
            df_to_plot,
            x="Olympic_year",
            y=committee_list,
            labels={
                "value": value_label,
                "variable": "Committee",
                "Olympic_year": "Year",
                "Olympiad": "Olympiad",
            },
            title=title,
            hover_data={"Olympiad": True},
        )
        fig.update_traces(mode="markers+lines", marker=dict(size=4))
        return fig

    def _create_medals_by_country(
        self,
        committee_list: List[str],
        medal_type: str,
        percentage: str,
        season: str,
    ):
        """
        Plot total medals won by selected committees over Olympic years (by olympic
        season winter/summer).

        Parameters:
        - committee_list (list): List of committees to plot.
        - season (str): Olympic season: "summer" or "winter".
        - medal_type (str): Type of medal. Default is "All".
        - percentage (str): Type of representation. Default is "Total medals".
        Other option is "Percentage"

        Returns:
        - fig: Plotly figure object with total medals by year for committees.
        """
        chart_title = (
            f"{medal_type} Medals for Selected Committees by Olympic Year | {season}"
        )
        value_label = f"{percentage} - Medals"

        medals_country = self._compute_medals_by_committee(
            committee_list, season, medal_type, percentage
        )
        return self._plot_fig_total_medals_by_country(
            medals_country, committee_list, value_label, chart_title
        )

    def create_medals_by_country_summer(
        self,
        committee_list: List[str],
        medal_type: str,
        percentage: str,
    ):
        """Public method to plot medals by country for the Summer Olympics."""
        return self._create_medals_by_country(
            committee_list=committee_list,
            medal_type=medal_type,
            percentage=percentage,
            season="summer",
        )

    def create_medals_by_country_winter(
        self,
        committee_list: List[str],
        medal_type: str,
        percentage: str,
    ):
        """Public method to plot medals by country for the Winter Olympics."""
        return self._create_medals_by_country(
            committee_list=committee_list,
            medal_type=medal_type,
            percentage=percentage,
            season="winter",
        )
