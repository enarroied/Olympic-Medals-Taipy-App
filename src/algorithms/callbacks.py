from algorithms.context import MedalTotals
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
        # Important to create new object:
        s.medal_totals = MedalTotals(
            int(len(s.df_olympic_medals)),
            _count_medals(s.df_olympic_medals, "Gold"),
            _count_medals(s.df_olympic_medals, "Silver"),
            _count_medals(s.df_olympic_medals, "Bronze"),
        )
