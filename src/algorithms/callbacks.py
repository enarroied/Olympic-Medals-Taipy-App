from algorithms.medal_details import create_medals_detail


def on_selector_medals_by_committee(state):
    with state as s:
        df_grouped_medals_olympics = s.df_grouped_medals_olympics.copy()
        selected_committe = s.committee_detail

        (
            s.total_medals_detail,
            s.gold_medals_detail,
            s.silver_medals_detail,
            s.bronze_medals_detail,
        ) = create_medals_detail(df_grouped_medals_olympics, selected_committe)


def init_total_medals(state):
    with state as s:
        df_olympic_medals = s.df_olympic_medals

        s.total_medals = int(len(df_olympic_medals))
        s.total_gold_medals = int(
            df_olympic_medals[df_olympic_medals["Medal_type"] == "Gold"][
                "Medal_type"
            ].count()
        )
        s.total_silver_medals = int(
            df_olympic_medals[df_olympic_medals["Medal_type"] == "Silver"][
                "Medal_type"
            ].count()
        )
        s.total_bronze_medals = int(
            df_olympic_medals[df_olympic_medals["Medal_type"] == "Bronze"][
                "Medal_type"
            ].count()
        )


def get_last_olympic(state):
    state.latest_olympiad = state.df_olympic_medals.loc[
        state.df_olympic_medals["Olympic_year"].idxmax(), "Olympiad"
    ]
