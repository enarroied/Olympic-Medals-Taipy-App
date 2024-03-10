import pandas as pd
import plotly.express as px
import taipy.gui.builder as tgb

###########################################################
###                    Load Datasets                    ###
###########################################################
df_olympic_cities = pd.read_csv("./src/data/olympic_cities.csv")
df_olympic_medals = pd.read_csv("./src/data/olympic_medals.csv")


with tgb.Page() as athlete_medals:

    tgb.text("Medals Awarded to athletes (or teams)", class_name="h2")
    tgb.text(
        "This dashboard shows detail data for the medals awarded to individuals or teams"
    )
