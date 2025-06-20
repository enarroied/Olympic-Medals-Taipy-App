import pandas as pd
from algorithms.plotting_medals_by_committee import (
    plot_medals_grid,
    plot_total_medals_by_country,
)

import taipy.gui.builder as tgb

###########################################################
###                    Load Datasets                    ###
###########################################################
df_olympic_medals = pd.read_csv("./data/olympic_medals.csv")

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
    "Chinese Taipei",
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
display_percent = "Total medals"

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

summer_medal_grid = plot_medals_grid(
    df_olympic_medals, committee=committee_detail, season="summer"
)
winter_medal_grid = plot_medals_grid(
    df_olympic_medals, committee=committee_detail, season="winter"
)


###########################################################
###                  Selector Function                  ###
###########################################################
def on_selector(state):
    with state as s:
        s.summer_medal_by_committee = plot_total_medals_by_country(
            df_olympic_medals,
            committee_list=s.committees,
            season="summer",
            medal_type=s.medal_type,
            percentage=s.display_percent,
        )
        s.winter_medal_by_committee = plot_total_medals_by_country(
            df_olympic_medals,
            committee_list=s.committees,
            season="winter",
            medal_type=s.medal_type,
            percentage=s.display_percent,
        )
        s.total_medals_detail = int(
            df_grouped_medals[df_grouped_medals["Committee"] == s.committee_detail][
                "Total"
            ].iloc[0]
        )
        s.gold_medals_detail = int(
            df_grouped_medals[df_grouped_medals["Committee"] == s.committee_detail][
                "Gold"
            ].iloc[0]
        )
        s.silver_medals_detail = int(
            df_grouped_medals[df_grouped_medals["Committee"] == s.committee_detail][
                "Silver"
            ].iloc[0]
        )
        s.bronze_medals_detail = int(
            df_grouped_medals[df_grouped_medals["Committee"] == s.committee_detail][
                "Bronze"
            ].iloc[0]
        )
        s.summer_medal_grid = plot_medals_grid(
            df_olympic_medals, committee=state.committee_detail, season="summer"
        )
        s.winter_medal_grid = plot_medals_grid(
            df_olympic_medals, committee=state.committee_detail, season="winter"
        )


###########################################################
###                      Design Page                    ###
###########################################################


with tgb.Page() as committee_medals:

    tgb.text("## Medals Awarded to Committees", mode="md")
    tgb.text(
        "This dashboard presents aggregated data for the medals awarded to committees."
    )
    tgb.text(
        "Compare as many committees as needed with multiple selections. You can choose to compare all medals or just one medal color."
    )
    tgb.text(
        "Results can be shown as total medals or as a percentage of total medals per Olympic Games."
    )

    with tgb.layout("1 1 1"):
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
            tgb.toggle(
                value="{display_percent}",
                lov=["Total medals", "Percentage"],
                on_change=on_selector,
            )

    with tgb.layout("1 1"):
        with tgb.part():
            tgb.chart(figure="{summer_medal_by_committee}")
        with tgb.part():
            tgb.chart(figure="{winter_medal_by_committee}")

    ########################################################

    tgb.text("Detailed information by committee", class_name="h2")
    tgb.text(
        "Select a country to see total medals and how they distribute accross Olympics and disciplines."
    )
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
                "#### Gold Medals 🥇",
                mode="md",
            )
            tgb.text(
                "#### {gold_medals_detail}",
                mode="md",
            )
        with tgb.part("card"):
            tgb.text(
                "#### Silver Medals 🥈",
                mode="md",
            )
            tgb.text(
                "#### {silver_medals_detail}",
                mode="md",
            )
        with tgb.part("card"):
            tgb.text(
                "#### Bronze Medals 🥉",
                mode="md",
            )
            tgb.text(
                "#### {bronze_medals_detail}",
                mode="md",
            )
        with tgb.part("card"):
            tgb.text(
                "#### Total Medals 🏟",
                mode="md",
            )
            tgb.text(
                "#### {total_medals_detail}",
                mode="md",
            )
    with tgb.layout("1 1"):
        with tgb.part():
            tgb.chart(figure="{summer_medal_grid}")
        with tgb.part():
            tgb.chart(figure="{winter_medal_grid}")
