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


def _count_medals(df_olympic_medals, medal_type):
    return int(
        df_olympic_medals[df_olympic_medals["Medal_type"] == medal_type][
            "Medal_type"
        ].count()
    )


def init_total_medals(state):
    with state as s:
        df_olympic_medals = s.df_olympic_medals

        s.total_medals = int(len(df_olympic_medals))
        s.total_gold_medals = _count_medals(df_olympic_medals, "Gold")
        s.total_silver_medals = _count_medals(df_olympic_medals, "Silver")
        s.total_bronze_medals = _count_medals(df_olympic_medals, "Bronze")


def get_last_olympic(state):
    state.latest_olympiad = state.df_olympic_medals.loc[
        state.df_olympic_medals["Olympic_year"].idxmax(), "Olympiad"
    ]
