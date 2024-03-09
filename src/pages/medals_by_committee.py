import pandas as pd
import plotly.express as px
import taipy.gui.builder as tgb

###########################################################
###                      Design Page                    ###
###########################################################


with tgb.Page() as committee_medals:

    tgb.text("Medals Awarded to committees", class_name="h2")
    tgb.text(
        "This dashboard shows aggregated data for the medals awarded to committees"
    )
