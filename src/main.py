from pages.all_time_medals import all_time_medals
from pages.medals_by_committee import committee_medals
from algorithms.read_parameters import yaml_to_list

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

if __name__ == "__main__":

    # Variables for both pages
    list_seasons = ["All", "summer", "winter"]
    list_medal_types = ["All", "Gold", "Silver", "Bronze"]

    # Variables for all_tme_medals
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

    gui_multi_pages.run(
        use_reloader=True,
        title="Olympic medals 🥇",
        port=2452,
        dark_mode=False,
    )

# gui_multi_pages.run(run_server=False, title="Olympic medals 🥇")
# flask_app = gui_multi_pages.get_flask_app()
