import pandas as pd
import plotly.express as px
import taipy.gui.builder as tgb

###########################################################
###                    Load Datasets                    ###
###########################################################
df_olympic_cities = pd.read_csv("./src/data/olympic_cities.csv")
df_olympic_medals = pd.read_csv("./src/data/olympic_medals.csv")

###########################################################
###             Ceate transformed DataFrames            ###
###########################################################
df_grouped_medals = (
    df_olympic_medals.groupby(["Committee", "Medal_type"])
    .size()
    .unstack(fill_value=0)
    .reset_index()
)
df_grouped_medals["Total"] = (
    df_grouped_medals["Gold"]
    + df_grouped_medals["Silver"]
    + df_grouped_medals["Bronze"]
)


###########################################################
###                      Functions                      ###
###########################################################


def plot_total_medals_by_country(df_medals, committee_list, season, medal_type="All"):
    df_filtered = df_medals[df_medals["Committee"].isin(committee_list)]
    df_filtered = df_filtered[df_filtered["Olympic_season"] == season]
    if medal_type != "All":
        df_filtered = df_filtered[df_filtered["Medal_type"] == medal_type]

    # Aggregating total medals for each Olympic year
    df_totals = (
        df_filtered.groupby(["Olympic_year", "Olympiad", "Committee"])
        .size()
        .unstack(fill_value=0)
        .reset_index()
    )

    fig = px.line(
        df_totals,
        x="Olympic_year",
        y=committee_list,
        labels={
            "value": "Total Medals",
            "variable": "Committee",
            "Olympic_year": "Year",
            "Olympiad": "Olympiad",
        },
        title=f"{medal_type} Medals for Selected committees by Olympic Year | {season}",
        hover_data={"Olympiad": True},
    )

    fig.update_traces(mode="markers+lines", marker=dict(size=4))

    return fig


###########################################################
###         Initial variables and selector lists        ###
###########################################################

list_seasons = ["All", "summer", "winter"]
list_medal_types = ["All", "Gold", "Silver", "Bronze"]
list_committees = [
    "Afghanistan",
    "Algeria",
    "Argentina",
    "Armenia",
    "Australasia",
    "Australia",
    "Austria",
    "Azerbaijan",
    "Bahamas",
    "Bahrain",
    "Barbados",
    "Belarus",
    "Belgium",
    "Bermuda",
    "Bohemia",
    "Botswana",
    "Brazil",
    "Bulgaria",
    "Burkina Faso",
    "Burundi",
    "Cameroon",
    "Canada",
    "Chile",
    "China",
    "Chinese Taipei[3]",
    "Colombia",
    "Costa Rica",
    "Croatia",
    "Cuba",
    "Cyprus",
    "Czechia",
    "Czechoslovakia",
    "Denmark",
    "Djibouti",
    "Dominican Republic",
    "East Germany",
    "Ecuador",
    "Egypt",
    "Eritrea",
    "Estonia",
    "Ethiopia",
    "Fiji",
    "Finland",
    "France",
    "Gabon",
    "Georgia",
    "Germany",
    "Ghana",
    "Great Britain",
    "Greece",
    "Grenada",
    "Guatemala",
    "Guyana",
    "Haiti",
    "Hong Kong, China",
    "Hungary",
    "Iceland",
    "Independent Olympic Athletes",
    "India",
    "Indonesia",
    "Iran",
    "Iraq",
    "Ireland",
    "Israel",
    "Italy",
    "Ivory Coast",
    "Jamaica",
    "Japan",
    "Jordan",
    "Kazakhstan",
    "Kenya",
    "Kosovo",
    "Kuwait",
    "Kyrgyzstan",
    "Latvia",
    "Lebanon",
    "Liechtenstein",
    "Lithuania",
    "Luxembourg",
    "Malaysia",
    "Mauritius",
    "Mexico",
    "Mixed-NOCs",
    "Moldova",
    "Monaco",
    "Mongolia",
    "Montenegro",
    "Morocco",
    "Mozambique",
    "Namibia",
    "Netherlands",
    "Netherlands Antilles",
    "New Zealand",
    "Niger",
    "Nigeria",
    "North Korea",
    "North Macedonia",
    "Norway",
    "Pakistan",
    "Panama",
    "Paraguay",
    "Peru",
    "Philippines",
    "Poland",
    "Portugal",
    "Puerto Rico",
    "Qatar",
    "ROC from the abbreviation for Russian Olympic Committee",
    "Romania",
    "Russia",
    "Samoa",
    "San Marino",
    "Saudi Arabia",
    "Senegal",
    "Serbia",
    "Serbia and Montenegro",
    "Singapore",
    "Slovakia",
    "Slovenia",
    "South Africa",
    "South Korea",
    "Soviet Union",
    "Spain",
    "Sri Lanka",
    "Sudan",
    "Suriname",
    "Sweden",
    "Switzerland",
    "Syria",
    "Tajikistan",
    "Tanzania",
    "Thailand",
    "Togo",
    "Tonga",
    "Trinidad and Tobago",
    "Tunisia",
    "Turkey",
    "Turkmenistan",
    "Uganda",
    "Ukraine",
    "Unified Team",
    "Unified Team from French Équipe unifiée",
    "United Arab Emirates",
    "United States",
    "Uruguay",
    "Uzbekistan",
    "Venezuela",
    "Vietnam",
    "Virgin Islands",
    "West Germany",
    "West Indies Federation",
    "Yugoslavia",
    "Zambia",
    "Zimbabwe",
]

committees = ["France", "United States"]
committee_detail = "France"
medal_type = "All"

###########################################################
###                  Displayed objects                  ###
###########################################################
summer_medal_by_committee = plot_total_medals_by_country(
    df_olympic_medals, committee_list=committees, season="summer", medal_type=medal_type
)
winter_medal_by_committee = plot_total_medals_by_country(
    df_olympic_medals, committee_list=committees, season="winter", medal_type=medal_type
)

# For detail cards
total_medals_detail = int(
    df_grouped_medals[df_grouped_medals["Committee"] == committee_detail]["Total"].iloc[
        0
    ]
)
gold_medals_detail = int(
    df_grouped_medals[df_grouped_medals["Committee"] == committee_detail]["Gold"].iloc[
        0
    ]
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


###########################################################
###                  Selector Function                  ###
###########################################################
def on_selector(state):
    # state.bar_medals = create_bar_medals(df_medals_by_olympiad, state.season)
    state.summer_medal_by_committee = plot_total_medals_by_country(
        df_olympic_medals,
        committee_list=state.committees,
        season="summer",
        medal_type=state.medal_type,
    )
    state.winter_medal_by_committee = plot_total_medals_by_country(
        df_olympic_medals,
        committee_list=state.committees,
        season="winter",
        medal_type=state.medal_type,
    )
    state.total_medals_detail = int(
        df_grouped_medals[df_grouped_medals["Committee"] == state.committee_detail][
            "Total"
        ].iloc[0]
    )
    state.gold_medals_detail = int(
        df_grouped_medals[df_grouped_medals["Committee"] == state.committee_detail][
            "Gold"
        ].iloc[0]
    )
    state.silver_medals_detail = int(
        df_grouped_medals[df_grouped_medals["Committee"] == state.committee_detail][
            "Silver"
        ].iloc[0]
    )
    state.bronze_medals_detail = int(
        df_grouped_medals[df_grouped_medals["Committee"] == state.committee_detail][
            "Bronze"
        ].iloc[0]
    )


###########################################################
###                      Design Page                    ###
###########################################################


with tgb.Page() as committee_medals:

    tgb.text("Medals Awarded to committees", class_name="h2")
    tgb.text(
        "This dashboard shows aggregated data for the medals awarded to committees"
    )
    with tgb.layout("1 1"):
        with tgb.part():
            tgb.selector(
                value="{committees}",
                lov=list_committees,
                dropdown=True,
                multiple=True,
                label="Select committees",
                class_name="fullwidth",
                on_change=on_selector,
            )
        with tgb.part():
            tgb.selector(
                value="{medal_type}",
                lov=list_medal_types,
                dropdown=True,
                label="Select medal type",
                class_name="fullwidth",
                on_change=on_selector,
            )
        with tgb.part():
            tgb.chart(figure="{summer_medal_by_committee}")
        with tgb.part():
            tgb.chart(figure="{winter_medal_by_committee}")

    tgb.text("Detailed information by committee", class_name="h2")
    with tgb.layout("1 1 1 1 1"):
        tgb.selector(
            value="{committee_detail}",
            lov=list_committees,
            dropdown=True,
            label="Select committee for detail",
            class_name="fullwidth",
            on_change=on_selector,
        )
        with tgb.part("card"):
            tgb.text(
                "Gold Medals 🥇",
                class_name="h4",
            )
            tgb.text(
                "{gold_medals_detail}",
                class_name="h4",
            )
        with tgb.part("card"):
            tgb.text(
                "Silver Medals 🥈",
                class_name="h4",
            )
            tgb.text(
                "{silver_medals_detail}",
                class_name="h4",
            )
        with tgb.part("card"):
            tgb.text(
                "Bronze Medals 🥉",
                class_name="h4",
            )
            tgb.text(
                "{bronze_medals_detail}",
                class_name="h4",
            )
        with tgb.part("card"):
            tgb.text(
                "Total Medals 🏟",
                class_name="h4",
            )
            tgb.text(
                "{total_medals_detail}",
                class_name="h4",
            )
