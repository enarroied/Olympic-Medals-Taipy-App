from algorithms.medal_details import create_medals_detail
from algorithms.plotting_all_time import create_bar_medals
from algorithms.plotting_medals_by_committee import (
    plot_medals_grid_both_seasons,
    plot_total_medals_by_country_both_seasons,
)


def on_selector_medals_by_committee(state):
    with state as s:
        df_grouped_medals_olympiads = s.df_grouped_medals_olympiads.copy()
        df_olympic_medals = s.df_olympic_medals.copy()
        df_total_medals_by_olympiad_and_committee = (
            s.df_total_medals_by_olympiad_and_committee.copy()
        )
        selected_committe = s.committee_detail

        s.summer_medal_by_committee, s.winter_medal_by_committee = (
            plot_total_medals_by_country_both_seasons(
                df_total_medals_by_olympiad_and_committee,
                committee_list=s.committees,
                medal_type=s.medal_type,
                percentage=s.display_percent,
            )
        )
        (
            s.total_medals_detail,
            s.gold_medals_detail,
            s.silver_medals_detail,
            s.bronze_medals_detail,
        ) = create_medals_detail(df_grouped_medals_olympiads, selected_committe)

        s.summer_medal_grid, s.winter_medal_grid = plot_medals_grid_both_seasons(
            df_olympic_medals, committee=selected_committe
        )


def on_selector_all_time_medals(state):
    with state as s:
        df_medals_by_olympiad = s.df_medals_by_olympiad.copy()
        s.bar_medals = create_bar_medals(df_medals_by_olympiad, s.season)


def init_total_medals(state):
    with state as s:
        df_olympic_medals = s.df_olympic_medals

        s.total_medals = int(len(df_olympic_medals))
        s.total_gold_medals = int(
            df_olympic_medals[df_olympic_medals["Medal_type"] == "Gold"][
                "Medal_type"
            ].count()
        )
        s.total_silver_medals = int(
            df_olympic_medals[df_olympic_medals["Medal_type"] == "Silver"][
                "Medal_type"
            ].count()
        )
        s.total_bronze_medals = int(
            df_olympic_medals[df_olympic_medals["Medal_type"] == "Bronze"][
                "Medal_type"
            ].count()
        )


def get_last_olympic(state):
    state.latest_olympiad = state.df_olympic_medals.loc[
        state.df_olympic_medals["Olympic_year"].idxmax(), "Olympiad"
    ]
