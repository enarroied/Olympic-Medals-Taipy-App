import pandas as pd
import plotly.express as px
import taipy.gui.builder as tgb
from taipy.gui import Gui

###########################################################
###                    Load Datasets                    ###
###########################################################
df_olympic_cities = pd.read_csv("./src/data/olympic_cities.csv")
df_olympic_medals = pd.read_csv("./src/data/olympic_medals.csv")

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
                "{int(df_olympic_medals[df_olympic_medals['Medal_type']=='Gold']['Medal_type'].count())}",
                class_name="h3",
            )

        with tgb.part("card card-bg"):
            tgb.text(
                "Total Silver Medals 🥈",
                class_name="h2",
            )
            tgb.text(
                "{int(df_olympic_medals[df_olympic_medals['Medal_type']=='Silver']['Medal_type'].count())}",
                class_name="h3",
            )

        with tgb.part("card card-bg"):
            tgb.text(
                "Total Bronze Medals 🥉 ",
                class_name="h2",
            )
            tgb.text(
                "{int(df_olympic_medals[df_olympic_medals['Medal_type']=='Bronze']['Medal_type'].count())}",
                class_name="h3",
            )

        with tgb.part("card card-bg"):
            tgb.text(
                "Total Medals 🏟",
                class_name="h2",
            )
            tgb.text("{int(len(df_olympic_medals))}", class_name="h3")

###########################################################
###                       Run App                       ###
###########################################################

if __name__ == "__main__":
    gui = Gui(page)
    gui.run(use_reloader=True, title="Olympic medals 🥇", port=2452)
