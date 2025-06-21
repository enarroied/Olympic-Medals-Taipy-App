def _get_medal_count(df_grouped_medals, medal_type, committee_detail):
    return int(
        df_grouped_medals[df_grouped_medals["Committee"] == committee_detail][
            medal_type
        ].iloc[0]
    )


def create_medals_detail(df_grouped_medals, committee_detail):
    """
    Returns total, gold, silver, and bronze medal counts for a given committee.

    Args:
        df_grouped_medals (pandas.DataFrame): DataFrame grouped by committee with medal counts.
        committee_detail (str): The committee name to look up.

    Returns:
        tuple: (Total, Gold, Silver, Bronze) medal counts as integers.
    """
    return (
        _get_medal_count(df_grouped_medals, "Total", committee_detail),
        _get_medal_count(df_grouped_medals, "Gold", committee_detail),
        _get_medal_count(df_grouped_medals, "Silver", committee_detail),
        _get_medal_count(df_grouped_medals, "Bronze", committee_detail),
    )
