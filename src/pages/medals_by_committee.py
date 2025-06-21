import pandas as pd
import taipy.gui.builder as tgb

from algorithms.plotting_medals_by_committee import (
    plot_medals_grid,
    plot_total_medals_by_country,
)


###########################################################
###                  Selector Function                  ###
###########################################################
def on_selector(state):
    with state as s:
        df_grouped_medals = s.df_grouped_medals.copy()
        df_olympic_medals = s.df_olympic_medals.copy()
        selected_committe = s.committee_detail

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
            df_grouped_medals[df_grouped_medals["Committee"] == selected_committe][
                "Total"
            ].iloc[0]
        )
        s.gold_medals_detail = int(
            s.df_grouped_medals[df_grouped_medals["Committee"] == selected_committe][
                "Gold"
            ].iloc[0]
        )
        s.silver_medals_detail = int(
            s.df_grouped_medals[df_grouped_medals["Committee"] == selected_committe][
                "Silver"
            ].iloc[0]
        )
        s.bronze_medals_detail = int(
            s.df_grouped_medals[df_grouped_medals["Committee"] == selected_committe][
                "Bronze"
            ].iloc[0]
        )
        s.summer_medal_grid = plot_medals_grid(
            s.df_olympic_medals, committee=selected_committe, season="summer"
        )
        s.winter_medal_grid = plot_medals_grid(
            s.df_olympic_medals, committee=selected_committe, season="winter"
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
                lov="{list_committees}",
                dropdown=True,
                multiple=True,
                label="Select committees",
                class_name="fullwidth",
                on_change=on_selector,
            )
        with tgb.part():
            tgb.selector(
                value="{medal_type}",
                lov="{list_medal_types}",
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
            lov="{list_committees}",
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
