import pandas as pd
import plotly.express as px
import taipy.gui.builder as tgb
from taipy.gui import Gui

###########################################################
###                    Load Datasets                    ###
###########################################################
olympic_cities_df = pd.read_csv("./data/olympic_cities.csv")
olympic_medals_df = pd.read_csv("./data/olympic_medals.csv")

###########################################################
###                      Functions                      ###
###########################################################


###########################################################
###                      Design Page                    ###
###########################################################
with tgb.Page() as page:
    tgb.text("Olympic medals 🥇🥈🥉", class_name="h1")

    with tgb.layout("1 1 1 1"):
        with tgb.part("card card-bg"):
            tgb.text(
                "Total Gold Medals 🥇 ",
                class_name="h2",
            )
            tgb.text(
                "{int(olympic_medals_df[olympic_medals_df['Medal_type']=='Gold']['Medal_type'].count())}",
                class_name="h3",
            )

        with tgb.part("card card-bg"):
            tgb.text(
                "Total Silver Medals 🥈",
                class_name="h2",
            )
            tgb.text(
                "{int(olympic_medals_df[olympic_medals_df['Medal_type']=='Silver']['Medal_type'].count())}",
                class_name="h3",
            )

        with tgb.part("card card-bg"):
            tgb.text(
                "Total Bronze Medals 🥉 ",
                class_name="h2",
            )
            tgb.text(
                "{int(olympic_medals_df[olympic_medals_df['Medal_type']=='Bronze']['Medal_type'].count())}",
                class_name="h3",
            )

        with tgb.part("card card-bg"):
            tgb.text(
                "Total Medals 🏟",
                class_name="h2",
            )
            tgb.text("{int(len(olympic_medals_df))}", class_name="h3")

###########################################################
###                       Run App                       ###
###########################################################

if __name__ == "__main__":
    gui = Gui(page)
    gui.run(use_reloader=True, title="Olympic medals 🥇", port=2452)
