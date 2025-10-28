import taipy.gui.builder as tgb

from algorithms import on_selector_medals_by_committee
from page_utils import builder_extension as tgb_ext

with tgb.Page() as committee_medals:
    tgb_ext.text_from_file("./pages/info_medals_by_committee.md")
    with tgb.layout("1 1 1"):
        with tgb.part():
            tgb_ext.drop_down_selector(
                value="{committees}",
                lov="{list_committees}",
                label="Select committees",
                multiple=True,
            )
        with tgb.part():
            tgb_ext.drop_down_selector(
                value="{medal_type}",
                lov="{list_medal_types}",
                label="Select medal type",
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

    tgb.text("## Detailed information by committee", mode="md")
    tgb.text(
        "Select a country to see total medals and how they distribute accross\
              Olympics and disciplines."
    )
    with tgb.layout("1 1 1 1 1"):
        tgb_ext.drop_down_selector(
            value="{committee_detail}",
            lov="{list_committees}",
            label="Select committee for detail",
            on_change=on_selector_medals_by_committee,
        )
        with tgb.part("card"):
            tgb.text(
                "#### Gold Medals 🥇",
                mode="md",
            )
            tgb.text(
                "#### {medal_details.gold}",
                mode="md",
            )
        with tgb.part("card"):
            tgb.text(
                "#### Silver Medals 🥈",
                mode="md",
            )
            tgb.text(
                "#### {medal_details.silver}",
                mode="md",
            )
        with tgb.part("card"):
            tgb.text(
                "#### Bronze Medals 🥉",
                mode="md",
            )
            tgb.text(
                "#### {medal_details.bronze}",
                mode="md",
            )
        with tgb.part("card"):
            tgb.text(
                "#### Total Medals 🏟",
                mode="md",
            )
            tgb.text(
                "#### {medal_details.total}",
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
