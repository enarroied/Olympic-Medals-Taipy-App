"""
Module for visualizing Olympic medal by committee and discipline.

This module defines the MedalsByOlympicAndDiscipline class, which creates a
grid with the number of medals a country has obtained for a certain discipline,
and by Olympic event.

Used by `all_time_medals.py`.
"""

import pandas as pd
import plotly.express as px


class MedalsByOlympicAndDiscipline:
    """Handles data aggregation and generates a bar chart by Olympic season."""

    def __init__(
        self,
        df_olympic_medals: pd.DataFrame,
    ):
        """Initialize MedalsBySeason with medal data and optional color mapping."""
        self.df_olympic_medals = df_olympic_medals.copy()

    # TODO: Season should only be ONE argument
    def _plot_grid_for_country(self, df_grouped, committee, season, ordered_olympiads):
        fig = px.imshow(
            df_grouped,
            labels=dict(x="Discipline", y="Olympiad", color="Total Medals"),
            x=df_grouped.columns,
            y=ordered_olympiads,
            color_continuous_scale="plasma",
            title=f"Medals by Olympiad and discipline for {committee} | {season}",
        )
        # reduce font size:
        fig.update_layout(
            xaxis=dict(tickfont=dict(size=9)),
            yaxis=dict(tickfont=dict(size=9)),
            coloraxis_colorbar=dict(
                tickfont=dict(size=9),
            ),
        )
        return fig

    def create_medals_grid(self, committee, season):
        """
        Plot medals won by a committee across different disciplines and Olympiads.

        Parameters:
        - df_medals (DataFrame): DataFrame containing medal data.
        - committee (str): Name of the committee.
        - season (str): Olympic season: "summer" or "winter".

        Returns:
        - fig: Plotly figure object showing medals by Olympiad and discipline for
        the committee.
        """
        df_medals = self.df_olympic_medals.copy()
        df_filtered = df_medals[(df_medals["Olympic_season"] == season)]

        # Get all possible disciplines --> Like this, all disciplines appear for all
        # countries
        # Important to do this after filtering by season and before filtering by
        # committee!
        all_disciplines = df_filtered["Discipline"].unique()

        # And then only filter the DataFrame by committee
        df_filtered = df_filtered[(df_filtered["Committee"] == committee)]
        df_grouped = df_filtered.pivot_table(
            index=["Olympiad", "Olympic_year"],
            columns="Discipline",
            aggfunc="size",
            fill_value=0,
            observed=True,
        )

        df_grouped = df_grouped.sort_index(level=1)

        # TODO: take this out of this function!
        ordered_olympiads = list(df_grouped.index.get_level_values("Olympiad").unique())

        # Add all the disciplines of the selcted season, whether the Committee won a
        #  medals or not
        return (
            df_grouped.reindex(columns=all_disciplines, fill_value=0),
            ordered_olympiads,
        )

    # TODO: Add a grouped abstraction to reduce repetition
    def plot_medals_grid_summer(self, committee):
        df_grouped, ordered_olympiads = self.create_medals_grid(
            committee=committee, season="summer"
        )
        return self._plot_grid_for_country(
            df_grouped, committee, "summer", ordered_olympiads
        )

    def plot_medals_grid_winter(self, committee):
        df_grouped, ordered_olympiads = self.create_medals_grid(
            committee=committee, season="winter"
        )
        return self._plot_grid_for_country(
            df_grouped, committee, "winter", ordered_olympiads
        )
