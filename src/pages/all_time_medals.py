import taipy.gui.builder as tgb

from page_utils import builder_extension as tgb_ext

with tgb.Page() as all_time_medals:
    tgb.text("## Medals awarded at all Olympic games", mode="md")
    tgb.text(
        "This dashboard displays aggregated data for the medals awarded across\
              the Olympics, from Athens 1896 to {latest_olympiad}."
    )
    with tgb.layout("1 1 1 1"):
        with tgb.part("card card-bg"):
            tgb.text(
                "#### Total Gold Medals 🥇 ",
                mode="md",
            )
            tgb.text(
                "#### {medal_totals.gold}",
                mode="md",
            )
        with tgb.part("card card-bg"):
            tgb.text(
                "#### Total Silver Medals 🥈",
                mode="md",
            )
            tgb.text(
                "#### {medal_totals.silver}",
                mode="md",
            )
        with tgb.part("card card-bg"):
            tgb.text(
                "#### Total Bronze Medals 🥉",
                mode="md",
            )
            tgb.text(
                "#### {medal_totals.bronze}",
                mode="md",
            )
        with tgb.part("card card-bg"):
            tgb.text(
                "#### Total Medals 🏟",
                mode="md",
            )
            tgb.text(
                "#### {medal_totals.total}",
                mode="md",
            )

    # Bar chart of all medals:
    with tgb.layout("1 1"):
        with tgb.part():
            tgb_ext.drop_down_selector(
                value="{season}",
                lov="{list_seasons}",
                label="Select season",
            )
            tgb.chart(
                figure=lambda medals_by_season,
                season: medals_by_season.create_bar_medal_season(season)
            )

        with tgb.part():
            tgb_ext.drop_down_selector(
                value="{selected_olympiad}",
                lov="{list_olympiads}",
                label="Select Olympiad",
            )
            tgb.chart(
                figure=lambda medals_by_olimpics,
                selected_olympiad: medals_by_olimpics.create_medals_by_olympics(
                    selected_olympiad
                )
            )
        with tgb.part():
            with tgb.layout("1 1"):
                with tgb.part():
                    tgb.selector(
                        value="{selected_season_map}",
                        lov="{list_seasons_map}",
                        dropdown=True,
                        label="Select season for map",
                        class_name="fullwidth",
                    )
                with tgb.part():
                    tgb.selector(
                        value="{selected_medal_color}",
                        lov="{list_medal_types}",
                        dropdown=True,
                        label="Select medal color",
                        class_name="fullwidth",
                    )
            tgb.chart(
                figure=lambda medal_map,
                selected_season_map,
                selected_medal_color: medal_map.create_olympic_medals_by_country(
                    selected_season_map, selected_medal_color
                )
            )
        with tgb.part():
            tgb_ext.drop_down_selector(
                value="{selected_olympiad_for_sunburst}",
                lov="{list_olympiads}",
                label="Select Olympiad",
            )
            tgb.chart(
                figure=lambda sunburnst_by_gender,
                selected_olympiad_for_sunburst: sunburnst_by_gender.create_sunburst_medals(
                    selected_olympiad_for_sunburst
                )
            )

    with tgb.expandable(expanded=False, title="Total Medals by Event"):
        tgb.table("{df_olympic_cities_simplified}", filter=True, page_size=20)
