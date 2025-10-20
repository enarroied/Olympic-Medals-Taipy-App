import taipy.gui.builder as tgb

from algorithms.callbacks import on_selector_medals_by_committee

with tgb.Page() as committee_medals:
    tgb.text("## Medals Awarded to Committees", mode="md")
    tgb.text(
        "This dashboard presents aggregated data for the medals awarded to\
              committees."
    )
    tgb.text(
        "Compare as many committees as needed with multiple selections. You can\
              choose to compare all medals or just one medal color."
    )
    tgb.text(
        "Results can be shown as total medals or as a percentage of total medals\
              per Olympic Games."
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
            )
        with tgb.part():
            tgb.selector(
                value="{medal_type}",
                lov="{list_medal_types}",
                dropdown=True,
                label="Select medal type",
                class_name="fullwidth",
            )
        with tgb.part():
            tgb.toggle(
                value="{display_percent}",
                lov=["Total", "Percentage"],
                label="Medal Display: ",
            )

    with tgb.layout("1 1"):
        with tgb.part():
            tgb.chart(
                figure=lambda medals_by_country,
                committees,
                medal_type,
                display_percent: medals_by_country.create_medals_by_country_summer(
                    committees, medal_type, display_percent
                )
            )
        with tgb.part():
            tgb.chart(
                figure=lambda medals_by_country,
                committees,
                medal_type,
                display_percent: medals_by_country.create_medals_by_country_winter(
                    committees, medal_type, display_percent
                )
            )

    ########################################################

    tgb.text("Detailed information by committee", class_name="h2")
    tgb.text(
        "Select a country to see total medals and how they distribute accross\
              Olympics and disciplines."
    )
    with tgb.layout("1 1 1 1 1"):
        tgb.selector(
            value="{committee_detail}",
            lov="{list_committees}",
            dropdown=True,
            label="Select committee for detail",
            class_name="fullwidth",
            on_change=on_selector_medals_by_committee,
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
            tgb.chart(
                figure=lambda medals_by_olympic_and_discipline,
                committee_detail: medals_by_olympic_and_discipline.plot_medals_grid_summer(
                    committee_detail
                )
            )
        with tgb.part():
            tgb.chart(
                figure=lambda medals_by_olympic_and_discipline,
                committee_detail: medals_by_olympic_and_discipline.plot_medals_grid_winter(
                    committee_detail
                )
            )
