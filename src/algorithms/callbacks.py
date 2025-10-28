from algorithms.context import MedalTotals


def init_total_medals(state):
    with state as s:
        s.medal_totals = create_total_medal_cards(s.df_olympic_medals)
        on_selector_medals_by_committee(s)


def on_selector_medals_by_committee(state):
    with state as s:
        df_grouped_medals_olympics = s.df_grouped_medals_olympics.copy()
        selected_committe = s.committee_detail

        s.medal_details = create_medals_detail(
            df_grouped_medals_olympics, selected_committe
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
    df_grouped_medals = df_grouped_medals.query(
        "Olympiad == 'All' and Committee == @committee_detail"
    ).drop(columns="Olympiad")
    return MedalTotals(
        _get_medal_count(df_grouped_medals, "Total"),
        _get_medal_count(df_grouped_medals, "Gold"),
        _get_medal_count(df_grouped_medals, "Silver"),
        _get_medal_count(df_grouped_medals, "Bronze"),
    )


def create_total_medal_cards(df):
    counts = {m.lower(): _count_medals(df, m) for m in ["Gold", "Silver", "Bronze"]}
    return MedalTotals(len(df), **counts)


def _count_medals(df, medal_type):
    return int((df["Medal_type"] == medal_type).sum())


def _get_medal_count(df_grouped_medals, medal_type):
    return int(df_grouped_medals[medal_type].iloc[0])
