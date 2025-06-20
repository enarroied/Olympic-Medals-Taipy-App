import pandas as pd
import plotly.express as px


def plot_total_medals_by_country(
    df_medals, committee_list, season, medal_type="All", percentage="Total medals"
):
    """
    Plot total medals won by selected committees over Olympic years (by olympic season winter/summer).

    Parameters:
    - df_medals (DataFrame): DataFrame containing medal data.
    - committee_list (list): List of committees to plot.
    - season (str): Olympic season: "summer" or "winter".
    - medal_type (str): Type of medal. Default is "All".
    - percentage (str): Type of representation. Default is "Total medals". Other option is "Percentage"

    Returns:
    - fig: Plotly figure object showing total medals by year for selected committees.
    """

    df_filtered = df_medals[df_medals["Olympic_season"] == season]
    if medal_type != "All":
        df_filtered = df_filtered[df_filtered["Medal_type"] == medal_type]

    # Quick fix: Replace "Stockholm 1956" with "Melbourne 1956"
    df_filtered.loc[df_filtered["Olympiad"] == "Stockholm 1956", "Olympiad"] = (
        "Melbourne 1956"
    )

    # Create a complete grid of all years, Olympiads, and committees for merging
    years_olympiads = df_filtered[["Olympic_year", "Olympiad"]].drop_duplicates()
    committees = pd.DataFrame({"Committee": committee_list})

    # Cartesian product of years/olympiads and committees
    full_grid = years_olympiads.merge(committees, how="cross")

    df_totals = (
        df_filtered.groupby(["Olympic_year", "Olympiad", "Committee"], observed=True)
        .size()
        .reset_index(name="Medal_count")
    )

    df_totals = full_grid.merge(
        df_totals, on=["Olympic_year", "Olympiad", "Committee"], how="left"
    ).fillna({"Medal_count": 0})

    # Pivot to have committees as columns
    df_pivot = df_totals.pivot_table(
        index=["Olympic_year", "Olympiad"],
        columns="Committee",
        values="Medal_count",
        fill_value=0,
        observed=True,
    ).reset_index()

    df_totals_max = (
        df_pivot.set_index(["Olympic_year", "Olympiad"])
        .sum(axis=1)
        .reset_index(name="Total_medals")
    )

    if percentage == "Percentage":
        df_pivot = df_pivot.merge(df_totals_max, on=["Olympic_year", "Olympiad"])
        for committee in committee_list:
            df_pivot[committee] = (
                df_pivot[committee] * 100 / df_pivot["Total_medals"]
            ).fillna(0)
        value_label = "Percentage of Medals"
        df_pivot = df_pivot.drop(columns=["Total_medals"])
    else:
        value_label = "Total Medals"

    fig = px.line(
        df_pivot,
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
