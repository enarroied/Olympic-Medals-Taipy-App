from algorithms.context import MedalTotals


def init_total_medals(state):
    with state as s:
        s.medal_totals = _create_total_medal_cards(s.df_olympic_medals)
        on_selector_medals_by_committee(s)


def on_selector_medals_by_committee(state):
    with state as s:
        df_grouped_medals_olympics = s.df_grouped_medals_olympics.copy()
        selected_committe = s.committee_detail

        s.medal_details = create_medals_detail(
            df_grouped_medals_olympics, selected_committe
        )


def _create_total_medal_cards(df):
    counts = {m.lower(): _count_medals(df, m) for m in ["Gold", "Silver", "Bronze"]}
    return MedalTotals(len(df), **counts)


def create_medals_detail(df_grouped_medals_olympiads, committee_detail):
    """
    Returns total, gold, silver, and bronze medal counts for a given committee.

    Args:
        df_grouped_medals (pandas.DataFrame): DataFrame grouped by committee
    with medal counts.
        committee_detail (str): The committee name to look up.

    Returns:
        MedalTotals: medal counts as integers.
    """
    medal_row = df_grouped_medals_olympiads.loc[
        (df_grouped_medals_olympiads["Olympiad"] == "All")
        & (df_grouped_medals_olympiads["Committee"] == committee_detail)
    ]
    row_data = medal_row.iloc[0]

    return MedalTotals(
        row_data["Total"],
        row_data["Gold"],
        row_data["Silver"],
        row_data["Bronze"],
    )


def _count_medals(df, medal_type):
    return int((df["Medal_type"] == medal_type).sum())
