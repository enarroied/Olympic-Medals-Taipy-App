import pandas as pd
from algorithms.callbacks import (
    get_last_olympic,
    init_total_medals,
    on_selector_all_time_medals,
    on_selector_medals_by_committee,
)
from algorithms.read_parameters import yaml_to_list
from pages.all_time_medals import all_time_medals
from pages.medals_by_committee import committee_medals

import taipy.gui.builder as tgb
from taipy.gui import Gui

###########################################################
###                       Run App                       ###
###########################################################
with tgb.Page() as root_page:
    with tgb.layout("1 1"):
        tgb.text("# Olympic medals 🥇🥈🥉", mode="md")
    tgb.navbar()

pages = {
    "/": root_page,
    "all_time_medals": all_time_medals,
    "medals_awarded_to_committees": committee_medals,
}
gui_multi_pages = Gui(pages=pages)


def on_init(state):
    init_total_medals(state)
    on_selector_all_time_medals(state)
    on_selector_medals_by_committee(state)
    get_last_olympic(state)


if __name__ == "__main__":
    # Variables for both page
    df_olympic_cities = pd.read_parquet("./data/olympic_cities.parquet")
    df_olympic_medals = pd.read_parquet("./data/olympic_medals.parquet")
    df_grouped_medals_olympiads = pd.read_parquet(
        "./data/grouped_medals_olympiads.parquet"
    )

    list_seasons = ["All", "summer", "winter"]
    list_medal_types = ["All", "Gold", "Silver", "Bronze"]

    # Variables for all_time_medals
    df_olympic_cities_simplified = pd.read_parquet(
        "./data/olympic_cities_simplified.parquet"
    )
    df_medals_by_olympiad = pd.read_parquet("./data/medals_by_olympiad.parquet")

    df_sunburst = df_olympic_medals[
        ["Olympiad", "Gender", "Discipline", "Event"]
    ].copy()
    df_sunburst = df_sunburst.astype(str)

    latest_olympiad = ""

    total_medals = 0
    total_gold_medals = 0
    total_silver_medals = 0
    total_bronze_medals = 0

    bar_medals = None
    bar_medals_by_committee = None
    map_medals = None
    sunburnst_medals = None

    list_olympiads = yaml_to_list("./parameters/list_olympiads.yml")

    list_seasons_map = ["All", "summer", "winter"]
    season = "All"
    selected_olympiad = "All"
    selected_season_map = "All"
    selected_medal_color = "All"
    selected_olympiad_for_sunburst = "All"

    # Variables for meddals_by_committe
    df_total_medals_by_olympiad_and_committee = pd.read_parquet(
        "./data/total_medals_by_olympiad_and_committee.parquet"
    )

    list_committees = yaml_to_list("./parameters/list_committees.yml")
    committees = ["France", "United States"]
    committee_detail = "France"
    medal_type = "All"
    display_percent = "Total medals"

    summer_medal_by_committee, winter_medal_by_committee = None, None
    # For detail cards
    (
        total_medals_detail,
        gold_medals_detail,
        silver_medals_detail,
        bronze_medals_detail,
    ) = (
        None,
        None,
        None,
        None,
    )

    summer_medal_grid, winter_medal_grid = None, None

    gui_multi_pages.run(
        use_reloader=True,
        title="Olympic medals 🥇",
        dark_mode=False,
    )

# gui_multi_pages.run(run_server=False, title="Olympic medals 🥇")
# flask_app = gui_multi_pages.get_flask_app()
