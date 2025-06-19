import pandas as pd
from algorithms.plotting_all_time import (
    create_bar_medals,
    create_bar_by_committee,
    create_sunburnst_medals,
    plot_olympic_medals_by_country,
)
import taipy.gui.builder as tgb

###########################################################
###                    Load Datasets                    ###
###########################################################
df_olympic_cities = pd.read_csv("./data/olympic_cities.csv")
df_olympic_medals = pd.read_csv("./data/olympic_medals.csv")

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
###                  Displayed objects                  ###
###########################################################
bar_medals = create_bar_medals(df_medals_by_olympiad, "All")
bar_medals_by_committee = create_bar_by_committee(df_olympic_medals, "All")
map_medals = plot_olympic_medals_by_country(
    df_olympic_cities, season="All", medal_type="All"
)
sunburnst_medals = create_sunburnst_medals(
    df_olympic_medals, selected_olympiad_for_sunburst="All"
)

###########################################################
###         Initial variables and selector lists        ###
###########################################################

list_seasons = ["All", "summer", "winter"]
list_olympiads = [
    "All",
    "Athina 1896",
    "Paris 1900",
    "St. Louis 1904",
    "London 1908",
    "Stockholm 1912",
    "Antwerpen 1920",
    "Paris 1924",
    "Amsterdam 1928",
    "Los Angeles 1932",
    "Berlin 1936",
    "London 1948",
    "Helsinki 1952",
    "Stockholm 1956",
    "Melbourne 1956",
    "Roma 1960",
    "Tokyo 1964",
    "Ciudad de México 1968",
    "München 1972",
    "Montréal 1976",
    "Moskva 1980",
    "Los Angeles 1984",
    "Seoul 1988",
    "Barcelona 1992",
    "Atlanta 1996",
    "Sydney 2000",
    "Athina 2004",
    "Beijing 2008",
    "London 2012",
    "Rio de Janeiro 2016",
    "Tokyo 2020",
    "Chamonix 1924",
    "Sankt Moritz 1928",
    "Lake Placid 1932",
    "Garmisch-Partenkirchen 1936",
    "Sankt Moritz 1948",
    "Oslo 1952",
    "Cortina d'Ampezzo 1956",
    "Squaw Valley 1960",
    "Innsbruck 1964",
    "Grenoble 1968",
    "Sapporo 1972",
    "Innsbruck 1976",
    "Lake Placid 1980",
    "Sarajevo 1984",
    "Calgary 1988",
    "Albertville 1992",
    "Lillehammer 1994",
    "Nagano 1998",
    "Salt Lake City 2002",
    "Torino 2006",
    "Vancouver 2010",
    "Sochi 2014",
    "PyeongChang 2018",
    "Beijing 2022",
    "Paris 2024"
]
list_seasons_map = ["All", "summer", "winter"]
list_medal_colors = ["All", "Gold", "Silver", "Bronze"]
season = "All"
selected_olympiad = "All"
selected_season_map = "All"
selected_medal_color = "All"
selected_olympiad_for_sunburst = "All"


###########################################################
###                  Selector Function                  ###
###########################################################
def on_selector(state):
    with state as s:
        s.bar_medals = create_bar_medals(df_medals_by_olympiad, s.season)
        season.bar_medals_by_committee = create_bar_by_committee(
            df_olympic_medals, s.selected_olympiad
        )
        s.map_medals = plot_olympic_medals_by_country(
            df_olympic_cities,
            season=s.selected_season_map,
            medal_type=s.selected_medal_color,
        )
        s.sunburnst_medals = create_sunburnst_medals(
            df_olympic_medals, s.selected_olympiad_for_sunburst
        )


###########################################################
###                      Design Page                    ###
###########################################################


with tgb.Page() as all_time_medals:

    tgb.text("## Medals awarded at all Olympic games", mode="md")
    tgb.text(
        "This dashboard displays aggregated data for the medals awarded across the Olympics, from Athens 1896 to Beijing 2022."
    )

    with tgb.layout("1 1 1 1"):
        with tgb.part("card card-bg"):
            tgb.text(
                "#### Total Gold Medals 🥇 ",
                mode="md",
            )
            tgb.text(
                "#### {int(df_olympic_medals[df_olympic_medals['Medal_type']=='Gold']['Medal_type'].count())}",
                mode="md",
            )

        with tgb.part("card card-bg"):
            tgb.text(
                "#### Total Silver Medals 🥈",
                mode="md",
            )
            tgb.text(
                "#### {int(df_olympic_medals[df_olympic_medals['Medal_type']=='Silver']['Medal_type'].count())}",
                mode="md",
            )

        with tgb.part("card card-bg"):
            tgb.text(
                "#### Total Bronze Medals 🥉",
                mode="md",
            )
            tgb.text(
                "#### {int(df_olympic_medals[df_olympic_medals['Medal_type']=='Bronze']['Medal_type'].count())}",
                mode="md",
            )

        with tgb.part("card card-bg"):
            tgb.text(
                "#### Total Medals 🏟",
                mode="md",
            )
            tgb.text(
                "#### {int(len(df_olympic_medals))}",
                mode="md",
            )

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

        with tgb.part():
            tgb.selector(
                value="{selected_olympiad}",
                lov=list_olympiads,
                dropdown=True,
                label="Select Olympiad",
                class_name="fullwidth",
                on_change=on_selector,
            )
            tgb.chart(figure="{bar_medals_by_committee}")
        with tgb.part():
            with tgb.layout("1 1"):
                with tgb.part():
                    tgb.selector(
                        value="{selected_season_map}",
                        lov=list_seasons_map,
                        dropdown=True,
                        label="Select season for map",
                        class_name="fullwidth",
                        on_change=on_selector,
                    )
                with tgb.part():
                    tgb.selector(
                        value="{selected_medal_color}",
                        lov=list_medal_colors,
                        dropdown=True,
                        label="Select medal color",
                        class_name="fullwidth",
                        on_change=on_selector,
                    )
            tgb.chart(figure="{map_medals}")
        with tgb.part():
            tgb.selector(
                value="{selected_olympiad_for_sunburst}",
                lov=list_olympiads,
                dropdown=True,
                label="Select Olympiad",
                class_name="fullwidth",
                on_change=on_selector,
            )
            tgb.chart(figure="{sunburnst_medals}")

    tgb.table(
        "{df_olympic_cities_simplified}",
        filter=True,
    )
