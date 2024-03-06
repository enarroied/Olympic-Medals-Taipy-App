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
###             Ceate transformed DataFrames            ###
###########################################################

# Small DataFrame to display as summary table
df_olympic_cities_simplified = df_olympic_cities[
    [
        "Olympiad",
        "Olympic_year",
        "Olympic_season",
        "total_medals",
        "total_medals_gold",
        "total_medals_silver",
        "total_medals_bronze",
        "number_committees",
        "number_disciplines",
        "number_events",
        "Country",
        "Continent",
    ]
]

# Define a custom sorting order for 'Medal_type'
medal_order = {"Bronze": 0, "Silver": 1, "Gold": 2}

df_medals_by_olympiad = (
    df_olympic_medals.groupby(
        ["Olympiad", "Olympic_year", "Medal_type", "Olympic_season"]
    )
    .size()
    .reset_index(name="Medal_count")
)

# Sort the DataFrame first by 'Olympic_year' and then by 'Medal_type' using the custom sorting order
df_medals_by_olympiad["Medal_type_code"] = df_medals_by_olympiad["Medal_type"].map(
    medal_order
)
df_medals_by_olympiad = df_medals_by_olympiad.sort_values(
    by=["Olympic_year", "Medal_type_code"]
)

# Reset index without creating a new column
df_medals_by_olympiad.reset_index(drop=True, inplace=True)


###########################################################
###                      Functions                      ###
###########################################################
def create_bar_medals(df_medals_by_olympiad, season):
    # Define colors for each medal type
    medal_colors = {"Gold": "#FFD700", "Silver": "#C0C0C0", "Bronze": "#CD7F32"}

    if season != "All":
        df_medals_season = df_medals_by_olympiad[
            df_medals_by_olympiad["Olympic_season"] == season
        ].reset_index(drop=True)
    else:
        df_medals_season = df_medals_by_olympiad
    # Create a stacked bar chart
    fig = px.bar(
        df_medals_season,
        x="Olympiad",
        y="Medal_count",
        color="Medal_type",
        color_discrete_map=medal_colors,  # Assign colors to medal types
        title="Medal Count by Olympiad and Medal Type",
        labels={"Medal_count": "Medal Count", "Olympiad": "Olympiad"},
        category_orders={"Olympiad": df_medals_season["Olympiad"].unique()},
    )
    return fig


###########################################################
###                  Displayed objects                  ###
###########################################################
bar_medals = create_bar_medals(df_medals_by_olympiad, "All")

###########################################################
###         Initial variables and selector lists        ###
###########################################################

list_seasons = ["All", "summer", "winter"]

season = "All"


###########################################################
###                  Selector Function                  ###
###########################################################
def on_selector(state):
    state.bar_medals = create_bar_medals(df_medals_by_olympiad, state.season)


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

    # Bar chart of all medals:
    with tgb.layout("1 1"):
        with tgb.part():
            tgb.selector(
                value="{season}",
                lov=list_seasons,
                dropdown=True,
                label="Select season",
                class_name="fullwidth",
                on_change=on_selector,
            )
            tgb.chart(figure="{bar_medals}")

    tgb.table("{df_olympic_cities_simplified}")
###########################################################
###                       Run App                       ###
###########################################################

if __name__ == "__main__":
    gui = Gui(page)
    gui.run(use_reloader=True, title="Olympic medals 🥇", port=2452)
