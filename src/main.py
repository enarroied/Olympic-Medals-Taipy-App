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
    if season != "winter":
        stockholm_annotation_y = 800  # Stockholm 1956 there are 18 medals total, but 800 will weep box out of othe chart elements
        stockholm_annotation_x = (
            df_medals_season[df_medals_season["Olympiad"] == "Stockholm 1956"].index[0]
            / 3
        ) + 1  # Divide by 3 because 3 types of medals

        fig.add_annotation(
            x=stockholm_annotation_x,
            y=stockholm_annotation_y,
            text=str("Stockholm 1956 only had equestrian games"),
            showarrow=True,
            arrowhead=1,
            arrowcolor="#FF0066",
            arrowwidth=1,
            arrowsize=1,
            ax=0,
            ay=-100,
            font=dict(color="black", size=12),
            align="center",
            bordercolor="#c7c7c7",
            borderwidth=2,
            borderpad=4,
            bgcolor="#ff7f0e",
            opacity=0.8,
        )
    return fig


def create_bar_by_committee(df_medals, Olympiad="All"):

    df_medals_by_committee = df_medals.copy()

    if Olympiad != "All":
        df_medals_by_committee = df_medals_by_committee[
            df_medals_by_committee["Olympiad"] == Olympiad
        ]

    # Define medal colors
    medal_colors = {"Gold": "#FFD700", "Silver": "#C0C0C0", "Bronze": "#CD7F32"}

    # Aggregating data to get count of medals by Medal_type for each Committee
    df_aggregated = (
        df_medals_by_committee.groupby(["Committee", "Medal_type"])
        .size()
        .unstack(fill_value=0)
    )

    # Sort DataFrame by count of gold and silver medals
    df_aggregated = df_aggregated.sort_values(by=["Gold", "Silver"], ascending=False)

    # Plotly bar chart
    fig = px.bar(
        df_aggregated,
        x=df_aggregated.index,
        y=["Gold", "Silver", "Bronze"],
        barmode="group",
        orientation="v",
        color_discrete_map=medal_colors,
        labels={"value": "Count", "variable": "Medal Type"},
        title="Count of Gold, Silver, Bronze Medals by Committee",
    )
    fig.update_layout(xaxis={"title": "Committee"}, yaxis={"title": "Count"})
    return fig


###########################################################
###                  Displayed objects                  ###
###########################################################
bar_medals = create_bar_medals(df_medals_by_olympiad, "All")
bar_medals_by_committee = create_bar_by_committee(df_olympic_medals, "All")

###########################################################
###         Initial variables and selector lists        ###
###########################################################

list_seasons = ["All", "summer", "winter"]
list_olympiads = [
    "All",
    "Athina 1896",
    "Paris 1900",
    "St. Louis 1904",
    "Athina 1906",
    "London 1908",
    "Stockholm 1912",
    "Antwerpen 1920",
    "Paris 1924",
    "Amsterdam 1928",
    "Los Angeles 1932",
    "Berlin 1936",
    "London 1948",
    "Helsinki 1952",
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
    "Stockholm 1956",
    "Torino 2006",
    "Beijing 2008",
    "London 2012",
    "Vancouver 2010",
    "Sochi 2014",
    "Rio de Janeiro 2016",
    "PyeongChang 2018",
    "Tokyo 2020",
    "Beijing 2022",
]

season = "All"
selected_olympiad = "All"


###########################################################
###                  Selector Function                  ###
###########################################################
def on_selector(state):
    state.bar_medals = create_bar_medals(df_medals_by_olympiad, state.season)
    state.bar_medals_by_committee = create_bar_by_committee(
        df_olympic_medals, state.selected_olympiad
    )


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

    tgb.table("{df_olympic_cities_simplified}")
###########################################################
###                       Run App                       ###
###########################################################

if __name__ == "__main__":
    gui = Gui(page)
    gui.run(use_reloader=True, title="Olympic medals 🥇", port=2452)
