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


def _count_medals(df, medal_type):
    return int((df["Medal_type"] == medal_type).sum())


def init_total_medals(state):
    with state as s:
        df = s.df_olympic_medals
        counts = {m.lower(): _count_medals(df, m) for m in ["Gold", "Silver", "Bronze"]}
        print(counts)
        s.medal_totals = MedalTotals(len(df), **counts)
