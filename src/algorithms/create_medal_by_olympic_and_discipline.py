"""
Module for visualizing Olympic medal by committee and discipline.

This module defines the MedalsByOlympicAndDiscipline class, which creates a
grid with the number of medals a country has obtained for a certain discipline,
and by Olympic event.

Used by `all_time_medals.py`.
"""

from functools import partial

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
        self.df_summer = self._filter_olympic_season(df_olympic_medals, "summer")
        self.df_winter = self._filter_olympic_season(df_olympic_medals, "winter")
        self.summer_disciplines = self.df_summer["Discipline"].unique()
        self.winter_disciplines = self.df_winter["Discipline"].unique()
        # Bind convenience callables that only require committee
        # Note: self._create_medals_grid_core is a bound method; partial binds the next args.
        self._create_summer_grid = partial(
            self._create_medals_grid, self.df_summer, self.summer_disciplines
        )
        self._create_winter_grid = partial(
            self._create_medals_grid, self.df_winter, self.winter_disciplines
        )

    def _filter_olympic_season(self, df, season):
        return df[(df["Olympic_season"] == season)].copy()

    def _plot_grid_for_country(self, df_grouped, title, ordered_olympiads):
        fig = px.imshow(
            df_grouped,
            labels=dict(x="Discipline", y="Olympiad", color="Total Medals"),
            x=df_grouped.columns,
            y=ordered_olympiads,
            color_continuous_scale="plasma",
            title=title,
        )
        # reduce font size:
        small_tick_font = dict(tickfont=dict(size=9))
        fig.update_layout(
            xaxis=small_tick_font,
            yaxis=small_tick_font,
            coloraxis_colorbar=small_tick_font,
        )
        return fig

    def _pivot_olympic_by_discipline(self, df):
        return df.pivot_table(
            index=["Olympiad", "Olympic_year"],
            columns="Discipline",
            aggfunc="size",
            fill_value=0,
            observed=True,
        ).sort_index(level=1)

    def _create_medals_grid(self, df_medals, all_disciplines, committee):
        """
        Plot medals won by a committee across different disciplines and Olympiads.

        Parameters:
        - df_medals (DataFrame): DataFrame containing medal data.
        - all_disciplines (list): All the disciplines for the Olympic season.
        - committee (str): Name of the committee.

        Returns:
        - fig: Plotly figure object showing medals by Olympiad and discipline for
        the committee.
        """
        df_medals = df_medals[(df_medals["Committee"] == committee)]
        return self._pivot_olympic_by_discipline(df_medals).reindex(
            columns=all_disciplines, fill_value=0
        )

    # TODO: Add a grouped abstraction to reduce repetition
    def plot_medals_grid_summer(self, committee):
        df_grouped = self._create_summer_grid(committee=committee)
        ordered_olympiads = list(df_grouped.index.get_level_values("Olympiad").unique())
        title = f"Medals by Olympiad and discipline for {committee} | summer"
        return self._plot_grid_for_country(df_grouped, title, ordered_olympiads)

    def plot_medals_grid_winter(self, committee):
        df_grouped = self._create_winter_grid(committee=committee)
        ordered_olympiads = list(df_grouped.index.get_level_values("Olympiad").unique())
        title = f"Medals by Olympiad and discipline for {committee} | winter"
        return self._plot_grid_for_country(df_grouped, title, ordered_olympiads)
