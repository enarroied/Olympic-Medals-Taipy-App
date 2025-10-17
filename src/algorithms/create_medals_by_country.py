import pandas as pd
import plotly.express as px


class MedalsByCountry:
    def __init__(self, df_total_medals_by_olympiad_and_committee):
        self.df_total_medals_by_olympiad_and_committee = (
            df_total_medals_by_olympiad_and_committee.copy()
        )

    def _compute_medals_by_committee(
        self, committee_list, season, medal_type, percentage
    ):
        # TODO: Clean this mess!
        df_filtered = self.df_total_medals_by_olympiad_and_committee[
            (self.df_total_medals_by_olympiad_and_committee["Olympic_season"] == season)
            & (
                self.df_total_medals_by_olympiad_and_committee["Medal_type"]
                == medal_type
            )
        ]

        columns_to_plot = [
            "Olympic_year",
            "Olympiad",
            "Total_medals",
        ] + committee_list  # TODO: take this hardcopded stuff out
        df_to_plot = df_filtered[columns_to_plot]

        if percentage == "Percentage":  # TODO: remove this flag
            for committee in committee_list:
                df_to_plot.loc[:, committee] = (
                    df_to_plot[committee] * 100 / df_to_plot["Total_medals"]
                ).fillna(0)
        df_to_plot = df_to_plot.drop(columns=["Total_medals"])
        return df_to_plot

    def _plot_fig_total_medals_by_country(
        self, df_to_plot, committee_list, season, medal_type, value_label
    ):
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
            title=f"{medal_type} Medals for Selected Committees by Olympic Year | {season}",  # TODO: title could be a parameter
            hover_data={"Olympiad": True},
        )
        fig.update_traces(mode="markers+lines", marker=dict(size=4))
        return fig

    def _create_total_medals_by_country(
        self,
        committee_list,
        season,
        medal_type="All",
        percentage="Total medals",
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
        - fig: Plotly figure object showing total medals by year for selected committees.
        """

        df_to_plot = self._compute_medals_by_committee(
            committee_list, season, medal_type, percentage
        )
        value_label = (
            "Percentage of Medals" if percentage == "Percentage" else "Total Medals"
        )  # TODO: change this to a dict or something cleaner
        return self._plot_fig_total_medals_by_country(
            df_to_plot, committee_list, season, medal_type, value_label
        )

    def create_total_medals_by_country_summer(
        self,
        committee_list,
        medal_type,
        percentage,
    ):
        return self._create_total_medals_by_country(
            committee_list=committee_list,
            season="summer",
            medal_type=medal_type,
            percentage=percentage,
        )

    def create_total_medals_by_country_winter(
        self,
        committee_list,
        medal_type,
        percentage,
    ):

        return self._create_total_medals_by_country(
            committee_list=committee_list,
            season="winter",
            medal_type=medal_type,
            percentage=percentage,
        )
