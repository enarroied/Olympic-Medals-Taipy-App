import plotly.express as px


def _create_grid_for_country(df_grouped, committee, season, ordered_olympiads):
    fig = px.imshow(
        df_grouped,
        labels=dict(x="Discipline", y="Olympiad", color="Total Medals"),
        x=df_grouped.columns,
        y=ordered_olympiads,
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


def create_medals_grid(df_medals, committee, season):
    """
    Plot medals won by a committee across different disciplines and Olympiads.

    Parameters:
    - df_medals (DataFrame): DataFrame containing medal data.
    - committee (str): Name of the committee.
    - season (str): Olympic season: "summer" or "winter".

    Returns:
    - fig: Plotly figure object showing medals by Olympiad and discipline for
      the committee.
    """
    df_filtered = df_medals[(df_medals["Olympic_season"] == season)]

    # Get all possible disciplines --> Like this, all disciplines appear for all
    # countries
    # Important to do this after filtering by season and before filtering by
    # committee!
    all_disciplines = df_filtered["Discipline"].unique()

    # And then only filter the DataFrame by committee
    df_filtered = df_filtered[(df_filtered["Committee"] == committee)]

    df_grouped = (
        df_filtered.groupby(["Olympiad", "Olympic_year", "Discipline"], observed=True)
        .size()
        .unstack(fill_value=0)
    )

    df_grouped = df_grouped.sort_index(level=1)
    ordered_olympiads = list(df_grouped.index.get_level_values("Olympiad").unique())

    # Add all the disciplines of the selcted season, whether the Committee won a
    #  medals or not
    df_grouped = df_grouped.reindex(columns=all_disciplines, fill_value=0)
    return _create_grid_for_country(df_grouped, committee, season, ordered_olympiads)


def plot_medals_grid_both_seasons(df_medals, committee):
    return (
        create_medals_grid(df_medals=df_medals, committee=committee, season="summer"),
        create_medals_grid(df_medals=df_medals, committee=committee, season="winter"),
    )
