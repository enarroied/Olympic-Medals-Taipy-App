import plotly.express as px


def _create_df_to_plot_medals(
    df_medals, committee_list, season, medal_type, percentage
):
    df_filtered = df_medals[
        (df_medals["Olympic_season"] == season)
        & (df_medals["Medal_type"] == medal_type)
    ]

    columns_to_plot = ["Olympic_year", "Olympiad", "Total_medals"] + committee_list
    df_to_plot = df_filtered[columns_to_plot]

    if percentage == "Percentage":
        for committee in committee_list:
            df_to_plot.loc[:, committee] = (
                df_to_plot[committee] * 100 / df_to_plot["Total_medals"]
            ).fillna(0)
    df_to_plot = df_to_plot.drop(columns=["Total_medals"])
    return df_to_plot


def _create_fig_total_medals_by_country(
    df_to_plot, committee_list, season, medal_type, value_label
):
    fig = px.line(
        df_to_plot,
        x="Olympic_year",
        y=committee_list,
        labels={
            "value": value_label,
            "variable": "Committee",
            "Olympic_year": "Year",
            "Olympiad": "Olympiad",
        },
        title=f"{medal_type} Medals for Selected Committees by Olympic Year | {season}",
        hover_data={"Olympiad": True},
    )
    fig.update_traces(mode="markers+lines", marker=dict(size=4))
    return fig


def plot_total_medals_by_country(
    df_total_medals_by_olympiad_and_committee,
    committee_list,
    season,
    medal_type="All",
    percentage="Total medals",
):
    """
    Plot total medals won by selected committees over Olympic years (by olympic season winter/summer).

    Parameters:
    - df_total_medals_by_olympiad_and_committee (DataFrame): DataFrame containing medal data.
    - committee_list (list): List of committees to plot.
    - season (str): Olympic season: "summer" or "winter".
    - medal_type (str): Type of medal. Default is "All".
    - percentage (str): Type of representation. Default is "Total medals". Other option is "Percentage"

    Returns:
    - fig: Plotly figure object showing total medals by year for selected committees.
    """
    df_medals = df_total_medals_by_olympiad_and_committee.copy()
    df_to_plot = _create_df_to_plot_medals(
        df_medals, committee_list, season, medal_type, percentage
    )
    value_label = (
        "Percentage of Medals" if percentage == "Percentage" else "Total Medals"
    )
    return _create_fig_total_medals_by_country(
        df_to_plot, committee_list, season, medal_type, value_label
    )


def plot_total_medals_by_country_both_seasons(
    df_total_medals_by_olympiad_and_committee,
    committee_list,
    medal_type="All",
    percentage="Total medals",
):
    return (
        plot_total_medals_by_country(
            df_total_medals_by_olympiad_and_committee=df_total_medals_by_olympiad_and_committee,
            committee_list=committee_list,
            season="summer",
            medal_type=medal_type,
            percentage=percentage,
        ),
        plot_total_medals_by_country(
            df_total_medals_by_olympiad_and_committee=df_total_medals_by_olympiad_and_committee,
            committee_list=committee_list,
            season="winter",
            medal_type=medal_type,
            percentage=percentage,
        ),
    )


def plot_medals_grid(df_medals, committee, season):
    """
    Plot medals won by a committee across different disciplines and Olympiads.

    Parameters:
    - df_medals (DataFrame): DataFrame containing medal data.
    - committee (str): Name of the committee.
    - season (str): Olympic season: "summer" or "winter".

    Returns:
    - fig: Plotly figure object showing medals by Olympiad and discipline for the committee.
    """
    # Filter DataFrame by season
    df_filtered = df_medals[(df_medals["Olympic_season"] == season)]

    # Get all possible disciplines --> Like this, all disciplines appear for all countries
    # Important to do this after filtering by season and before filtering by committee!
    all_disciplines = df_filtered["Discipline"].unique()

    # And then only filter the DataFrame by committee
    df_filtered = df_filtered[(df_filtered["Committee"] == committee)]

    # Group by Olympiad and Discipline, then count occurrences
    df_grouped = (
        df_filtered.groupby(["Olympiad", "Olympic_year", "Discipline"], observed=True)
        .size()
        .unstack(fill_value=0)
    )
    # Sort the index by "Olympic_year"
    df_grouped = df_grouped.sort_index(level=1)
    ordered_olympiads = df_grouped.index.get_level_values("Olympiad").unique()

    # Add all the disciplines of the selcted season, whether the Committee won a medals or not
    df_grouped = df_grouped.reindex(columns=all_disciplines, fill_value=0)

    fig = px.imshow(
        df_grouped,
        labels=dict(x="Discipline", y="Olympiad", color="Total Medals"),
        x=df_grouped.columns,
        y=list(ordered_olympiads),
        color_continuous_scale="plasma",
        title=f"Medals by Olympiad and discipline for {committee} | {season}",
    )
    # reduce font size:
    fig.update_layout(
        xaxis=dict(tickfont=dict(size=9)),
        yaxis=dict(tickfont=dict(size=9)),
        coloraxis_colorbar=dict(
            tickfont=dict(size=9),
        ),
    )
    return fig


def plot_medals_grid_both_seasons(df_medals, committee):
    return (
        plot_medals_grid(df_medals=df_medals, committee=committee, season="summer"),
        plot_medals_grid(df_medals=df_medals, committee=committee, season="winter"),
    )
