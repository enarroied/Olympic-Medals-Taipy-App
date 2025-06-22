import taipy.gui.builder as tgb

from algorithms.plotting_all_time import (
    create_bar_by_committee,
    create_bar_medals,
    create_sunburnst_medals,
    plot_olympic_medals_by_country,
)


def on_selector(state):
    with state as s:
        df_olympic_cities = s.df_olympic_cities.copy()
        df_olympic_medals = s.df_olympic_medals.copy()
        df_medals_by_olympiad = s.df_medals_by_olympiad.copy()

        s.bar_medals = create_bar_medals(df_medals_by_olympiad, s.season)
        s.bar_medals_by_committee = create_bar_by_committee(
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
                lov="{list_seasons}",
                dropdown=True,
                label="Select season",
                class_name="fullwidth",
                on_change=on_selector,
            )
            tgb.chart(figure="{bar_medals}")

        with tgb.part():
            tgb.selector(
                value="{selected_olympiad}",
                lov="{list_olympiads}",
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
                        lov="{list_seasons_map}",
                        dropdown=True,
                        label="Select season for map",
                        class_name="fullwidth",
                        on_change=on_selector,
                    )
                with tgb.part():
                    tgb.selector(
                        value="{selected_medal_color}",
                        lov="{list_medal_types}",
                        dropdown=True,
                        label="Select medal color",
                        class_name="fullwidth",
                        on_change=on_selector,
                    )
            tgb.chart(figure="{map_medals}")
        with tgb.part():
            tgb.selector(
                value="{selected_olympiad_for_sunburst}",
                lov="{list_olympiads}",
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
