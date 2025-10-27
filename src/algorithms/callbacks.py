from algorithms.context import MedalTotals


def _get_medal_count(df_grouped_medals, medal_type, committee_detail):
    return int(
        df_grouped_medals[df_grouped_medals["Committee"] == committee_detail][
            medal_type
        ].iloc[0]
    )


def create_medals_detail(df_grouped_medals_olympiads, committee_detail):
    """
    Returns total, gold, silver, and bronze medal counts for a given committee.

    Args:
        df_grouped_medals (pandas.DataFrame): DataFrame grouped by committee
    with medal counts.
        committee_detail (str): The committee name to look up.

    Returns:
        tuple: (Total, Gold, Silver, Bronze) medal counts as integers.
    """
    df_grouped_medals = df_grouped_medals_olympiads.copy()
    df_grouped_medals = df_grouped_medals[df_grouped_medals["Olympiad"] == "All"]
    df_grouped_medals = df_grouped_medals.drop(columns="Olympiad")
    return (
        _get_medal_count(df_grouped_medals, "Total", committee_detail),
        _get_medal_count(df_grouped_medals, "Gold", committee_detail),
        _get_medal_count(df_grouped_medals, "Silver", committee_detail),
        _get_medal_count(df_grouped_medals, "Bronze", committee_detail),
    )


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
