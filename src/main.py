import pandas as pd
import taipy.gui.builder as tgb
from taipy.gui import Gui

from algorithms.plotting_all_time import (create_bar_by_committee,
                                          create_bar_medals,
                                          create_sunburnst_medals,
                                          plot_olympic_medals_by_country)
from algorithms.plotting_medals_by_committee import (
    plot_medals_grid, plot_total_medals_by_country_both_seasons)
from algorithms.read_parameters import yaml_to_list
from pages.all_time_medals import all_time_medals
from pages.medals_by_committee import committee_medals

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

if __name__ == "__main__":

    # Variables for both pages
    df_olympic_cities = pd.read_parquet("./data/olympic_cities.parquet")
    df_olympic_medals = pd.read_parquet("./data/olympic_medals.parquet")

    list_seasons = ["All", "summer", "winter"]
    list_medal_types = ["All", "Gold", "Silver", "Bronze"]

    # Variables for all_time_medals
    df_olympic_cities_simplified = pd.read_parquet(
        "./data/olympic_cities_simplified.parquet"
    )
    df_medals_by_olympiad = pd.read_parquet("./data/medals_by_olympiad.parquet")
    df_grouped_medals = pd.read_parquet("./data/grouped_medals.parquet")

    bar_medals = create_bar_medals(df_medals_by_olympiad, "All")
    bar_medals_by_committee = create_bar_by_committee(df_olympic_medals, "All")
    map_medals = plot_olympic_medals_by_country(
        df_olympic_cities, season="All", medal_type="All"
    )
    sunburnst_medals = create_sunburnst_medals(
        df_olympic_medals, selected_olympiad_for_sunburst="All"
    )

    list_olympiads = yaml_to_list("./parameters/list_olympiads.yml")

    list_seasons_map = ["All", "summer", "winter"]
    season = "All"
    selected_olympiad = "All"
    selected_season_map = "All"
    selected_medal_color = "All"
    selected_olympiad_for_sunburst = "All"

    # Variables for meddals_by_committe
    list_committees = yaml_to_list("./parameters/list_committees.yml")
    committees = ["France", "United States"]
    committee_detail = "France"
    medal_type = "All"
    display_percent = "Total medals"

    # To fix
    summer_medal_by_committee, winter_medal_by_committee = (
        plot_total_medals_by_country_both_seasons(
            df_olympic_medals,
            committee_list=committees,
            medal_type=medal_type,
        )
    )
    # For detail cards
    total_medals_detail = int(
        df_grouped_medals[df_grouped_medals["Committee"] == committee_detail][
            "Total"
        ].iloc[0]
    )
    gold_medals_detail = int(
        df_grouped_medals[df_grouped_medals["Committee"] == committee_detail][
            "Gold"
        ].iloc[0]
    )
    silver_medals_detail = int(
        df_grouped_medals[df_grouped_medals["Committee"] == committee_detail][
            "Silver"
        ].iloc[0]
    )
    bronze_medals_detail = int(
        df_grouped_medals[df_grouped_medals["Committee"] == committee_detail][
            "Bronze"
        ].iloc[0]
    )

    summer_medal_grid = plot_medals_grid(
        df_olympic_medals, committee=committee_detail, season="summer"
    )
    winter_medal_grid = plot_medals_grid(
        df_olympic_medals, committee=committee_detail, season="winter"
    )

    gui_multi_pages.run(
        use_reloader=True,
        title="Olympic medals 🥇",
        port=2452,
        dark_mode=False,
    )

# gui_multi_pages.run(run_server=False, title="Olympic medals 🥇")
# flask_app = gui_multi_pages.get_flask_app()
