import taipy.gui.builder as tgb
from taipy.gui import Gui

from pages.all_time_medals import all_time_medals
from pages.medals_by_committee import committee_medals

###########################################################
###                       Run App                       ###
###########################################################
with tgb.Page() as root_page:
    with tgb.layout("1 1"):
        tgb.text("# Olympic medals 🥇🥈🥉", mode="md")
        tgb.image("../img/jo.jpeg", width="100px", label="Enjoy Paris 2024!")
    tgb.navbar()

pages = {
    "/": root_page,
    "all_time_medals": all_time_medals,
    "medals_awarded_to_committees": committee_medals,
}
gui_multi_pages = Gui(pages=pages)

if __name__ == "__main__":
    gui_multi_pages.run(
        use_reloader=True,
        title="Olympic medals 🥇",
        port=2452,
        dark_mode=False,
    )

# gui_multi_pages.run(run_server=False, title="Olympic medals 🥇")
# flask_app = gui_multi_pages.get_flask_app()
